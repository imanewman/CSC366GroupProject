# Generated by Django 3.0.6 on 2020-05-30 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0009_auto_20200530_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
            ],
        ),
    ]
