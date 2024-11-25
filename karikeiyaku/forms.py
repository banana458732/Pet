from django import forms
from .models import Karikeiyaku
from datetime import date, timedelta

class KarikeiyakuForm(forms.ModelForm):
    agreement = forms.BooleanField(
        required=True, 
        label="上記について同意します",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})  # 見た目を整える
    )

    class Meta:
        model = Karikeiyaku
        fields = ['end_date']  # end_date のみ保存対象

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ページを開いた日を元に二週間後の日付を設定
        self.fields['end_date'].initial = date.today() + timedelta(weeks=2)
        self.fields['end_date'].widget.attrs['readonly'] = 'readonly'
