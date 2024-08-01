from django.db import models


class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.first_name}"


class MandatoryUser(models.Model):
    chat_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mandatory')
    name = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(unique=True)
    channel_id = models.BigIntegerField(unique=True)

    def __str__(self):
        return f"{self.name}"


class RolesImage(models.Model):
    roleimage_mandatory_id = models.ForeignKey(MandatoryUser, models.CASCADE, related_name='image_mandatory')

    class NameRole(models.TextChoices):
        YIGITLAR = 'YIGITLAR', 'Yigitlar'
        QIZLAR = 'QIZLAR', 'Qizlar'
        JUFLIKLAR = 'JUFLIKLAR', 'Jufliklar'
        KANALLAR_UCHUN = 'KANALLAR_UCHUN', 'Kanallar uchun'
        MULTIK_RASM = 'MULTIK_RASM', 'Multik Rasm'
        JUMA_TABRIGI = 'JUMA_TABRIGI', 'Juma Tabrigi'
        TURLICHA_LOGO = 'TURLICHA_LOGO', 'Turlicha logo'
        PABG_UCHUN = 'PABG_UCHUN', 'Pabg uchun'
        MUSLIM_VA_MUSLIMALAR = 'MUSLIM_VA_MUSLIMALAR', 'Muslim Va Muslimalar uchun'
        KOZGA_ISM = 'KOZGA_ISM', "Ko'zga ism"
        TUGILGAN_KUN = 'TUGILGAN_KUN', 'Tug\'ilgan kun'
        DOSTLARGA = 'DOSTLARGA', 'Do\'stlarga'
        DUGONALARGA = 'DUGONALARGA', 'Dugonalarga'
        BOTLAR_UCHUN = 'BOTLAR_UCHUN', 'Botlar uchun'
        FUTBOLKA_UCHUN = 'FUTBOLKA_UCHUN', 'Futbolka uchun'

    name = models.CharField(max_length=50, choices=NameRole.choices)


class Image(models.Model):
    role_id = models.ForeignKey(RolesImage, models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='roles_images/')



