# Generated by Django 5.1.1 on 2024-10-17 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0011_alter_task_description_alter_task_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(blank=True, null=True, to='labels.label', verbose_name='Labels'),
        ),
    ]
