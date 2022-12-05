from django.db import models


class Pdf(models.Model):
    name = models.CharField(max_length=50, blank=False, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name + " " + self.author