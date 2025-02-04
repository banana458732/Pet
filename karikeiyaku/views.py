from django.shortcuts import render, redirect, get_object_or_404
from petapp.models import Pet, PetImage
from .models import Karikeiyaku
from .forms import KarikeiyakuForm
from datetime import date, timedelta
from django.contrib import messages
from django.urls import reverse


def karikeiyaku_form(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    # ユーザーが現在契約中のペットを取得
    user_karikeiyaku = Karikeiyaku.objects.filter(user=request.user, pet=pet, status="仮契約中").first()

    # 他のユーザーが仮契約しているかをチェック
    other_user_karikeiyaku = Karikeiyaku.objects.filter(pet=pet).exclude(user=request.user).first()

    # 仮契約中のペット数をカウント
    current_karikeiyaku_count = Karikeiyaku.objects.filter(user=request.user, status="仮契約中").count()

    # 仮契約が3匹以上の場合、契約できない
    can_contract = current_karikeiyaku_count < 3 or user_karikeiyaku is not None

    # 病気の除外リスト
    exclusion_list = [
        "なし", "無し", "無い", "ない", "無", "ありません", "無いです", "ないです",
        "存在しない", "不明", "特にない", "特にありません", "特に無い",
        "特に不明", "特になし", "特に無し", "特にないです"
    ]

    # pet.diseaseが除外リストに含まれていない場合に表示する
    show_disease = pet.disease and pet.disease not in exclusion_list

    # ペット画像を取得
    pet_images = PetImage.objects.filter(pet=pet)

    # formをPOST外で初期化
    form = KarikeiyakuForm(request.POST or None)

    if request.method == 'POST' and not user_karikeiyaku:
        # 仮契約が3匹を超える場合は契約を許可しない
        if current_karikeiyaku_count >= 3:
            messages.error(request, "仮契約中のペットは3匹までです。")
        else:
            if form.is_valid():
                karikeiyaku = form.save(commit=False)
                karikeiyaku.pet = pet
                karikeiyaku.user = request.user
                karikeiyaku.status = "仮契約中"
                # end_dateが空の場合、2週間後の日付を設定
                if not karikeiyaku.end_date:
                    karikeiyaku.end_date = date.today() + timedelta(weeks=2)
                karikeiyaku.save()
                return redirect('karikeiyaku:complete')

    # end_dateをYYYY-MM-DD形式でテンプレートに渡す
    end_date = form.fields['end_date'].initial.strftime('%Y-%m-%d') if form.fields['end_date'].initial else None

    # コンテキストにcan_contractとother_user_karikeiyakuを追加
    return render(request, 'karikeiyaku/karikeiyaku_form.html', {
        'form': form,
        'pet': pet,
        'end_date': end_date,
        'user_karikeiyaku': user_karikeiyaku,
        'show_disease': show_disease,  # 病気情報を表示するかどうか
        'pet_images': pet_images,  # pet_imagesを渡す
        'current_karikeiyaku_count': current_karikeiyaku_count,  # 仮契約数をテンプレートに渡す
        'can_contract': can_contract,  # can_contractを渡す
        'other_user_karikeiyaku': other_user_karikeiyaku,  # 他のユーザーの仮契約情報を渡す
    })


def karikeiyaku_cancel(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    karikeiyaku = get_object_or_404(Karikeiyaku, pet=pet, user=request.user)

    if request.method == 'POST':
        # 仮契約を削除
        karikeiyaku.delete()

        # キャンセル完了画面へリダイレクト
        return redirect('karikeiyaku:cancel_complete')  # キャンセル完了画面へのリダイレクト

    return render(request, 'karikeiyaku/karikeiyaku_cancel.html', {'pet': pet})


def cancel_complete(request):
    return render(request, 'karikeiyaku/cancel_com.html')


# 仮契約完了ページ
def karikeiyaku_comp(request):
    return render(request, 'karikeiyaku/karikeiyaku_comp.html')


def contractor(request, pet_id):
    # ペット情報を取得
    pet = get_object_or_404(Pet, id=pet_id)

    # 仮契約情報を取得
    karikeiyaku = Karikeiyaku.objects.filter(pet=pet, status='仮契約中').first()

    # 契約完了ボタンが押された場合
    if request.method == "POST" and 'complete_contract' in request.POST:
        if karikeiyaku:
            print(f"Before update: {karikeiyaku.status}")  # デバッグ用ログ
            karikeiyaku.status = '契約済み'  # ステータスを「契約済み」に変更
            karikeiyaku.save()
            print(f"After update: {karikeiyaku.status}")  # 更新後のログ

        # マイページにリダイレクト
        return redirect(reverse('karikeiyaku:com', kwargs={'pet_id': pet.id}))  # 'mypage'ビューにリダイレクト

    return render(request, 'karikeiyaku/contractor.html', {
        'pet': pet,
        'karikeiyaku': karikeiyaku
    })


def com(request, pet_id):
    # pet_idに基づいて仮契約情報を取得
    karikeiyaku = Karikeiyaku.objects.filter(user=request.user, pet_id=pet_id, status='契約済み').first()

    if not karikeiyaku:
        messages.error(request, "仮契約中のペットがいません。")
        return redirect('accounts:staff_menu')  # 契約が完了したペットがなければトップページへリダイレクト

    pet = karikeiyaku.pet  # 仮契約が完了したペット情報を取得

    # 契約完了したペットとその契約者情報をテンプレートに渡す
    return render(request, 'karikeiyaku/com.html', {
        'pet': pet,
        'karikeiyaku': karikeiyaku
    })


def completed_contract_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    contract = Karikeiyaku.objects.filter(pet=pet, status="契約済み").first()

    if not contract:
        messages.error(request, "契約済みのペットがいません。")
        return redirect('accounts:staff_menu')

    # デバッグ出力
    print("契約者:", contract.user.username)
    print("メールアドレス:", contract.user.email)

    context = {
        'pet': pet,
        'contract': contract,
    }
    return render(request, 'karikeiyaku/completed_contract_detail.html', context)
