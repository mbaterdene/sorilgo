import re
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from model_utils.managers import InheritanceManager
# from djrichtextfield.models import RichTextField
from ckeditor.fields import RichTextField
from django.dispatch import receiver

## 04_23

class tuslamj(models.Model):
    HELP_CHOICE = [('images','Зураг'), ('video','Видео')]
    help_group = models.CharField(
        choices = HELP_CHOICE, 
        max_length = 20,
        verbose_name = "Агуулгын төрөл"
    )
    help_name = models.CharField(
        max_length = 200,
        verbose_name = "Агуулгын нэр",
        help_text = "Зураг дээр курсор хүрэхэд дээд талд гарч ирэх нэр"
    )
    help_title = models.CharField(
        max_length = 200,
        verbose_name = "Агуулгын тухай ойлголт",
        help_text = "Зураг дээр курсор хүрэхэд доод талд гарч ирнэ. Энд богинохон хэмжээний тест оруулах"
    )
    help_image = models.ImageField(
        upload_to = 'help/images/',
        verbose_name = "Зураг",
        help_text = "Зөвхөн нүүр хэсэгт харагдах агуулгыг бүрэн төлөөлөхөөц тодорхой ойлгомжтой зураг оруулах"
    )
    help_content = models.FileField(
        upload_to = 'help/videos/', 
        blank = True,
        verbose_name = "Үндсэн файл",
        help_text = "Цааш дарж ороход харагдах дэлгэрэнгүй бодлого эсвэл онолын материалыг зураг хэлбэрээр оруулах"
    )
    help_video = models.URLField(
        blank = True,
        verbose_name = "Видео хичээлийн линк",
        help_text = "Агуулгын төрөл зөвхөн видео тохиолдолд YOUTUBE-ийн линк оруулж ажиглана. Бусад тохиолдолд хоосон байна."
    )
    def __str__(self):
        return self.help_name
    class Meta:
        ordering = ['id']
        verbose_name = "Заавар, зөвлөмж"
        verbose_name_plural = "Заавар, зөвлөмж"
 
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
    video_lesson = models.BooleanField(
        default = False,
        blank = False,
        help_text = 'Уг хэрэглэгч цуврал хичээлүүдийг үзэх эрхтэй бол заавал сонгоно уу.',
        verbose_name = 'Хичээл үзэх эрхтэй эсэх'
    )
    class Meta:
        verbose_name = "Хэрэглэгчийн нэмэлт эрх"
        verbose_name_plural = "Хэрэглэгчийн нэмэлт эрх"

## old


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
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        user_info.objects.create(user=instance)
    instance.user_info.save()
    
class blog_post(models.Model):
    title = models.CharField(
        max_length = 200,
        verbose_name = "Гарчиг",
    )
    description = models.CharField(
        max_length = 300,
        verbose_name = "Тайлбар",
        help_text = "300 тэмдэгтээс хэтрүүлж болохгүй"
    )
    figure = models.ImageField(
        upload_to = 'images/',
        verbose_name = "Зураг"
    )
    content = RichTextField()
    submision_date = models.DateTimeField(
        auto_now_add = True,
        verbose_name = "Огноо"
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE )
    class Meta:
        verbose_name = "Нийтлэл"
        verbose_name_plural = "Нийтлэл"

class home_info(models.Model):
    home_title = models.CharField(
        max_length = 200,
        verbose_name = "Нүүр хуудасны гарчиг"
    )
    home_copyright = models.CharField(
        max_length = 200,
        verbose_name = "Оюуны өмч",
        help_text = "Ихэвчлэн BRAINMUSCLE INC гэж байна."
    )
    home_description = models.CharField(
        max_length = 200,
        verbose_name = "Оюыны өмч",
        help_text = ""
    )
    home_rule = models.TextField(
         verbose_name = "Сайтны зорилго"
    )
    home_address = models.TextField(
        verbose_name = "Хаяг",
        help_text = ""
    )
    home_email = models.EmailField(
        verbose_name = "Цахим хаяг",
        help_text = "Ихэвчлэн bod@gmail.com байх бол уу"
    )
    home_phone = models.CharField(
        max_length = 200, 
        verbose_name = "Холбоо барих дугаар",
        help_text = ""
    )
    home_time = models.CharField(max_length = 200)
    class Meta:
        verbose_name = "Нүүр хуудасны мэдээлэл"
        verbose_name_plural = "Нүүр хуудасны мэдээлэл"

class services(models.Model):
    name = models.CharField(
        max_length = 100,
        verbose_name = "Нэр"
    )
    image = models.ImageField(
        upload_to = 'images/',
        verbose_name = "Зураг"
    )
    description = models.TextField(
        verbose_name = "Тодорхойлолт"
    )
    submision_date = models.DateTimeField(
        auto_now_add = True,
        verbose_name = "Огноо"
    )
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['id']
        verbose_name = "Үйлчилгээ"
        verbose_name_plural = "Үйлчилгээ"

class testimonial(models.Model):
    author = models.CharField(
        max_length = 100,
        verbose_name = "Нэр"
    )
    author_firm = models.CharField(
        max_length = 100,
        verbose_name = "Харъяалал",
        help_text = "Жишээлбэл, BRAINMUSCLE INC үүсгэн байгуулагч"
    )
    author_image = models.ImageField(
        upload_to = 'images/',
        verbose_name = "Зураг"
    )
    testimonial = models.TextField(
        verbose_name = "Философи"
    )
    submision_date = models.DateTimeField(
        auto_now_add = True,
        verbose_name = "Огноо"
    )
    def __str__(self):
        return self.author
    class Meta:
        verbose_name = "Философи"
        verbose_name_plural = "Философи"

class clients(models.Model):
    client_name = models.CharField(
        max_length=100,
        verbose_name = "Нэр",
        help_text = "Хамтран ажилладаг байгууллагын нэрийг оруулна уу"
    )
    client_url = models.URLField(
        verbose_name = "Веб хуудас",
        help_text = "Хамтран ажилладаг байгууллагын веб хуудасны линкийг оруулна уу"
    )
    client_image = models.ImageField(
        upload_to = 'images/',
        verbose_name = "Логоны зураг"
    )
    submission_date = models.DateTimeField(
        auto_now_add = True,
        verbose_name = "Огноо"
    )
    def __str__(self):
        return self.client_name
    class Meta:
        ordering = ['id']
        verbose_name = "Хамтрагч байгууллага"
        verbose_name_plural = "Хамтрагч байгууллага"

class about_us(models.Model):
    about_title = models.CharField(
        max_length = 100,
        verbose_name = "Том гарчиг",
        help_text = "Ихэвчлэн СОРИЛГО.МН гэж байна."
    )
    about_description = models.TextField(
        verbose_name = "Тодорхойлолт",
        help_text = "Том гарчигны ард бичигдэх талбай байдлаар орно."
    )
    about_general_info_title = models.CharField(
        max_length = 200,
        verbose_name = "Жижиг гарчиг",
        help_text = "Дэд гарчиг байдалтай зүйлийг бичнэ.",
        blank = True,
        null = True
    )
    general_info = models.TextField(
        verbose_name = "Бидний тухай",
        help_text = "Бидний тухай цэсний гол агуулгыг энэ хэсэгт дэлгэрэнгүй бичиж оруулна."
    )

    class Meta:
        verbose_name = "Бидний тухай"
        verbose_name_plural = "Бидний тухай"

class lesson_with_video(models.Model):
    PORTFO_CHOICE = [('problem','Бодлого'), ('video','Видео хичээл'), ('theorem','Онол')]
    group = models.CharField(
        choices = PORTFO_CHOICE, 
        max_length = 20,
        verbose_name = "Агуулгын төрөл"
    )
    name = models.CharField(
        max_length = 200,
        verbose_name = "Агуулгын нэр",
        help_text = "Зураг дээр курсор хүрэхэд дээд талд гарч ирэх нэр"
    )
    title = models.CharField(
        max_length = 200,
        verbose_name = "Агуулгын тухай ойлголт",
        help_text = "Зураг дээр курсор хүрэхэд доод талд гарч ирнэ. Энд богинохон хэмжээний тест оруулах"
    )
    image = models.ImageField(
        upload_to = 'images/',
        verbose_name = "Зураг",
        help_text = "Зөвхөн нүүр хэсэгт харагдах агуулгыг бүрэн төлөөлөхөөц тодорхой ойлгомжтой зураг оруулах"
    )
    content = models.FileField(
        upload_to = 'videos/', 
        blank = True,
        verbose_name = "Үндсэн файл",
        help_text = "Цааш дарж ороход харагдах дэлгэрэнгүй бодлого эсвэл онолын материалыг зураг хэлбэрээр оруулах"
    )
    video = models.URLField(
        blank = True,
        verbose_name = "Видео хичээлийн линк",
        help_text = "Агуулгын төрөл зөвхөн видео тохиолдолд YOUTUBE-ийн линк оруулж ажиглана. Бусад тохиолдолд хоосон байна."
    )
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['id']
        verbose_name = "Цахим агуулга"
        verbose_name_plural = "Цахим агуулга"

class AngiManager(models.Manager):

    def new_angi(self, angi):
        new_angi = self.create(angi=re.sub('\s+', '-', angi).lower())
        new_angi.save()
        return new_angi


class angi(models.Model):

    angi = models.CharField(
        verbose_name = "Анги",
        max_length = 250, 
        blank = True,
        unique = True, 
        null = True
    )

    objects = AngiManager()

    class Meta:
        verbose_name = "Анги"
        verbose_name_plural = "Анги"
        ordering = ['angi']

    def __str__(self):
        return self.angi

class angi_info(models.Model):
    angi_info = models.ForeignKey(
        angi,
        on_delete = models.CASCADE
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='teacher',
        on_delete = models.CASCADE
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='students'
    )
    class Meta:
        verbose_name = "Ангийн мэдээлэл"
        verbose_name_plural = "Ангийн мэдээлэл"
