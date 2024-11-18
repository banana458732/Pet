from django import forms


class SimplePetSurveyForm(forms.Form):
    # 全ての情報を一つのフィールドに集約した自由入力フィールド
    general_info = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}),
        required=True
    )

    AGE_CHOICES = [
        ('0-3', '0~3歳'),
        ('4-7', '4~7歳'),
        ('8-10', '8~10歳')
    ]

    age_range = forms.MultipleChoiceField(
        choices=AGE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
