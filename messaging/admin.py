from django.contrib import admin
from .models import Pet, Shelter, PetImage


class PetImageInline(admin.TabularInline):
    model = PetImage
    extra = 1  # 新しい画像を追加するための空のフォームの数を指定


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('age', 'size', 'color', 'inuneko', 'syu',
                    'disease', 'personality', 'shelter')
    inlines = [PetImageInline]  # PetImageのインラインを追加


@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'shelter_type')
