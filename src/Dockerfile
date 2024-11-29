# 使用官方 Python 3.9 作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 将当前目录内容复制到容器的 /app 目录
COPY . /app/

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量
ENV PYTHONUNBUFFERED 1

# 如果是运行 web 服务器，可以暴露端口 8000（例如 FastAPI 应用）
EXPOSE 8000

# 设置容器启动时运行的命令
CMD ["python", "src/main.py"]
