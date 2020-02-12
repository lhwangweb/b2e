# Django
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, validate_ipv46_address
import logging
logger = logging.getLogger(__name__)

# Proj
from home.models import Urldata, Urllog
from home.forms import UrlForm

# Others
import random
import html

def home(request):
    """
    首頁 - 同時也是入口頁
    """
    return render(request, 'home.html')


@require_http_methods(["POST"])
def create(request):
    """
    新增縮址的 API
    """
    response_data = {
        "status": 0,
        "message": "",
        "data": []
    }

    form = UrlForm(request.POST)
    if form.is_valid():
        try:
            # transaction
            with transaction.atomic():

                # 先儲存
                new_url = form.save()

                # === 產生 縮址 hash ===
                # 0. 長度 62 的字串樣本，內容是 0-9a-zA-Z shuffle 過
                population = 'Tr3JhSlcZE8Fw4XHxGAWiepotRqU7YusLadbD1g65PKV9mCnvNz2Oj0IMQyBkf'
                population2 = 'pX52BRaoEn0j3ksTVDzOqeby6fuxrUt4iQmAL7hClKJSWc9F8G1vNdwgHMIYPZ'

                # 1. 加上一個常數 (方便起見 > 62)
                serial_no = new_url.id + 193

                # 2. 62 進位轉換，只是字串用 population，而非 0-9a-zA-Z ()
                url_hash = ''
                while serial_no != 0:
                    serial_no, i = divmod(serial_no, 62)
                    url_hash = population[i] + url_hash
                # 3. 得到縮址字串
                #    (1) 因跟 id 一起變大，故也不會產生出重複的 hash
                #    (2) 由於 population 本身不是依序，所以要從大量結果反推，比較不那麼直白好推
                #    (3) 試算： 10 進位 4294967294 ~= hKPHw3，長度約 6 字而已，換言之 row limit 會先頂到，而非 hash 長度上限先頂到

                # 4. 加上 2 個隨機英數字元，稍微增加反推難度
                rand_num1 = random.randint(0, 61)
                rand_num2 = random.randint(0, 61)
                url_hash = population2[rand_num2] + \
                    url_hash + population2[rand_num1]

                if len(url_hash) > 12:
                    # url_hash 欄位長度為 12，雖然理論上不可能達到
                    raise Exception("抱歉！ 本縮址系統已達設計的資料上限，暫時無法繼續為您服務！")
                # === 產生 縮址 hash ===

                # 回存 hash
                new_url.url_hash = url_hash
                new_url.save()
                # raise Exception("Test Transaction")

                # response data
                response_data["status"] = 1
                response_data["message"] = "SUCCESS"
                response_data["hash"] = url_hash

        except Exception as e:
            logger.error('[home][create] 新增縮址資料錯誤')
            logger.error(str(e))
            response_data["status"] = -1
            response_data["message"] = "新增失敗，伺服器發生錯誤 " + str(e) 
            response_data["errors"] = { "fail":str(e) }
    else:
        # 資料驗證先不 log 怕太吵
        # logger.warning('[home][create] 新增縮址資料錯誤')
        # logger.warning(str(form.errors))
        response_data["status"] = -1
        response_data["message"] = "新增失敗，資料格式錯誤"
        response_data["errors"] = form.errors

    return JsonResponse(response_data)


def result(request, url_hash):
    """
    新增縮址結果頁
    """
    urldata = Urldata.objects.filter(url_hash=url_hash).first()

    if urldata is None:
        # 沒結果就導向首頁
        logger.warning('[home][url_handler] Urldata 找不到 url_hash: ' + url_hash)
        return redirect('/')
    
    # 輸出 HTML
    temp_data = {
        "url_hash": url_hash,
        "original_url": urldata.original_url,
        "short_url": request.scheme + "://" + request.get_host() + "/go/" + url_hash
    }

    return render(request, 'result.html', temp_data)


def url_handler(request, url_hash):
    """
    存取縮址 - 如果有效導向目標，無效或失敗導向首頁
    """
    urldata = Urldata.objects.filter(url_hash=url_hash).first()

    if urldata is None:
        # 沒結果就導向首頁
        logger.warning('[home][url_handler] Urldata 找不到 url_hash: ' + url_hash)
        return redirect('/')
    
    try:
        user_agent = get_agent(request)
        ip = get_ip(request)
        log = Urllog.objects.create(urldata=urldata, ip=ip, agent=user_agent)
        log.save()
    except Exception as e:
        logger.error('[home][url_handler] 紀錄 urllog 出錯 錯誤')
        logger.error(str(e))

    try:
        original_url = urldata.original_url if urldata.original_url else ''
        u_validate = URLValidator(schemes=("http", "https"))
        res = u_validate(original_url)
        print(res)
        return redirect(original_url)
    except ValidationError as ve:
        # 錯誤 - 導向首頁
        logger.error('[home][url_handler] Urldata.original_url 格式錯誤，不予導向')
        logger.error(str(ve))
        return redirect('/')
    except Exception as e:
        logger.error('[home][url_handler] 導向出錯')
        logger.error(str(e))
        # 錯誤 - 導向首頁
        return redirect('/')

def get_agent(req):
    """
    取得 User Agent - 順便做 HTML 轉譯(簡單多一道防注入)以及限制長度
    """
    user_agent = html.escape(
        req.META.get(
            'HTTP_USER_AGENT', 
            'Unknown Agent'
        )
    )
    user_agent = user_agent if len(user_agent) <= 1024 else user_agent[0:1020] + "..."
    return user_agent

def get_ip(req):
    """
    取得 IP - 包含驗證與不合法備註的處理
    """
    ip = ""
    x_forward = req.META.get('HTTP_X_FORWARDED_FOR', '')

    if x_forward:
        ip = x_forward.split(',')[0]
    else:
        ip = req.META.get('REMOTE_ADDR', '')
    
    if ip:
        try:
            validate_ipv46_address(ip)
        except ValidationError as ve:
            logger.error('[home][get_ip] 偵測到不合法IP。 IP: ' + ip)
            logger.error(str(ve))
            ip = "[Invalid IP][IP Save Into Log]"
        except Exception as e:
            logger.error('[home][get_ip] 偵測IP出錯。 IP: ' + ip)
            logger.error(str(e))
            ip = "[Valid IP Exception Occur][IP Save Into Log]"
    else:
        ip = "[Empty IP]"

    return ip
