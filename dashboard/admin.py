from django.contrib import admin
from .models import Note, HomeWork

# Register your models here.
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
  list_display = ("id", "user", "title")

@admin.register(HomeWork)
class HomeWorkAdmin(admin.ModelAdmin):
  list_display = ("id", "user","subject", "title")