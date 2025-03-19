from djongo import models


class Author(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=255, unique=True)
    birth_date = models.DateField()

    class Meta:
        db_table = 'authors'
        ordering = ['name']
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.name


class Publisher(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=255)
    address = models.TextField()

    class Meta:
        db_table = 'publishers'
        ordering = ['name']
        verbose_name_plural = 'Publishers'

    def __str__(self):
        return self.name


class Category(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'categories'
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Book(models.Model):
    _id = models.ObjectIdField()
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    published_date = models.DateField()
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='images/covers/')
    price = models.IntegerField()
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    categories = models.CharField(max_length=255)
    type = models.CharField(max_length=255, default='book')

    class Meta:
        db_table = 'books'
        ordering = ['title']
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title
