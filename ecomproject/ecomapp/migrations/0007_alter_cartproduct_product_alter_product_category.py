# Generated by Django 4.1.5 on 2023-01-16 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ecomapp", "0006_alter_cartproduct_cart"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartproduct",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="ecomapp.product",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="ecomapp.category"
            ),
        ),
    ]
