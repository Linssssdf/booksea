# Generated by Django 5.1.1 on 2025-03-12 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_alter_book_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='borrow_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
