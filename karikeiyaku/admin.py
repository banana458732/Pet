from django.contrib import admin
from .models import Karikeiyaku

@admin.register(Karikeiyaku)
class KarikeiyakuAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'created_at')  # 必要なフィールドを表示
    search_fields = ('user__username', 'pet__name')  # 検索を有効化
