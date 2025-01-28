from django import forms


class SimplePetSurveyForm(forms.Form):
    # ペットの種類
    TYPE_CHOICES = [
        ('犬', '犬'),
        ('猫', '猫'),
    ]
    pet_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        label="ペットの種類",
        error_messages={'required': 'ペットの種類を選択してください。'},
    )

    # ペットのサイズ
    SIZE_CHOICES = [
        ('小型', '小型'),
        ('中型', '中型'),
        ('大型', '大型'),
    ]
    size = forms.ChoiceField(
        choices=SIZE_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label="ペットのサイズ"
    )

    # 色
    color = forms.CharField(
        max_length=100,
        required=False,
        label="色",
        widget=forms.TextInput(attrs={'placeholder': '例: 白, 黒, 茶色'})
    )

    # 種別
    kinds = forms.CharField(
        max_length=100,
        required=False,
        label="種別",
        widget=forms.TextInput(attrs={'placeholder': '例: ゴールデンレトリバー, シャム猫'})
    )

    # 性格
    pet_personality = forms.CharField(
        max_length=500,
        required=False,
        label="性格",
        widget=forms.TextInput(attrs={'rows': 5, 'cols': 50}),
    )

    # 性別
    SEX_CHOICES = [
        ('オス', 'オス'),
        ('メス', 'メス'),
    ]
    sex = forms.ChoiceField(
        choices=SEX_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label="性別"
    )

    # 年齢の範囲（チェックボックス選択）
    AGE_CHOICES = [
        ('0-3', '0~3歳'),
        ('4-7', '4~7歳'),
        ('8-10', '8~10歳'),
    ]
    age_range = forms.ChoiceField(
        choices=AGE_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label="年齢の範囲"
    )
