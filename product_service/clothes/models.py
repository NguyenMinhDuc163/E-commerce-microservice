from djongo import models


class Brand(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    class Meta:
        db_table = 'brands'
        ordering = ['name']
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name


class Clothes(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=255, unique=True)
    size = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    sale = models.IntegerField()
    color = models.CharField(max_length=255)
    type = models.CharField(max_length=255, default='clothes')
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='images/clothes/')
    brand = models.CharField(max_length=255)

    class Meta:
        db_table = 'clothes'
        ordering = ['name']
        verbose_name_plural = 'Clothes'

    def __str__(self):
        return self.name
