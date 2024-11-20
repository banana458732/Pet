from django.shortcuts import render, get_object_or_404, redirect
from .models import Pet
from django.contrib.auth.decorators import login_required
from .forms import MessageForm, CommentForm
from django.core.mail import send_mail
from django.views.generic.base import TemplateView


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
            return redirect('pet_detail', pet_id=pet.id)
    else:
        form = CommentForm()

    return render(request, 'pets/pet_detail.html', {
        'pet': pet,
        'comments': comments,  # ペットのコメントをテンプレートに渡す
        'form': form
    })


class IndexView(TemplateView):
    template_name = 'messaging/index.html'


def index(request):
    return render(request, 'messaging/index.html')
