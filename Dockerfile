FROM ubuntu:18.04
# 更新套件 url 為國網
RUN sed -i 's/archive.ubuntu.com/free.nchc.org.tw/g' /etc/apt/sources.list

# 安裝必要套件
RUN apt-get update && apt install -y build-essential

# 工作目錄
RUN mkdir -p /var/www/b2e
WORKDIR /var/www/b2e

# pip 安裝與升級
# COPY requirements.txt /var/www/b2e/requirements.txt
# RUN python3 -m pip install --upgrade pip && pip install -r requirements.txt

# 啟動 Django
