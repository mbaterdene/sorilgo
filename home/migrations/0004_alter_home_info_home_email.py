# Generated by Django 5.0.1 on 2024-02-06 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_lesson_status_teacher_status_tuslamj'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home_info',
            name='home_email',
            field=models.EmailField(help_text='Ихэвчлэн bod@gmail.com байх бол уу', max_length=254, verbose_name='Цахим хаяг'),
        ),
    ]