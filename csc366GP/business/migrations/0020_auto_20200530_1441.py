# Generated by Django 3.0.6 on 2020-05-30 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0019_locationexpenses'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField()),
                ('menuItem', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='business.MenuItem')),
                ('stockItem', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='business.StockItem')),
            ],
        ),
        migrations.AddField(
            model_name='menuitem',
            name='items',
            field=models.ManyToManyField(through='business.Ingredients', to='business.StockItem'),
        ),
    ]
