from django.db import models
from django.contrib.auth.models import User


class Shelter(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    shelter_type = models.CharField(
        max_length=20,
        choices=[('normal', '保健所'), ('protection', '保護施設')],
        default='normal'
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shelters', null=True, blank=True)  # 追加

    def __str__(self):
        return self.name


class Pet(models.Model):
    pet_id = models.CharField(max_length=10, unique=True)  # ペットのID
    age = models.IntegerField()  # 年齢
    size = models.CharField(max_length=50)  # サイズ (例: 小型, 中型, 大型)
    color = models.CharField(max_length=50)  # 毛の色
    inuneko = models.CharField(
        max_length=10,
        choices=[('犬', '犬'), ('猫', '猫')],  # 犬または猫を選択
        default=''
    )
    syu = models.CharField(max_length=100)  # 犬種または猫種を追加

    disease = models.CharField(max_length=100, null=True,  blank=True, default='')  # 病気

    personality = models.CharField(max_length=500, null=False, default='')  # 性格

    sex = models.CharField(
        max_length=10,
        choices=[('男の子', '男の子'), ('女の子', '女の子')],
        default='')

    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='pets', null=True, blank=True)

    def __str__(self):
        return f'{self.pet_id} - {self.size} {self.color} {self.inuneko} ({self.syu})'


class PetImage(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='pet_images/')  # 画像のアップロード先を指定

    def __str__(self):
        return f'Image for {self.pet.pet_id}'


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        User,
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.pet.pet_id}'
