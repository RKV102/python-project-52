# Generated by Django 5.1.1 on 2024-11-22 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0004_alter_status_options_alter_status_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='status',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Updated at'),
        ),
    ]
