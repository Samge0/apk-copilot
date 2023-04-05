## ApkCopilot 多渠道打包&签名 
一个简易的ApkCopilot 多渠道打包&签名 + gradio操作界面。

### 版本信息
- java：`java version "17.0.4.1" 2022-08-18 LTS`
- python：`Python 3.10.10`
- build-tools：`31.0.0`

### docker方式运行
备注：目前暂且在本地运行，需要自行配置java、python、安卓的build-tools环境，后续有时间再改为docker运行模式；
[点击这里查看docker说明](docker/README.md)


### 本地源码运行

- 安装依赖
先按`版本信息`配置本地环境，然后创建python的env环境，安装python依赖：
```shell
pip install -r requirements.txt
```

- 复制配置
```shell
cp config.dev.json config.json
```
```shell
cp -R 本地路径xxx/build-tools/31.0.0 res/build-tools/31.0.0
```

- 运行
> gradio界面
```shell
uvicorn app:app --reload --host 0.0.0.0 --port 7860
```
