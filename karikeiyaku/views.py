from django.shortcuts import render, redirect, get_object_or_404
from petapp.models import Pet
from .models import Karikeiyaku
from .forms import KarikeiyakuForm


# 仮契約フォーム
def karikeiyaku_form(request, pet_id):
    pet = Pet.objects.get(id=pet_id)

    if request.method == 'POST':
        # 仮契約フォームに同意したらデータを保存
        form = KarikeiyakuForm(request.POST)
        if form.is_valid():
            karikeiyaku = form.save(commit=False)
            karikeiyaku.pet = pet
            karikeiyaku.user = request.user
            karikeiyaku.status = "仮契約中"  # 仮契約中のステータスを設定
            karikeiyaku.save()

            return redirect('karikeiyaku:complete')  # 仮契約完了ページにリダイレクト
    else:
        form = KarikeiyakuForm(initial={'pet': pet})

    return render(request, 'karikeiyaku/karikeiyaku_form.html', {'form': form, 'pet': pet})

# キャンセル
def karikeiyaku_cancel(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    karikeiyaku = Karikeiyaku.objects.get(pet=pet, user=request.user)

    if request.method == 'POST':
        # ユーザーがキャンセルを確認した場合、仮契約を削除
        karikeiyaku.delete()
        return HttpResponse("仮契約がキャンセルされました。")  # 適切なメッセージを表示

    return redirect('karikeiyaku:form', pet_id=pet.id)


# 仮契約完了ページ
def karikeiyaku_comp(request):
    return render(request, 'karikeiyaku/karikeiyaku_comp.html')


# 再仮契約キャンセル表示
def karikeiyaku_form_second(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    karikeiyaku = Karikeiyaku.objects.get(pet=pet, user=request.user)

    if karikeiyaku.status == "仮契約中":
        return render(request, 'karikeiyaku/karikeiyaku_form_second.html', {'karikeiyaku': karikeiyaku})
    else:
        # 既にキャンセルされている場合
        return redirect('karikeiyaku:cancel', pet_id=pet.id)  # キャンセルページにリダイレクト
