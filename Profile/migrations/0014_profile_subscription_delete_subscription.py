# Generated by Django 5.0.6 on 2024-05-14 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0013_remove_profile_following_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='subscription',
            field=models.ManyToManyField(blank=True, to='Profile.profile'),
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]