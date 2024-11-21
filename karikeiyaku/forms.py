from django import forms
from .models import Karikeiyaku

class KarikeiyakuForm(forms.ModelForm):
    class Meta:
        model = Karikeiyaku
        fields = ['price', 'end_date', 'has_appropriate_space', 'understands_responsibility', 'status', 'cancellation_policy']

    # 病歴を表示
    disease = forms.CharField(widget=forms.Textarea(attrs={'readonly': 'readonly'}), required=False)

    # 同意チェックボックスを追加
    agreement = forms.BooleanField(required=True, label="上記の仮契約内容を確認し、同意します。")
