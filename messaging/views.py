from django.shortcuts import render, get_object_or_404, redirect
from .models import Pet, Comment
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

        recipient_email = 'ngn2349602@stu.o-hara.ac.jp'  # 固定の受信者メールアドレス

        # メールを送信
        send_mail(
            f'新しいメッセージ: {sender_name}さんからのお問い合わせ',
            message_content,
            recipient_email,
            [recipient_email, sender_email],
            fail_silently=False,
        )

        # 完了画面にリダイレクト
        return render(request, 'messaging/send_message_complete.html', {
            'sender_name': sender_name,
            'sender_email': sender_email,
            'message_content': message_content,
        })
    else:
        form = MessageForm()

    return render(request, 'messaging/send_message.html', {'form': form})


def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    comments = pet.comments.all().order_by('-timestamp')

    user_karikeiyaku = None
    other_user_karikeiyaku = None

    if request.user.is_authenticated:
        user_karikeiyaku = Karikeiyaku.objects.filter(user=request.user, pet=pet).first()
        other_user_karikeiyaku = Karikeiyaku.objects.filter(pet=pet, status="仮契約中").exclude(user=request.user).first()

    # POSTリクエストの処理
    if request.method == 'POST':
        print("POST data:", request.POST)  # デバッグ用の出力
        if 'delete_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id)
            if request.user.is_superuser:
                comment.delete()
                print(f"Comment ID {comment_id} deleted by {request.user}")
                return redirect('messaging:pet_detail', pet_id=pet.id)
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.pet = pet
                comment.user = request.user
                comment.save()
                return redirect('messaging:pet_detail', pet_id=pet.id)
    else:
        form = CommentForm()

    # 常にformを渡す
    return render(request, 'pets/pet_detail.html', {
        'pet': pet,
        'comments': comments,
        'form': form,
        'user_karikeiyaku': user_karikeiyaku,
        'other_user_karikeiyaku': other_user_karikeiyaku,
    })
