# Generated by Django 4.1.7 on 2023-03-21 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.IntegerField()),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('profile_img', models.ImageField(default='default.jpg', upload_to='profile_images')),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]