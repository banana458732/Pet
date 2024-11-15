from django import forms


class SimplePetSurveyForm(forms.Form):
    # 全ての情報を一つのフィールドに集約した自由入力フィールド
    general_info = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}),
        label='求めているペットについて自由にご記入ください。',
        help_text='（例: ペットの種類、性格、性別など)',
        required=True  # 必須項目
    )

    # 年齢の範囲を指定するチェックボックスフィールド
    AGE_CHOICES = [
        ('0-3', '0~3歳'),
        ('4-7', '4~7歳'),
        ('8-10', '8~10歳')
    ]

    age_range = forms.MultipleChoiceField(
        choices=AGE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='希望するペットの年齢範囲(任意)',
        required=False  # 必須ではない
    )
