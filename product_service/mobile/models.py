from djongo import models


class Producer(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    address = models.TextField()
    phone_number = models.CharField(max_length=255)
    email = models.EmailField()
    website = models.URLField()

    class Meta:
        db_table = 'producers'
        ordering = ['name']
        verbose_name_plural = 'Producers'

    def __str__(self):
        return self.name


class Mobile(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.IntegerField()
    sale = models.IntegerField()
    color = models.CharField(max_length=255)
    type = models.CharField(max_length=255, default='mobile')
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='images/mobiles/')
    producer = models.CharField(max_length=255)

    class Meta:
        db_table = 'mobiles'
        ordering = ['name']
        verbose_name_plural = 'Mobiles'

    def __str__(self):
        return self.name
