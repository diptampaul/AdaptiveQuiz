# Generated by Django 3.1.7 on 2021-03-23 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='difficulty',
            field=models.CharField(choices=[('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard')], default='null', max_length=6),
            preserve_default=False,
        ),
    ]
