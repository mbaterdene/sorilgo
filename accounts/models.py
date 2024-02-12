from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete = models.CASCADE
    )
    first_name = models.CharField(
        max_length = 100, 
        blank = True
    )
    last_name = models.CharField(
        max_length = 100, 
        blank = True
    )
    email = models.EmailField(
        max_length = 150
    )
    signup_confirmation = models.BooleanField(
        default = False
    )

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class teacher_status(models.Model):
    user = models.OneToOneField(
       User,
       on_delete = models.CASCADE,
       verbose_name = "Хэрэглэгчийн нэр"
    )
    is_teacher = models.BooleanField(
        default = False,
        blank = False,
        verbose_name = 'Багш эсэх',
        help_text = 'Сорилго боловсролын цогц системд багшийн эрхээр орж, сурагчдынхаа мэдээллийг үзэх эрхтэй болгох'
    )
    class Meta:
        verbose_name = "Багшлах эрх"
        verbose_name_plural = "Багшлах эрх"

class lesson_status(models.Model):
    user = models.OneToOneField(
       User,
       on_delete = models.CASCADE,
       verbose_name = "Хэрэглэгчийн нэр"
    )
    test_videos = models.BooleanField(
        default = False,
        blank = False,
        help_text = 'Уг хэрэглэгч алдсан бодлогынхоо видео бодолтыг үзэх эрхтэй бол заавал сонгоно уу.',
        verbose_name = 'Тестийн бодолт үзэх эсэх'
    )
    whole_videos = models.BooleanField(
        default = False,
        blank = False,
        help_text = 'Уг хэрэглэгч системд байгаа бүх хичээлийг үзэх эрхтэй бол заавал сонгоно уу.',
        verbose_name = 'Бүх хичээлийг үзэх эсэх'
    )
    video_lesson_word = models.BooleanField(
        default = False,
        blank = False,
        help_text = 'Уг хэрэглэгч цуврал хичээлүүдийг үзэх эрхтэй бол заавал сонгоно уу.',
        verbose_name = 'Өгүүлбэртэй бодлого'
    )
    video_lesson_other = models.BooleanField(
        default = False,
        blank = False,
        help_text = 'Уг хэрэглэгч цуврал хичээлүүдийг үзэх эрхтэй бол заавал сонгоно уу.',
        verbose_name = 'Нэмэлт хөтөлбөр'
    )
    video_lesson_geometry = models.BooleanField(
        default = False,
        blank = False,
        help_text = 'Уг хэрэглэгч цуврал хичээлүүдийг үзэх эрхтэй бол заавал сонгоно уу.',
        verbose_name = 'Геометр'
    )
    video_lesson_combina = models.BooleanField(
        default = False,
        blank = False,
        help_text = 'Уг хэрэглэгч цуврал хичээлүүдийг үзэх эрхтэй бол заавал сонгоно уу.',
        verbose_name = 'Боломж тоолох'
    )
    class Meta:
        verbose_name = "Хэрэглэгчийн нэмэлт эрх"
        verbose_name_plural = "Хэрэглэгчийн нэмэлт эрх"

class user_info(models.Model):
    user = models.OneToOneField(
       User,
       on_delete = models.CASCADE,
       verbose_name = "Хэрэглэгчийн нэр"
    )
    phone = models.CharField(
       max_length=256,
       blank=True,
       null=True,
       verbose_name = "Холбоо барих дугаар"
    )
    gender = models.CharField(
        max_length = 1,
        choices = (('m', 'Эрэгтэй'), ('f', 'Эмэгтэй')),
        blank = True,
        null = True,
        verbose_name = "Хүйс"
    )
    image = models.ImageField(
        default='default.png',
        upload_to='profile_pics/'
    )
    add_info = models.CharField(
        max_length = 300,
        verbose_name = "Нэмэлт мэдээлэл",
        blank = True,
        null = True,
        help_text = "Сургууль, анги гэх мэт нэмэлт хэрэг болж магадгүй мэдээлэл оруулах"
    )
    class Meta:
        verbose_name = "Хэрэглэгч нэмэх болон бүртгэх"
        verbose_name_plural = "Хэрэглэгч нэмэх болон бүртгэх"
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        user_info.objects.create(user=instance)
    instance.user_info.save()

class whatsgrade(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE
    )
    is_grade = models.CharField(
        max_length = 2,
        choices = (('fp', '5-р анги'), ('ef', '8-р анги'), ('tg','12-р анги')),
        blank = True,
        null = True,
        verbose_name = "Анги"
    )
@receiver(post_save, sender=User)
def create_or_update_whatsgrade(sender, instance, created, **kwargs):
    if created:
        whatsgrade.objects.create(user=instance)
    instance.whatsgrade.save()

class price_test(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE
    )
    is_payed = models.BooleanField(
        default = False,
        blank = False,
        verbose_name = 'Тест ажиллах эсэх',
        help_text = 'Тест ажиллах төлбөр төлсөн эсэхийг тодорхойлох'
    )
    class Meta:
        verbose_name = "Тестийн эрх"
        verbose_name_plural = "Тестийн эрх"
