from django.db import models




class Color(models.Model):
    colors_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.colors_name
class Person(models.Model):
    color = models.ForeignKey(Color,null=True,on_delete=models.CASCADE , related_name='color')
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    
