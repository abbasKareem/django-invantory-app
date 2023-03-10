# Generated by Django 4.1.5 on 2023-01-15 20:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("total", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("quantity", models.IntegerField(default=1)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("exist_in_stock", models.BooleanField(default=True)),
                ("slug", models.SlugField(blank=True, max_length=255, null=True)),
                ("jira_number", models.CharField(blank=True, max_length=20, null=True)),
                ("model", models.CharField(blank=True, max_length=100, null=True)),
                ("bar_code", models.CharField(blank=True, max_length=100, null=True)),
                ("image_url", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ecomapp.category",
                    ),
                ),
            ],
            options={"verbose_name_plural": "Products",},
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ordered_by", models.CharField(max_length=200)),
                ("jira_number", models.CharField(max_length=200)),
                (
                    "order_status",
                    models.CharField(
                        choices=[
                            ("In Box", "In Box"),
                            ("Approved", "Approved"),
                            ("Caneled", "Caneled"),
                        ],
                        max_length=50,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "cart",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="ecomapp.cart"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HistoricalProduct",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("quantity", models.IntegerField(default=1)),
                ("created_at", models.DateTimeField(blank=True, editable=False)),
                ("exist_in_stock", models.BooleanField(default=True)),
                ("slug", models.SlugField(blank=True, max_length=255, null=True)),
                ("jira_number", models.CharField(blank=True, max_length=20, null=True)),
                ("model", models.CharField(blank=True, max_length=100, null=True)),
                ("bar_code", models.CharField(blank=True, max_length=100, null=True)),
                ("image_url", models.CharField(blank=True, max_length=100, null=True)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="ecomapp.category",
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical product",
                "verbose_name_plural": "historical Products",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("full_name", models.CharField(max_length=200)),
                ("joined_on", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CartProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField()),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ecomapp.cart"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ecomapp.product",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="cart",
            name="customer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="ecomapp.customer",
            ),
        ),
        migrations.CreateModel(
            name="Admin",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("full_name", models.CharField(max_length=50)),
                ("image", models.ImageField(upload_to="admin")),
                ("mobile", models.CharField(max_length=20)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
