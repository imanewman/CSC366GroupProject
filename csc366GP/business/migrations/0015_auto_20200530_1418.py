# Generated by Django 3.0.6 on 2020-05-30 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0014_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.Customer'),
        ),
    ]
