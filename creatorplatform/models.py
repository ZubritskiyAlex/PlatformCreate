from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models, transaction


# Create your models here.

class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError("The given email must be set")
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
            return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password=password, **extra_fields)


class Customer(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name='username', max_length=30, blank=True)
    email = models.EmailField(max_length=40, unique=True)
    is_staff = models.BooleanField(default=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    url = models.URLField(verbose_name='URL', blank=True, null=True)
    description = models.CharField(max_length=255, verbose_name="Description", blank=True, null=True)
    image = models.ImageField(verbose_name='Photo', null=True)
    date_created = models.DateField(auto_now=True)
    is_owner = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        super(Customer, self).save(*args, **kwargs)
        return self

    class Meta:
        db_table = 'User'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"


class Store(models.Model):

    user = models.ForeignKey(Customer, related_name="user", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Store name")
    url = models.URLField(verbose_name='URL', blank=True, null=True, unique=True)
    description = models.TextField("Description")
    date_created = models.DateField(auto_now=True)
    image = models.ImageField(verbose_name='Image', upload_to='uploads/images', null=False, blank=False)
    category = models.ForeignKey('Category',related_name="category", verbose_name='Category', on_delete=models.PROTECT, null=True)
    owner = models.ForeignKey(Customer,related_name="owner", on_delete=models.SET_NULL,
                              null=True)

    objects = models.Manager()


    def __str__(self):
        return f"{self.user} - {self.name}-{self.description}-{self.url}"


    class Meta:
        db_table = "Store"
        verbose_name = "Store"
        verbose_name_plural = "Stores"


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Name of category')
    slug = models.SlugField(unique=True)
    url = models.URLField(verbose_name='URL', blank=True, null=True, unique=True)

    def __str__(self):
        return self.name


    class Meta:

        db_table = "Category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):

    title = models.CharField(max_length=255, verbose_name="Product name")
    stores = models.ForeignKey(Store, verbose_name='Stores',on_delete=models.CASCADE, default="1")
    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.PROTECT, null=True)
    description = models.TextField(verbose_name='Description', null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Price", default=0)
    date_created = models.DateField(auto_now=True)
    image = models.ImageField(verbose_name='Image',upload_to='uploads/images', null=False, blank=False)
    url = models.URLField(verbose_name='URL', blank=True, null=True, unique=True)
    draft = models.BooleanField("Draft", default=False)

    owner = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True, related_name='my_products')

    def __str__(self):
        return f"{self.title} - {self.price}"


    class Meta:

        db_table = "Product"
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Review(models.Model):
    """Reviews"""
    email = models.EmailField(verbose_name="Email")
    name = models.CharField("Name", max_length=100)
    text = models.TextField("Message", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Parent", on_delete=models.SET_NULL, blank=True, null=True
    )
    review_on_store = models.ForeignKey(Store, verbose_name="Parent", on_delete=models.SET_NULL, blank=True, null=True
    )
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.product}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
