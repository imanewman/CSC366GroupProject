# Generated by Django 3.0.6 on 2020-05-30 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0021_inventory_supplier_supplierinvoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplierinvoice',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.CreateModel(
            name='SupplierInvoiceLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('costPerItem', models.FloatField()),
                ('stockItem', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='business.StockItem')),
                ('supplierInvoice', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='business.SupplierInvoice')),
            ],
        ),
        migrations.AddField(
            model_name='supplierinvoice',
            name='items',
            field=models.ManyToManyField(through='business.SupplierInvoiceLine', to='business.StockItem'),
        ),
    ]