from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User 

# Create your models here.
class Note(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  description = models.TextField()
  
  class Meta:
    verbose_name = "Note"
    verbose_name_plural = "Notes"
  
  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
    return reverse("dashboard:note-detail", args=[self.pk])


class HomeWork(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  subject = models.CharField(max_length=50)
  title = models.CharField(max_length=200)
  description = models.TextField()
  due = models.DateField()
  is_finished = models.BooleanField(default=False)
  
  def __str__(self):
    return self.title


class Todo(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=100)
  is_done = models.BooleanField(default=False)
  
  def __str__(self):
    return self.title