# Generated by Django 5.0.1 on 2024-01-10 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botapp', '0002_rename_a_words_v1_rename_b_words_v2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='words',
            name='used',
            field=models.BooleanField(default=False),
        ),
    ]
