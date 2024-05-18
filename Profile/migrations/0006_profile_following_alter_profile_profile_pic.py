# Generated by Django 5.0.2 on 2024-04-10 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0005_remove_profile_vk_profile_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='followers', to='Profile.profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='profile/default.png', upload_to='profile'),
        ),
    ]
