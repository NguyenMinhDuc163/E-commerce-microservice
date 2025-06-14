# Generated by Django 5.1.7 on 2025-03-13 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('order_item_id', models.IntegerField()),
                ('username', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=10)),
                ('shipment_status', models.CharField(max_length=50)),
                ('shipment_type', models.CharField(max_length=50)),
                ('price', models.IntegerField(null=True)),
            ],
        ),
    ]
