# b2e

## 部署與啟動步驟

1. 前置確認
   - 確保機器上已安裝 Docker, Docker-Compose 並執行中
   - 確保機器上 Port 3306, 80 沒有服務佔用中

2. 取得專案
以下假設您 clone 到 /Path/To/Projects

```bash
user$ cd /Path/To/Projects
user$ git clone https://github.com/lhwangweb/b2e.git
```

3. 以下用 b2e.com 作為範例測試網址，請編輯以下地方，確保您的測試網址可用：

    (1) /Path/To/Projects/b2e/default_nginx L9

    ```bash
    # 請修改為您的 FQDN
    server_name b2e.com;
    ```

    (2) /Path/To/Projects/b2e/b2e/b2e/settings.py L29

    ```bash
    # 請增加允許的 FQDN
    ALLOWED_HOSTS = ['b2e.com']
    ```

    (3) 此外，您可能需要編輯您本機 /etc/hosts (mac, linux) 或 C:\WINDOWS\system32\drivers\etc\hosts

    ```bash
    127.0.0.1 b2e.com
    ```

2. 執行 docker-compose

```bash
user$ cd /Path/To/Projects/
user$ git clone https://github.com/lhwangweb/b2e.git
user$ cd /Path/To/Projects/b2e
user$ docker-compose up -d
 ...
 詳細過程略
 ...
Successfully tagged b2e_b2e:latest
WARNING: Image for service b2e was built because it did not already exist. To rebuild this image you must use `docker-compose build` or `docker-compose up --build`.
mysql57_instance is up-to-date
Creating b2e_instance ... done
```

3. 查看啟動中的 Container

```bash
$ docker-compose ps
      Name                    Command               State                 Ports              
---------------------------------------------------------------------------------------------
b2e_instance       uwsgi --ini /var/www/b2e/d ...   Up      0.0.0.0:80->80/tcp
mysql57_instance   docker-entrypoint.sh mysql ...   Up      0.0.0.0:3306->3306/tcp, 33060/tcp
```

4. 執行 NGINX RESTART

```bash
user$ docker exec -it b2e_instance service nginx restart
```

附註： 目前還沒有研究成功如何完美的 docker start 就把服務全部啟動完成 ( entrypoint 與 start.sh 之類的方式還在試驗中)，因此先提供此較笨步驟，手動 restart service

5. 訪問首頁 http://b2e.com

## 測試步驟

1. 連結前台首頁 http://b2e.com

2. 輸入一個欲縮短的網址並按下『儲存』

3. 成功後，導向結果，嘗試點擊該網址，將會 redirect 到原本輸入的網址

4. 連結後台 http://b2e.com/admin
    - 帳密 b2e_admin / c696b04ea  (管理者，具有一切權限，可看縮址資料以及日誌，可編輯)
    - 帳密 b2e_sales / e07c48895262  (業務，假設只能看縮址資料，達成方式為 Django 預設後台)

## 程式規劃
1. 使用 Docker 封裝 2 包執行環境

    (1) Ubuntu 18.04 ( Python 3.6 + Django 3.0.3 + uWSGI + Nginx)

    (2) MySQL 5.7 - pull 現成 image

2. 因為都封裝為一包環境了，也沒有多組環境的需求，所以就不裝 Virtualenv 環境了

3. 有簡單的使用日誌可供查詢紀錄

4. 有簡單的 File Log


