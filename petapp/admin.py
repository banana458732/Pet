from django.contrib import admin
from .models import Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'size', 'color', 'age',
                    'kinds', 'disease', 'personality', 'sex',
                    )
    search_fields = ('type', 'size', 'color', 'age')  # 検索機能を追加
