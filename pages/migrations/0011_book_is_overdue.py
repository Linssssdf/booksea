# Generated by Django 5.1.1 on 2025-03-18 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_book_borrower'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_overdue',
            field=models.BooleanField(default=False),
        ),
    ]
