# 使用官方的 Python 运行时镜像作为基础镜像
FROM python:3.6-slim

# 设置时区
ENV TZ=Asia/Shanghai
RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone


# 设置工作目录
WORKDIR /app

# 复制当前目录下的所有文件到工作目录
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 6767

# 运行应用
CMD ["python", "Zcmu_Score.py"]