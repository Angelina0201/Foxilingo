# Generated by Django 3.1.3 on 2020-12-15 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foxilang', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='theme',
            old_name='practice',
            new_name='answers',
        ),
        migrations.AddField(
            model_name='theme',
            name='questions',
            field=models.TextField(default=str),
            preserve_default=False,
        ),
    ]
