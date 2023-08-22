from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.db import models



class Category (models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("core:product-category", kwargs={"slug": self.slug})

class Color (models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.name

class Rate (models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True, related_name="color")
    rate = models.ForeignKey(Rate, on_delete=models.CASCADE, blank=True, null=True, default="5")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    photo = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_added_to_cart_url(self):
        return reverse("core:added-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

        

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total

class Address1(models.Model):
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postalcode = models.CharField(max_length=100)

    def __str__(self):
        return self.fullname

class CreditCardPayment(models.Model):
    CardNumber = models.CharField(max_length=100)
    ExpDate = models.CharField(max_length=5)
    NameOnCard = models.CharField(max_length=100)
    CVV = models.CharField(max_length=3)

    def __str__(self):
        return self.NameOnCard


class Address2(models.Model):
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postalcode = models.CharField(max_length=100)

    def __str__(self):
        return self.fullname

class Otp(models.Model):
    otp = models.CharField(max_length=100)

    def __str__(self):
        return self.otp

class UploadImage(models.Model):  
    newimage = models.CharField(max_length=100, default="New image")
    image = models.ImageField(upload_to='images')  
  
    def __str__(self):  
        return self.newimage