from django import forms
from .models import Karikeiyaku
from datetime import date, timedelta

class KarikeiyakuForm(forms.ModelForm):
    agreement = forms.BooleanField(
        required=True, 
        label="上記について同意します",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Karikeiyaku
        fields = ['end_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 新規作成時のみ、end_dateを2週間後に設定
        if not self.instance.pk:
            self.fields['end_date'].initial = date.today() + timedelta(weeks=2)

        self.fields['end_date'].widget = forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'readonly': 'readonly',
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD'
            }
        )
