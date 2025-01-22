from django.contrib import admin
from .models import CustomUser

class CustiomUserAdmin(admin.ModelAdmin):
    '''管理ページのレコード一覧に表示するカラムを設定するクラス（※任意）
    '''
    list_display = ('id', 'username') # レコード一覧にid, usernameカラムを表示
    list_display_links = ('id', 'username') # list_displayに指定したカラムにリンクを表示
    exclude = ("first_name","last_name" ,"groups")


admin.site.register(CustomUser, CustiomUserAdmin)