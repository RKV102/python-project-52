# Generated by Django 5.1.1 on 2024-09-16 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=20, null=True),
        ),
    ]