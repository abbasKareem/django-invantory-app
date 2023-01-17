from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from django.urls import reverse


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

    history = HistoricalRecords()


    # image = models.ImageField(upload_to="products")
    # marked_price = models.PositiveIntegerField()
    # selling_price = models.PositiveIntegerField()
    # description = models.TextField()
    # warranty = models.CharField(max_length=300, null=True, blank=True)
    # return_policy = models.CharField(max_length=300, null=True, blank=True)
    # view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.quantity <= 0:
            self.exist_in_stock = False
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





