# Generated by Django 3.0.4 on 2020-03-13 18:03

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='about_us',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_title', models.CharField(help_text='Ихэвчлэн СОРИЛГО.МН гэж байна.', max_length=100, verbose_name='Том гарчиг')),
                ('about_description', models.TextField(help_text='Том гарчигны ард бичигдэх талбай байдлаар орно.', verbose_name='Тодорхойлолт')),
                ('about_general_info_title', models.CharField(blank=True, help_text='Дэд гарчиг байдалтай зүйлийг бичнэ.', max_length=200, null=True, verbose_name='Жижиг гарчиг')),
                ('general_info', models.TextField(help_text='Бидний тухай цэсний гол агуулгыг энэ хэсэгт дэлгэрэнгүй бичиж оруулна.', verbose_name='Бидний тухай')),
            ],
            options={
                'verbose_name': 'Бидний тухай',
                'verbose_name_plural': 'Бидний тухай',
            },
        ),
        migrations.CreateModel(
            name='angi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('angi', models.CharField(blank=True, max_length=250, null=True, unique=True, verbose_name='Анги')),
            ],
            options={
                'verbose_name': 'Анги',
                'verbose_name_plural': 'Анги',
                'ordering': ['angi'],
            },
        ),
        migrations.CreateModel(
            name='clients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(help_text='Хамтран ажилладаг байгууллагын нэрийг оруулна уу', max_length=100, verbose_name='Нэр')),
                ('client_url', models.URLField(help_text='Хамтран ажилладаг байгууллагын веб хуудасны линкийг оруулна уу', verbose_name='Веб хуудас')),
                ('client_image', models.ImageField(upload_to='images/', verbose_name='Логоны зураг')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='Огноо')),
            ],
            options={
                'verbose_name': 'Хамтрагч байгууллага',
                'verbose_name_plural': 'Хамтрагч байгууллага',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='home_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_title', models.CharField(max_length=200, verbose_name='Нүүр хуудасны гарчиг')),
                ('home_copyright', models.CharField(help_text='Ихэвчлэн BRAINMUSCLE INC гэж байна.', max_length=200, verbose_name='Оюуны өмч')),
                ('home_description', models.CharField(max_length=200, verbose_name='Оюыны өмч')),
                ('home_rule', models.TextField(verbose_name='Сайтны зорилго')),
                ('home_address', models.TextField(verbose_name='Хаяг')),
                ('home_email', models.EmailField(help_text='Ихэвчлэн sorilgomn@gmail.com байх бол уу', max_length=254, verbose_name='Цахим хаяг')),
                ('home_phone', models.CharField(max_length=200, verbose_name='Холбоо барих дугаар')),
                ('home_time', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Нүүр хуудасны мэдээлэл',
                'verbose_name_plural': 'Нүүр хуудасны мэдээлэл',
            },
        ),
        migrations.CreateModel(
            name='lesson_with_video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(choices=[('problem', 'Бодлого'), ('video', 'Видео хичээл'), ('theorem', 'Онол')], max_length=20, verbose_name='Агуулгын төрөл')),
                ('name', models.CharField(help_text='Зураг дээр курсор хүрэхэд дээд талд гарч ирэх нэр', max_length=200, verbose_name='Агуулгын нэр')),
                ('title', models.CharField(help_text='Зураг дээр курсор хүрэхэд доод талд гарч ирнэ. Энд богинохон хэмжээний тест оруулах', max_length=200, verbose_name='Агуулгын тухай ойлголт')),
                ('image', models.ImageField(help_text='Зөвхөн нүүр хэсэгт харагдах агуулгыг бүрэн төлөөлөхөөц тодорхой ойлгомжтой зураг оруулах', upload_to='images/', verbose_name='Зураг')),
                ('content', models.FileField(blank=True, help_text='Цааш дарж ороход харагдах дэлгэрэнгүй бодлого эсвэл онолын материалыг зураг хэлбэрээр оруулах', upload_to='videos/', verbose_name='Үндсэн файл')),
                ('video', models.URLField(blank=True, help_text='Агуулгын төрөл зөвхөн видео тохиолдолд YOUTUBE-ийн линк оруулж ажиглана. Бусад тохиолдолд хоосон байна.', verbose_name='Видео хичээлийн линк')),
            ],
            options={
                'verbose_name': 'Цахим агуулга',
                'verbose_name_plural': 'Цахим агуулга',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Нэр')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Зураг')),
                ('description', models.TextField(verbose_name='Тодорхойлолт')),
                ('submision_date', models.DateTimeField(auto_now_add=True, verbose_name='Огноо')),
            ],
            options={
                'verbose_name': 'Үйлчилгээ',
                'verbose_name_plural': 'Үйлчилгээ',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='testimonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100, verbose_name='Нэр')),
                ('author_firm', models.CharField(help_text='Жишээлбэл, BRAINMUSCLE INC үүсгэн байгуулагч', max_length=100, verbose_name='Харъяалал')),
                ('author_image', models.ImageField(upload_to='images/', verbose_name='Зураг')),
                ('testimonial', models.TextField(verbose_name='Философи')),
                ('submision_date', models.DateTimeField(auto_now_add=True, verbose_name='Огноо')),
            ],
            options={
                'verbose_name': 'Философи',
                'verbose_name_plural': 'Философи',
            },
        ),
        migrations.CreateModel(
            name='blog_post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Гарчиг')),
                ('description', models.CharField(help_text='300 тэмдэгтээс хэтрүүлж болохгүй', max_length=300, verbose_name='Тайлбар')),
                ('figure', models.ImageField(upload_to='images/', verbose_name='Зураг')),
                ('content', ckeditor.fields.RichTextField()),
                ('submision_date', models.DateTimeField(auto_now_add=True, verbose_name='Огноо')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Нийтлэл',
                'verbose_name_plural': 'Нийтлэл',
            },
        ),
        migrations.CreateModel(
            name='angi_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('angi_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.angi')),
                ('students', models.ManyToManyField(related_name='students', to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ангийн мэдээлэл',
                'verbose_name_plural': 'Ангийн мэдээлэл',
            },
        ),
    ]