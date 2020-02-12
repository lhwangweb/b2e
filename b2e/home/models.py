from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

class Urldata(models.Model):
    """
    縮址資料主表
    """
    # 原本的url
    original_url = models.CharField(max_length=1023, verbose_name="原 Url")
    # 縮址 hash
    url_hash = models.CharField(
        max_length=12, unique=True, verbose_name="Hash 碼")
    # 時間
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    # 時間
    updated_at = models.DateTimeField(auto_now=True, verbose_name="變更時間")

    def __str__(self):
        return self.url_hash

    # 自訂顯示資料 - 縮址
    def short_url(self):
        return "/go/" + self.url_hash
    short_url.short_description = u'縮址'

    class Meta:
        verbose_name = "縮址資料"
        verbose_name_plural = "縮址資料"


class Urllog(models.Model):
    """
    縮址使用日誌
    """
    # FK to Urldata
    urldata = models.ForeignKey('Urldata', on_delete=models.PROTECT, related_name='url_items', verbose_name="對應縮址")
    # User IP
    ip = models.CharField(max_length=130, verbose_name="IP")
    # User-Agent
    agent = models.CharField(max_length=1024, verbose_name="User Agent")
    # 時間
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    # 時間
    updated_at = models.DateTimeField(auto_now=True, verbose_name="變更時間")

    def __str__(self):
        return "Log No." + str(self.id)

    class Meta:
        verbose_name = "縮址使用日誌"
        verbose_name_plural = "縮址使用日誌"
