from django.db import models


class Img(models.Model):
    img = models.ImageField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        self.img.delete()
        return super().delete(using=using, keep_parents=keep_parents)
    