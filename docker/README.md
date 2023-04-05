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
```shell
docker run -d \
--name apk-copilot \
-p 7860:7860 \
--pull=always \
--restart always \
--memory=1.0G \
samge/apk-copilot:latest
```