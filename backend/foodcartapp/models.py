from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import F, Sum
from django.utils import timezone


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)

    def fetch_with_available_restaurant_ids(self):
        products = []
        for product in self:
            product.available_restaurant_ids = product.menu_items \
                             .filter(availability=True) \
                             .values_list('restaurant')
            products.append(product)
        return products


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=300,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name='ресторан',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        related_name='menu_items',
        verbose_name='продукт',
        on_delete=models.CASCADE,
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f'{self.restaurant.name} - {self.product.name}'


class OrderQuerySet(models.QuerySet):
    def get_cost(self):
        return self.annotate(cost=Sum(F('starburger_items__price')))

    def prefetch_order_items(self):
        return self.prefetch_related('starburger_items__product') \
                              .select_related('restaurant') \
                              .exclude(status='complete')


class Order(models.Model):
    STATUS_CHOICES = [
        ('incoming', 'Необработанный'),
        ('in_progress', 'Готовится'),
        ('delivery', 'Передан курьеру'),
        ('complete', 'Выполнен'),
    ]
    PAYMENT_TYPE_CHOICES = [
        ('cash', 'Наличными'),
        ('online', 'Онлайн'),
        ('not_specified', 'Не указано'),
    ]
    restaurant = models.ForeignKey(
        Restaurant,
        null=True,
        blank=True,
        related_name='orders',
        on_delete=models.SET_NULL,
    )
    firstname = models.CharField('Имя', max_length=50)
    lastname = models.CharField('Фамилия', max_length=50)
    phonenumber = PhoneNumberField('Номер телефона', max_length=50)
    address = models.TextField('Адрес доставки', max_length=200)
    status = models.CharField(
        'Статус',
        max_length=30,
        default='incoming',
        choices=STATUS_CHOICES,
        db_index=True,
    )
    payment_type = models.CharField(
        'Тип оплаты',
        max_length=30,
        default='not_specified',
        choices=PAYMENT_TYPE_CHOICES,
        db_index=True,
    )
    comment = models.TextField(
        'Комментарий',
        max_length=200,
        blank=True,
    )
    registered_at = models.DateTimeField(
        'Время оформления',
        default=timezone.now,
        db_index=True,
    )
    called_at = models.DateTimeField(
        'Время звонка',
        db_index=True,
        null=True,
        blank=True,
    )
    delivered_at = models.DateTimeField(
        'Время доставки',
        db_index=True,
        null=True,
        blank=True,
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ['-status', 'id']

    def __str__(self):
        return f'Заказ №{self.id}'


class OrderProductItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='starburger_items',
        verbose_name='заказ',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='starburger_items',
        verbose_name='продукт',
    )
    price = models.DecimalField(
        'цена',
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    quantity = models.SmallIntegerField(
        'Количество',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    class Meta:
        verbose_name = 'продукт в заказе'
        verbose_name_plural = 'продукты в заказе'

    def __str__(self):
        return f'Заказ №{self.order.id} - {self.product.name}'
