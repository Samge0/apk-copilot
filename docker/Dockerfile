# 设置基础镜像
FROM samge/apk-copilot:base

# 将工作目录设置为 /app
WORKDIR /app

# 复制当前目录中的所有文件到 /app
COPY . .

# 安装所需的 Python 包
RUN java -version && pip install --no-cache-dir -r requirements.txt

# 声明容器监听的端口
EXPOSE 7860

# 目录映射
VOLUME /app/user_configs

# 运行应用程序
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 7860"]
