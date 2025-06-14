# Generated by Django 5.1.7 on 2025-03-13 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('order_item_id', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('payment_type', models.CharField(max_length=20)),
                ('payment_date', models.DateField(null=True)),
            ],
        ),
    ]
