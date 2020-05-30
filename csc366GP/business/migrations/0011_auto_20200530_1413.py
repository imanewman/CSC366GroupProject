# Generated by Django 3.0.6 on 2020-05-30 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0010_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='employementrecod',
            name='location',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='business.Location'),
        ),
        migrations.AddField(
            model_name='location',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='location',
            name='state',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='location',
            name='city',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]