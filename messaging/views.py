from django.shortcuts import render, get_object_or_404, redirect
from .models import Pet, Comment, FavoritePet
from django.contrib.auth.decorators import login_required
from .forms import MessageForm, CommentForm
from django.core.mail import send_mail
from django.views.generic.base import TemplateView
from karikeiyaku.models import Karikeiyaku  # 仮契約モデルをインポート


def send_message(request):
    if request.method == 'POST':
        sender_name = request.POST.get('sender_name')  # フォームから送信された名前
        sender_email = request.POST.get('sender_email')  # フォームから送信されたメールアドレス
        message_content = request.POST.get('message')
        pet_id = request.POST.get('pet_id')  # pet_id がPOSTデータで送られる場合

        recipient_email = 'ngn2349602@stu.o-hara.ac.jp'  # 固定の受信者メールアドレス

        # メールを送信
        send_mail(
            f'新しいメッセージ: {sender_name}さんからのお問い合わせ',
            message_content,
            sender_email,
            [recipient_email],
            fail_silently=False,
        )

        # 完了画面にリダイレクト
        return render(request, 'messaging/send_message_complete.html', {
            'sender_name': sender_name,
            'sender_email': sender_email,
            'message_content': message_content,
            'pet_id': pet_id,
        })
    else:
        form = MessageForm()

    return render(request, 'messaging/send_message.html', {'form': form})


def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    comments = pet.comments.all().order_by('-timestamp')  # ペットに関連するすべてのコメントを取得

    # ログインしていないユーザーにも対応するために、匿名ユーザーの場合は None を設定
    user_karikeiyaku = None
    other_user_karikeiyaku = None

    # ログインしている場合のみ仮契約情報を取得
    if request.user.is_authenticated:
        user_karikeiyaku = Karikeiyaku.objects.filter(user=request.user, pet=pet).first()
        other_user_karikeiyaku = Karikeiyaku.objects.filter(pet=pet, status="仮契約中").exclude(user=request.user).first()

    # コメントフォームの処理
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.pet = pet
            comment.user = request.user  # 現在のユーザーをコメントの投稿者に設定

            # 管理者のコメントには特別なマークを追加
            if request.user.is_superuser:
                comment.content = comment.content

            comment.save()
            return redirect('messaging:pet_detail', pet_id=pet.id)

        # コメント削除処理 (管理者のみ)
        if 'delete_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id)
            if request.user.is_superuser:  # 管理者のみ削除可能
                comment.delete()
                return redirect('messaging:pet_detail', pet_id=pet.id)
    else:
        form = CommentForm()

    return render(request, 'pets/pet_detail.html', {
        'pet': pet,
        'comments': comments,  # ペットのコメントをテンプレートに渡す
        'form': form,
        'user_karikeiyaku': user_karikeiyaku,
        'other_user_karikeiyaku': other_user_karikeiyaku,
    })


@login_required
def toggle_favorite(request, pet_id):
    pet = Pet.objects.get(id=pet_id)

    if request.method == "POST":
        # チェックボックスの状態を取得
        is_favorite = request.POST.get('favorite') == 'on'
        
        if is_favorite:
            # お気に入りに登録
            FavoritePet.objects.get_or_create(user=request.user, pet=pet)
        else:
            # お気に入りから解除
            FavoritePet.objects.filter(user=request.user, pet=pet).delete()

    return redirect('pet_detail', pet_id=pet.id)


class IndexView(TemplateView):
    template_name = 'messaging/index.html'


def index(request):
    return render(request, 'messaging/index.html')
