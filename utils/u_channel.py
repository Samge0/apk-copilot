import os
import subprocess
import zipfile

from utils import u_date, u_config
from utils import u_file

"""
apk多渠道打包&签名相关工具类
"""

# res目录，这里加 .. 是相对 build-tools 目录而言，因为程序中会执行 os.chdir(build_tool_path) 进入 buildTool 目录
res_path = f"../.."

# sdk 编译环境的位置
# build_tool_path = f"res/build-tools/31.0.0"
build_tool_path = f"res/build-tools/33.0.0"

# walle的jar文件路径
walle_jar_file = f"{res_path}/jars/walle-cli-all.jar"
# 签名检查的jar文件路径
check_android_v2_signature_jar_file = f"{res_path}/jars/CheckAndroidV2Signature.jar"


def parse_channel_with_sign() -> (str, list):
    """
    处理多渠道签名
    :return:
    """

    # 读取配置
    option = u_config.user_config

    # 当前登录用户名
    username = option.username

    # 签名别名
    key_alias = option.key_alias
    # 签名别名-密码
    key_store_pw = option.key_store_pw
    # 签名密码
    key_pw = option.key_pw
    # 签名文件路径
    key_file = option.key_file

    # 渠道配置的文件路径
    channel_file = option.channel_file

    # 移动到buildtool目录
    os.chdir(f"{get_project_root_path()}/{build_tool_path}")

    # 今天的日期字符串
    today_str = u_date.get_today_str(f='%Y-%m-%d')
    # 输出的渠道文件目录
    outputs_dir = f"{res_path}/outputs/{today_str}/{username}"
    u_file.makedirs(outputs_dir, need_clean=True)

    # 签名之后的名称
    apk_filename = get_filename(option.apk_name) if option.apk_name else get_filename(option.apk_path)
    sign_save_dir = f"{res_path}/apks/{today_str}/{username}"
    u_file.makedirs(sign_save_dir, need_clean=True)
    sign_apk_path = f"{sign_save_dir}/{apk_filename}_sign.apk"

    # zipalign操作
    status, error_msg = parse_zipalign(option.apk_path, sign_apk_path)
    if not status:
        return error_msg, None

    # 进行签名
    status, error_msg = parse_apksigner(key_file, key_alias, key_store_pw, key_pw, sign_apk_path)
    if not status:
        return error_msg, None

    # 验证签名
    status, error_msg = parse_signature_check(sign_apk_path)
    if not status:
        return error_msg, None

    # 多渠道打包
    status, error_msg = parse_batch_channel(channel_file, outputs_dir, sign_apk_path)
    if not status:
        return error_msg, None

    # apk文件路径填充渠道别名信息
    file_output_lst = rename_apk(apk_filename, channel_file, option, outputs_dir)

    # 判断是否需要输出为zip压缩包
    zip_file_path = zip_apk_dir(outputs_dir, sign_apk_path, option)
    if zip_file_path:
        file_output_lst.append(zip_file_path)

    file_output_lst = file_output_lst if len(file_output_lst or []) > 0 else None
    return None, file_output_lst


def rename_apk(apk_filename, channel_file, option, outputs_dir) -> list:
    """
    对已输出的渠道apk文件进行重名件，将渠道别名添加到apk文件名中，方便后续选取

    :param apk_filename: 上传的apk名称
    :param channel_file: 渠道配置文件
    :param option: 操作配置
    :param outputs_dir: apk所在目录
    :return:
    """
    # 文件输出列表
    file_output_lst = []
    # 批量替换渠道文件名
    channel_dict = get_channel_dict(channel_file)
    # 遍历目录
    for root, dirs, files in os.walk(outputs_dir):
        for filename in files:
            # 判断文件名是否符合条件
            if not filename.endswith('.apk'):
                continue
            channel_key = filename.replace('.apk', '').split('_')[-1]
            channel_name = channel_dict.get(channel_key) or ''
            if not channel_name:
                continue

            # 按照指定规则修改文件名
            new_filename = filename.replace('.apk', f'_{channel_name}.apk')
            # 拼接完整路径
            old_path = os.path.join(root, filename)
            new_path = os.path.join(root, new_filename)
            print(old_path, '->', new_path)

            # 执行修改操作
            if u_file.exists(new_path):
                os.remove(new_path)
            os.rename(old_path, new_path)

            # 如果不是压缩模式 && 是本次操作的同名文件，则添加到输出文件列表
            if not option.zip_enable and apk_filename in new_path:
                file_output_lst.append(new_path)

    return file_output_lst


def parse_batch_channel(channel_file, outputs_dir, sign_apk_path) -> (bool, str):
    """
    # 使用 Walle 工具批量给一个已经签名的 APK 文件打渠道包。具体来说：
    # 参数说明：
    # {walle_jar_file} 是指 Walle 工具的 Jar 文件路径；
    # "batch" 是命令参数，表示批处理模式；
    # "-f {channel_file}" 表示指定渠道列表文件的路径；
    # {sign_apk_path} 是指已经签名的 APK 文件的路径；
    # {outputs_dir} 是指输出渠道包的目录路径。
    # 在执行此命令时，Walle 工具会读取渠道列表文件（即 {channel_file}），并在已签名的 APK 文件中添加渠道信息。
    # 然后，它会将生成的渠道包文件保存到指定的输出目录（即 {outputs_dir}）中。
    # 渠道包的命名方式为：原 APK 文件名-渠道名.apk。这个命令通常用于批量生成多个渠道包，以便在发布应用程序时方便地分发给不同的渠道。

    :param channel_file: 渠道列表文件的路径
    :param outputs_dir: 输出渠道包的目录路径
    :param sign_apk_path: 已经签名的 APK 文件的路径
    :return:
    """
    try:
        cmd = f"java -jar {walle_jar_file} batch -f {channel_file} {sign_apk_path} {outputs_dir}"
        ret = os.system(cmd)
        if ret == 0:
            print("渠道包生成成功")
            return True, "渠道包生成成功"
        else:
            print("渠道包生成失败")
            return False, "渠道包生成失败"
    except Exception as e:
        return False, f"渠道包生成失败，error={e}"


def parse_signature_check(sign_apk_path) -> (bool, str):
    """
    # 使用检查 Android V2 签名的 Jar 文件来验证一个已经签名的 APK 文件的签名是否有效。具体来说：
    # 参数说明：
    # {check_android_v2_signature_jar_file} 是指 Android V2 签名检查工具的 Jar 文件路径；
    # {sign_apk_path} 是指已经签名的 APK 文件的路径。
    # 当你运行这个命令时，它会读取 APK 文件中的签名信息并使用 Android V2 签名检查工具来验证该签名是否有效。
    # 如果签名有效，则命令会输出一个 "Verified" 的消息，否则会输出一个错误消息。

    :param sign_apk_path: 已经签名的 APK 文件的路径
    :return:
    """
    try:
        cmd = f"java -jar {check_android_v2_signature_jar_file} {sign_apk_path}"
        ret = os.system(cmd)
        if ret == 0:
            print("验证签名成功")
            return True, "验证签名成功"
        else:
            print("验证签名失败")
            return False, "验证签名失败"
    except Exception as e:
        return False, f"验证签名失败，error={e}"


def read_key_info(key_file, key_alias, key_store_pw, key_pw) -> (bool, str):
    """
    读取秘钥信息
        例如：
            keytool -list -v -keystore 密钥文件路径 -alias 密钥别名 -storepass 密钥库密码 -keypass 密钥密码

    :param key_file: 应用程序签名的密钥库 (keystore) 文件路径
    :param key_alias: 用于签署 APK 文件的密钥库中的密钥别名
    :param key_store_pw: 密钥库密码
    :param key_pw: 密钥密码
    :return:
    """
    try:
        if not key_file or not u_file.exists(key_file):
            return False, "请上传正确格式的秘钥文件"

        if not key_alias:
            return False, "请配置“秘钥别名”"

        if not key_store_pw:
            return False, "请配置“密钥库密码”"

        cmd = ["keytool", "-list", "-v", "-keystore", key_file, "-alias", key_alias]
        if key_store_pw:
            cmd += ["-storepass", key_store_pw]
        if key_pw:
            cmd += ["-keypass", key_pw]
        # print(' '.join(cmd))
        result = subprocess.run(cmd, capture_output=True, timeout=10)
        byte_str = result.stdout
        byte_encoding = check_encoding(byte_str)
        if not byte_encoding:
            return False, f"读取秘钥信息错误，未知的编码格式：{byte_str}"
        output = byte_str.decode(byte_encoding)
        return True, output
    except Exception as e:
        return False, f"读取秘钥信息错误，error={e}"


def check_encoding(byte_str) -> str:
    try:
        byte_str.decode('utf-8')
        return 'utf-8'
    except UnicodeDecodeError:
        try:
            byte_str.decode('gbk')
            return 'gbk'
        except UnicodeDecodeError:
            return 'unknown'


def parse_apksigner(key_file, key_alias, key_store_pw, key_pw, sign_apk_path) -> (bool, str):
    """
    # 对一个 Android 应用程序包 (APK) 进行签名，以确保该 APK 文件的完整性和来源可信。具体来说，
    # 该命令会在 APK 文件的 META-INF 文件夹中添加一个签名文件，并将其与应用程序的证书一起打包到 APK 文件中。
    # 参数说明：
    # --ks：指定应用程序签名的密钥库 (keystore) 文件路径。
    # --ks-key-alias：指定用于签署 APK 文件的密钥库中的密钥别名。
    # --ks-pass pass:{key_store_pw}：指定密钥库密码，这里的 {key_store_pw} 是指密钥库密码。
    # --key-pass pass:{key_pw}：指定用于签署 APK 文件的密钥密码，这里的 {key_pw} 是指密钥密码。
    # {sign_apk_path}：需要签名的 APK 文件路径。
    # 该命令需要提供一个密钥库文件以及密钥别名和密码等信息。这些信息通常是由开发人员在应用程序开发过程中生成和管理的。
    # 签名后的 APK 文件通常是发布给最终用户的版本，以确保用户能够安全地下载和安装应用程序。
    # 签名还可以帮助 Android 系统验证应用程序的来源和完整性，并提供基本的应用程序安全保护措施。

    :param key_file: 应用程序签名的密钥库 (keystore) 文件路径
    :param key_alias: 用于签署 APK 文件的密钥库中的密钥别名
    :param key_store_pw: 密钥库密码
    :param key_pw: 密钥密码
    :param sign_apk_path: 需要签名的 APK 文件路径
    :return:
    """
    try:
        if not key_file or not u_file.exists(key_file):
            return False, "请上传正确格式的秘钥文件"

        if not key_alias:
            return False, "请配置“秘钥别名”"

        if not key_store_pw:
            return False, "请配置“密钥库密码”"

        cmd = f"apksigner sign --ks {key_file} --ks-key-alias {key_alias} --ks-pass pass:{key_store_pw} --key-pass pass:{key_pw} {sign_apk_path}"
        ret = os.system(cmd)
        if ret == 0:
            print("sign成功")
            return True, "sign成功"
        else:
            print("sign失败")
            return False, "sign失败"
    except Exception as e:
        return False, f"sign失败，error={e}"


def parse_zipalign(apk_path, sign_apk_path) -> (bool, str):
    """
    # 对一个 Android 应用程序包 (APK) 进行优化，以便于在 Android 设备上运行时能够更高效地使用内存和处理器。
    # 具体来说，该命令会将 APK 文件中的资源和数据进行重新排列，以便于在内存中加载和访问。这可以提高应用程序的启动速度和响应速度，并减少内存使用量。
    # 参数说明：
    # -v：输出详细的日志信息。
    # -f：强制执行操作，即覆盖已存在的输出文件。
    # 4：对齐的字节对齐数，这里设为4，表示按4个字节对齐。
    # {apk_path}：输入的 APK 文件路径。
    # {sign_apk_path}：输出的已签名 APK 文件路径。

    :param apk_path: 输入的 APK 文件路径
    :param sign_apk_path: 输出的已签名 APK 文件路径
    :return:
    """
    try:
        cmd = f"zipalign -v -f 4 {apk_path} {sign_apk_path}"
        print(cmd)
        ret = os.system(cmd)
        if ret == 0:
            print("zipalign成功")
            return True, "zipalign成功"
        else:
            print("zipalign失败")
            return False, "zipalign失败"
    except Exception as e:
        return False, f"zipalign失败，error={e}"


def get_channel_dict(channel_file_path: str) -> dict:
    """
    解析渠道文件并转化为字典，为后续替换文件名做准备

    :param channel_file_path:
    :return:
    """
    channel_dict = {}
    channel_text = u_file.read(channel_file_path) or ''
    for line in channel_text.split('\n') or []:
        _splits = line.replace(' ', '').split('#')
        if len(_splits) == 2:
            channel_dict[_splits[0]] = _splits[1]
    return channel_dict


def zip_apk_dir(directory_path, sign_apk_path, option):
    """
    将apk文件添加到压缩包

    :param directory_path: 要压缩的文件夹的路径
    :param sign_apk_path: 已经签名的apk文件目录
    :param option: 操作配置
    :return:
    """

    if not option.zip_enable:
        return None

    # 今天的日期字符串
    today_str = u_date.get_today_str(f='%Y-%m-%d')

    # 压缩包文件输出目录
    apk_name = get_filename(sign_apk_path)
    zip_file_path = f"{directory_path}/{apk_name}_{today_str}.zip"

    print('正在将结果文件夹输出为zip压缩包……')
    if u_file.exists(zip_file_path):
        os.remove(zip_file_path)
    tmp_zip_file = f'result-{u_date.get_timestamp()}.zip'
    _zipfile = zipfile.ZipFile(tmp_zip_file, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(directory_path):
        for filename in files:

            if apk_name not in str(filename):
                continue

            if not str(filename).endswith('.apk'):
                continue

            print(f"正在压缩：{filename}")
            # 计算出当前文件的相对路径，压缩文件中将多层文件夹也打包进去了
            relative_path = os.path.relpath(os.path.join(root, filename), directory_path)
            # apk文件路径
            apk_file_path = os.path.join(root, filename)
            # 使用相对路径添加文件到压缩包中
            _zipfile.write(apk_file_path, relative_path)

            # 判断是否在压缩后自动删除源文件
            if option.zip_with_del:
                os.remove(apk_file_path)
    _zipfile.close()
    os.rename(tmp_zip_file, zip_file_path)
    print(f"压缩完成，文件存放在：{zip_file_path}")
    return zip_file_path


def get_filename(filepath: str) -> str:
    """
    从文件路径中解析文件名称
        前提是提供一个正常的以 / 分隔的文件路径

    :param filepath:
    :return:
    """
    try:
        filepath = filepath.replace(os.path.sep, '/')
        return filepath.split('/')[-1].split('.')[0]
    except:
        return ''


def execute_cmd(cmd) -> (str, str):
    """
    python执行cmd命令

    :param cmd:
    :return:
    """
    print(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.communicate()


def get_project_root_path():
    """
    获取项目根目录
    :return:
    """
    _path = os.path.dirname(os.path.abspath(__file__))
    _path = os.path.dirname(_path)
    return os.path.relpath(_path)


if __name__ == "__main__":
    pass
