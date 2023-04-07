## ApkCopilot的api-docker镜像
一个ApkCopilot的api-docker镜像

### 构建api正式包
```shell
docker build . -t samge/apk-copilot -f docker/Dockerfile
```

### 上传
```shell
docker push samge/apk-copilot
```

### 运行docker镜像
- 方式1：使用环境变量配置登录用户信息
```shell
docker run -d \
--name apk-copilot \
-p 7860:7860 \
-e APK_COPILOT_AUTH="user1:pw1|user2:pw2" \
--pull=always \
--restart always \
--memory=1.0G \
samge/apk-copilot:latest
```

- 方式2：使用配置文件配置登录用户信息
```shell
COPY config.dev.json ~/config.json
```
```shell
docker run -d \
--name apk-copilot \
-p 7860:7860 \
-v ~/config.json:/app/config.json \
--pull=always \
--restart always \
--memory=1.0G \
samge/apk-copilot:latest
```