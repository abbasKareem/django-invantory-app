from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="admin")
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username



# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=200)
#     # address = models.CharField(max_length=200, null=True, blank=True)
#     joined_on = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.full_name


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)


    def get_absolute_url(self):
        return reverse('ecomapp:category_list', args=[self.slug])


    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=200)

    # Category have many product, but product have one categroy
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    exist_in_stock = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    jira_number = models.CharField(max_length=20, null=True,  blank=True)
    model = models.CharField(max_length=100, null=True,  blank=True)
    bar_code = models.CharField(max_length=100, null=True,  blank=True)
    image_url = models.CharField(max_length=100, null=True,  blank=True)
    min_quantity_to_end = models.PositiveIntegerField(default=5, null=True, blank=True)
    about_to_end = models.BooleanField(default=True, null=True, blank=True)


    history = HistoricalRecords()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.quantity <= 0:
            self.exist_in_stock = False
        if self.quantity <= self.min_quantity_to_end:
            self.about_to_end = True
        if self.quantity > self.min_quantity_to_end:
            self.about_to_end = False
        super(Product, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'Products'


class Cart(models.Model):
    # Customer may have many carts, but cart only belong to one customer
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(self.id)



class CartProduct(models.Model):
    # a Cart may have many CartProduct, 
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    # rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    # subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)


ORDER_STATUS = (
    ("In Box", "In Box"),
    ("Approved", "Approved"),
    ("Caneled", "Caneled")
)

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    # ordered_by = models.ForeignKey(Customer, on_delete=models.SET_NULL)
    jira_number = models.CharField(max_length=200)
    # mobile = models.CharField(max_length=10)
    # email = models.EmailField(null=True, blank=True)
    # subtotal = models.PositiveIntegerField()
    # discount = models.PositiveIntegerField()
    # total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()
    

    def __str__(self):
        return "Order: " + str(self.id)

# method for updating
@receiver(post_save, sender=Order)
def update_approved(sender, instance, **kwargs):
    if instance.order_status == 'Approved':
        all_cart_products = instance.cart.cartproduct_set.all()
        for single_cart_product in all_cart_products:
            the_product = single_cart_product.product
            the_product.quantity -= single_cart_product.quantity
            the_product.save()



