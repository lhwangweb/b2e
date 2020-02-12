# B2E 實作 - 縮址產生器

## 部署與啟動步驟

1. 前置確認

   - 確保機器上已安裝 Docker, Docker-Compose ，且 Docker 執行中
   - 確保機器上 Port 3306, 80 沒有服務佔用中

2. 取得專案 Code

   - 以下假設您 clone 到 /Path/To/Projects

   ```bash
   user$ cd /Path/To/Projects
   user$ git clone https://github.com/lhwangweb/b2e.git
   ```

3. 執行安裝前，請編輯以下 3 個地方，確保您的測試網址可用：

   以下用 b2e.com 作為範例測試網址

   (1) /Path/To/Projects/b2e/default_nginx  約 L9

   ```bash
   # 請修改為您的 FQDN
   server_name b2e.com;
   ```

   (2) /Path/To/Projects/b2e/b2e/b2e/settings.py 約 L29

   ```bash
   # 請增加允許的 FQDN
   ALLOWED_HOSTS = ['b2e.com']
   ```

   (3) 此外，如果您是在本機進行部署安裝，請編輯 /etc/hosts (mac, linux) 或 C:\WINDOWS\system32\drivers\etc\hosts  (Windows) ，新增以下這行，以獲得正確 DNS 解析。

   ```bash
   127.0.0.1 b2e.com
   ```

4. 執行 docker-compose up -d 

   ```bash
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
   
5. 查看啟動中的 Container

   ```bash
   user$ docker-compose ps
      Name                    Command               State                 Ports           
   ---------------------------------------------------------------------------------------
   b2e_instance       uwsgi --ini /var/www/b2e/d ...   Up      0.0.0.0:80->80/tcp
   mysql57_instance   docker-entrypoint.sh mysql ...   Up      0.0.0.0:3306->3306/tcp
   ```

6. 執行 Nginx Service Restart

   ```bash
   user$ docker exec -it b2e_instance service nginx restart
   ```

   附註： 目前完美的全自動啟動還沒研究成功，因此先提供此較笨步驟 - 手動 restart service

7. 訪問首頁 http://b2e.com ，並可依下節測試步驟進行測試。

## 測試步驟

### 測試前台

1. 連結前台首頁 http://b2e.com

2. 輸入一個欲縮短的網址並按下『儲存』

3. 成功後，導向結果，嘗試點擊該網址，將會 redirect 到原本輸入的網址

### 測試後台

4. 連結後台 http://b2e.com/admin

   - 帳密 b2e_admin / c696b04ea  (管理者，具有一切權限，可看縮址資料以及日誌，可編輯)
   
   - 帳密 b2e_sales / e07c48895262  (業務，假設只能看縮址資料，達成方式為 Django 預設後台)

## 程式規劃與討論

1. 架構
  
   規劃兩台主機： Ubuntu 與 MySQL 各一台：

   (1) Ubuntu 18.04 (Python 3.6 + Django 3.0.3 + uWSGI + Nginx)

      - uWSGI ON 在 8001 port

      - Nginx 跑在 80 port，動態請求轉給 uWSGI，靜態資源由 Nginx 直接提供，例如 /static/* 
   
   (2) MySQL 5.7 - pull 現成 image 來做，並使用一些環境變數，快速建好基本帳號

2. 部署

   - 使用 Docker 分別封裝上述兩台主機

   - 因為都封裝 Docker 了，也沒有多組環境的需求，所以就不裝 Virtualenv 環境了

3. 幾個比較重大的功能：

   (1) 簡單的日誌可供查詢 redirect 紀錄 (限管理者)

   (2) 有簡單的 File Log (限伺服器管理員可見，位置在 /Path/To/Projects/b2e/b2e.log )

   (3) 用 Django 原生 Admin 建立後台，並使用預設權限系統規劃出簡單的『管理者』、『業務』帳號

4. 縮址演算討論

   - 縮址的演算，精神是拿 primary key 做 62 進位：
   
      (1) 先存 DB，取得 record primary key

      (2) primary key 加一個常數 193

      (3) 做 62 進位轉換，只是換算的字串 shuffle 過，不是依序 0-9 a-z A-Z

      (4) 最後加兩碼隨機碼

      (5) 以上過程有包 DB transaction，如果出錯，會 rollback record

   - 穿插各種動作，增加反推規則的難度。
   
   - 可參考 /Path/To/Projects/b2e/home/views.py 約 L27， def create()

## sqlmap 掃描

   1. 導向功能
   ```bash
   python /Users/hank/sqlmap-dev/sqlmap.py -u "http://b2e.com/go/a1*" --method=GET --tamper=space2comment  --random-agent --level=5 --risk=3 --tables --time-sec=30 --dbms=mysql --batch

   [WARNING] URI parameter '#1*' does not seem to be injectable
   ```

   2. 新增縮址 (先關閉CSRF再測)
   ```bash
   python /Users/hank/sqlmap-dev/sqlmap.py -u "http://b2e.com/url/create" --method=POST --data="original_url=http://haha.cc" --tamper=space2comment  --random-agent --level=5 --risk=3 --tables --time-sec=30 --dbms=mysql --batch

   [WARNING] POST parameter 'original_url' does not seem to be injectable
   ```

   3. 縮址結果頁
   ```bash
   python /Users/hank/sqlmap-dev/sqlmap.py -u "http://b2e.com/url/result/a1*" --method=GET --tamper=space2comment  --random-agent --level=5 --risk=3 --tables --time-sec=30 --dbms=mysql --batch
   
   [WARNING] URI parameter '#1*' does not seem to be injectable
   ```
## LICENSE

本程式以 Django 建構，LICENSE 遵循 Django  的 3-clause BSD


