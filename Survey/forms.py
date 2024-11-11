from django import forms


class SimplePetSurveyForm(forms.Form):
    # 新しく追加したペットの種類を選択するフィールド
    pet_type = forms.ChoiceField(
        choices=[('dog', '犬'), ('cat', '猫')],
        widget=forms.RadioSelect,
        label='ペットの種類を選んでください',
        required=True
    )

    # ユーザーの生活環境を入力するフィールド
    living_environment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        label='あなたの生活環境について教えてください（例: 都市部、広い家、アパートなど）',
        required=True  # 必須項目
    )

    # ユーザーが希望するペットの性格を入力するフィールド
    pet_personality = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        label='どんな性格のペットをお望みですか？（例: おとなしい、活発、社交的など）',
        required=True  # 必須項目
    )

    # ユーザーが希望するペットの活動量を入力するフィールド
    activity_level = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        label='ペットの活動量について教えてください（例: 毎日散歩が必要、家の中で遊べるなど）',
        required=True  # 必須項目
    )

    # ユーザーがペットに対して希望するサイズを入力するフィールド
    pet_size_preference = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        label='ペットのサイズについて教えてください（例: 小型犬、中型猫など）',
        required=True  # 必須項目
    )
