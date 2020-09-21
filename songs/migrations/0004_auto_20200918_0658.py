# Generated by Django 3.1.1 on 2020-09-18 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0003_auto_20200918_0655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='tag',
            field=models.ManyToManyField(null=True, to='songs.Tag'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='content',
            field=models.CharField(max_length=50),
        ),
    ]