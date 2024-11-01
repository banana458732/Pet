# from django import forms
# from .models import Pet

# class PetForm(forms.ModelForm):
#     class Meta:
#         model = Pet
#         fields = ['name', 'breed', 'age', 'description', 'is_adopted']

# petapp/forms.py
from django import forms
from .models import Pet

class PetCreateForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['id', 'type', 'size', 'color', 'age', 'image']

class PetUpdateForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['type', 'size', 'color', 'age', 'image']  # IDは除外

      # IDの重複をチェックするバリデーション
    def clean_id(self):
        id = self.cleaned_data.get('id')
        # 現在のオブジェクトのIDを取得（もし存在する場合）
        current_id = self.instance.id

        if id and current_id and id != current_id:
            # 新しいIDがすでに存在する場合
            if Pet.objects.filter(id=id).exists():
                raise forms.ValidationError("このIDはすでに登録されています。別のIDを入力してください。")
        
        return id

    TYPE_CHOICES = [
        ('dog', '犬'),
        ('cat', '猫'),
    ]
    
    SIZE_CHOICES = [
        ('large', '大型'),
        ('medium', '中型'),
        ('small', '小型'),
    ]
    
    AGE_CHOICES = [(i, f'{i}歳') for i in range(21)]  # 0歳から20歳までのドロップダウン

    id = forms.IntegerField(widget=forms.NumberInput(), label='ID')  # 数字専用のIDフィールド
    type = forms.ChoiceField(choices=TYPE_CHOICES, label='種類')
    size = forms.ChoiceField(choices=SIZE_CHOICES, label='サイズ')
    color = forms.CharField(max_length=100, label='毛の色')
    age = forms.ChoiceField(choices=AGE_CHOICES, label='年齢')
