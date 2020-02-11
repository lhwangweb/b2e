# b2e


## 安裝與啟動步驟

```bash
user$ docker image build -t py/dj:1.0 /Path/To/b2e/
user$ docker run -itd -p 80:8000 -v /Path/To/b2e/:/var/www/b2e --name b2e py/dj:1.0
user$ docker exec -it b2e bash
```