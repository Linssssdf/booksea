# Generated by Django 5.1.1 on 2025-03-15 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_alter_user_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.FloatField(null=True),
        ),
    ]
