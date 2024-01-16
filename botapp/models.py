from django.db import models


class TgUser(models.Model):
    username = models.CharField(max_length=555, blank=True, null=True)
    first_name = models.CharField(max_length=555, blank=True, null=True)
    last_name = models.CharField(max_length=555, blank=True, null=True)
    tg_id = models.BigIntegerField(unique=True)
    reg_date = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        if self.username:
            return self.username
        return self.first_name


class Category(models.Model):
    name = models.CharField(max_length=88)
    icon = models.CharField(max_length=255)


class Product(models.Model):
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    price = models.PositiveBigIntegerField(default=0)
    image = models.ImageField(upload_to="images")
    text = models.TextField(blank=True)


class Words(models.Model):
    english = models.CharField(max_length=255)
    uzbek = models.CharField(max_length=255)

    v1 = models.CharField(max_length=255, null=True, blank=True)
    v2 = models.CharField(max_length=255, null=True, blank=True)
    v3 = models.CharField(max_length=255, null=True, blank=True)
    v4 = models.CharField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    used = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "So'zlar"
        verbose_name = "So'z"

    def __str__(self) -> str:
        return self.english + " - " + self.uzbek
    



    



