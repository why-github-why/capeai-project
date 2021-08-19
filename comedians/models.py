from django.db import models

class Comedian(models.Model):
   username = models.CharField(max_length=100, default='Leon', null=True)
   inspiration = models.CharField(max_length=100, default='Politics', null=True)
   joke_of_the_day = models.TextField(default='Why are there gates around cemeteries? Because people are dying to get in!')

   def __str__(self):
      return self.username.capitalize()
