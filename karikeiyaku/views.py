from django.shortcuts import render, redirect, get_object_or_404
from petapp.models import Pet
from .models import Karikeiyaku
from .forms import KarikeiyakuForm
from datetime import date, timedelta

# 仮契約フォーム
def karikeiyaku_form(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        form = KarikeiyakuForm(request.POST)
        if form.is_valid():
            karikeiyaku = form.save(commit=False)
            karikeiyaku.pet = pet
            karikeiyaku.user = request.user
            karikeiyaku.status = "仮契約中"  # 仮契約中の状態を設定
            karikeiyaku.end_date = date.today() + timedelta(weeks=2)  # 契約終了日を設定
            karikeiyaku.save()
            return redirect('karikeiyaku:complete')  # 仮契約完了ページにリダイレクト
    else:
        form = KarikeiyakuForm()

    return render(request, 'karikeiyaku/karikeiyaku_form.html', {'form': form, 'pet': pet})


# キャンセル
def karikeiyaku_cancel(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    karikeiyaku = get_object_or_404(Karikeiyaku, pet=pet, user=request.user)

    if request.method == 'POST':
        # 仮契約を削除
        karikeiyaku.delete()
        return redirect('pet_detail', pet_id=pet.id)  # ペット詳細ページにリダイレクト

    return render(request, 'karikeiyaku/karikeiyaku_cancel.html', {'pet': pet})

# 仮契約完了ページ
def karikeiyaku_comp(request):
    return render(request, 'karikeiyaku/karikeiyaku_comp.html')


# 再仮契約キャンセル表示
def karikeiyaku_form_second(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    karikeiyaku = get_object_or_404(Karikeiyaku, pet=pet, user=request.user)

    return render(request, 'karikeiyaku/karikeiyaku_form_second.html', {'karikeiyaku': karikeiyaku})
