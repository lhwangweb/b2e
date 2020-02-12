from django.contrib import admin
from home.models import Urldata, Urllog

# admin.site.register(Urldata)
# admin.site.register(Urllog)

# Define the admin class
class UrldataAdmin(admin.ModelAdmin):
    # 列表檢視
    list_display = ('id', 'url_hash', 'short_url', 'original_url',  'created_at')
    list_filter = ('created_at',)
    
    # 全部僅供檢視
    # fields = []
    readonly_fields = ('url_hash', 'short_url', 'original_url','created_at', 'updated_at')

admin.site.register(Urldata, UrldataAdmin)

class UrllogAdmin(admin.ModelAdmin):
    # 列表檢視
    list_display = ('id', 'urldata', 'ip', 'created_at')
    list_filter = ('created_at',)

    # 全部僅供檢視
    # fields = []
    readonly_fields=('urldata', 'ip', 'agent', 'created_at', 'updated_at')

admin.site.register(Urllog, UrllogAdmin)