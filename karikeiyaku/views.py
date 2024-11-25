from django.shortcuts import render, redirect, get_object_or_404
from petapp.models import Pet
from .models import Karikeiyaku
from .forms import KarikeiyakuForm
from datetime import date, timedelta


# 仮契約
def karikeiyaku_form(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    user_karikeiyaku = Karikeiyaku.objects.filter(user=request.user, pet=pet, status="仮契約中").first()

    if request.method == 'POST' and not user_karikeiyaku:
        form = KarikeiyakuForm(request.POST)
        if form.is_valid():
            karikeiyaku = form.save(commit=False)
            karikeiyaku.pet = pet
            karikeiyaku.user = request.user
            karikeiyaku.status = "仮契約中"
            karikeiyaku.end_date = form.cleaned_data['end_date']
            karikeiyaku.save()
            return redirect('karikeiyaku:complete')
    else:
        form = KarikeiyakuForm()

    # 日付をYYYY-MM-DD形式でテンプレートに渡す
    end_date = form.fields['end_date'].initial.strftime('%Y-%m-%d')

    return render(request, 'karikeiyaku/karikeiyaku_form.html', {
        'form': form,
        'pet': pet,
        'end_date': end_date,
        'user_karikeiyaku': user_karikeiyaku,
    })


# キャンセル
def karikeiyaku_cancel(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    karikeiyaku = get_object_or_404(Karikeiyaku, pet=pet, user=request.user)

    if request.method == 'POST':
        # 仮契約を削除
        karikeiyaku.delete()
        return redirect('messaging:pet_detail', pet_id=pet.id)  # ペット詳細ページにリダイレクト

    return render(request, 'karikeiyaku/karikeiyaku_cancel.html', {'pet': pet})


# 仮契約完了ページ
def karikeiyaku_comp(request):
    return render(request, 'karikeiyaku/karikeiyaku_comp.html')