from django.db import models

class Cameras(models.Model):
    ip = models.TextField()
    descricao = models.TextField()
    

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name_plural = 'Cameras'
