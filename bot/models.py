from django.db import models

class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)  # Optional
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)  # Optional
    
    def __str__(self):
        return f"{self.name or 'No Name'}"

    def __str__(self):
        return f"{self.name}"


class MandatoryUser(models.Model):
    chat_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mandatory')
    name = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=200)
    channel_id = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.name}"


class NameRole(models.Model):
    roles = (
        ('Yigitlar', 'Yigitlar'),
        ('Qizlar', 'Qizlar'),
        ('Juftliklar', 'Juftliklar'),
    )
    name = models.CharField(max_length=500, choices=roles)
    image = models.ImageField(upload_to='role_image/')
    def __str__(self) -> str:
        return self.name

class Image(models.Model):
    role_id = models.ForeignKey(NameRole, models.CASCADE, related_name='images')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='roles_images/')
    def __str__(self) -> str:
        return self.name

class Video(models.Model):
    name = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos/')
    def __str__(self) -> str:
        return self.name

class OrderVideo(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    channel_id = models.CharField(max_length=20)
    def __str__(self) -> str:
        return self.name
    