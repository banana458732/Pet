from django.db import models
from django.contrib.auth.models import User
from petapp.models import Pet
from accounts.models import CustomUser


class Message(models.Model):
    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='messages',
        null=True,
        blank=True
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return (f'Message from {self.sender.username}'
                f'to {self.recipient.username} '
                f'about {self.pet.pet_id if self.pet else "No Pet"}')


class Comment(models.Model):
    pet = models.ForeignKey(Pet, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username}'


class Karikeiyaku(models.Model):
    # 他のフィールド...
    status = models.CharField(
        max_length=50,
        choices=[('仮契約中', '仮契約中'), ('キャンセル', 'キャンセル'), ('仮契約済', '仮契約済')],
        default='仮契約中', verbose_name="ステータス"
    )
    # 他のフィールド...