# Generated by Django 4.2.8 on 2024-01-03 03:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0007_alter_cart_id_alter_cartitem_cart"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="cartitem",
            unique_together={("cart", "product")},
        ),
    ]
