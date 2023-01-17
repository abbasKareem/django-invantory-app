# Generated by Django 4.1.5 on 2023-01-16 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ecomapp", "0003_alter_cartproduct_cart"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartproduct",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="theproduct",
                to="ecomapp.product",
            ),
        ),
    ]
