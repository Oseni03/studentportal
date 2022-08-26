from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST, require_GET 

from .models import Note, HomeWork, Todo
from .forms import NoteForm, HomeWorkForm, TodoForm, ConversionForm, ConversionLengthForm, ConversionMassForm, UserRegistrationForm

from youtubesearchpython import VideosSearch
import requests, wikipedia

# Create your views here.
class HomeView(generic.TemplateView):
  template_name = "dashboard/home.html"

class NoteView(LoginRequiredMixin, generic.FormView):
  form_class = NoteForm
  success_url = "/notes/"
  
  def get_context_data(self):
    context = super().get_context_data()
    context["notes"] = Note.objects.filter(user=self.request.user)
    return context
  
  def form_valid(self, form):
    note = form.save(commit=False)
    note.user = self.request.user
    note.save()
    messages.success(self.request, "Note added successfully")
    return super().form_valid(form)
  
  def get_template_names(self):
    if self.request.htmx:
      return "dashboard/partials/notes_element.html"
    # super().get_template_names()
    return "dashboard/notes.html"


@login_required
def delete_note(request, pk):
  note = Note.objects.get(id=pk).delete()
  notes = Note.objects.filter(user=request.user)
  context = {
    "notes": notes,
  }
  return render(request, "dashboard/partials/notes_list.html", context)


class NoteDetailView(LoginRequiredMixin, generic.DetailView):
  model = Note 
  template_name = "dashboard/notes_detail.html"
  context_object_name = "note"


@login_required
def update_note(request, pk):
  note = Note.objects.get(id=pk)
  form = NoteForm(instance=note)
  if request.POST:
    form = NoteForm(request.POST, instance=note)
    if form.is_valid():
      form.save()
      messages.success(request, "Note updtaed successfully")
      return redirect(note)
      
  context = {
    "note": note,
    "form": form,
  }
  return render(request, "dashboard/partials/note_update_form.html", context)


class HomeWorkView(LoginRequiredMixin, generic.FormView):
  form_class = HomeWorkForm
  
  def get_context_data(self):
    context = super().get_context_data()
    context["homeworks"] = HomeWork.objects.filter(user=self.request.user)
    return context
  
  def form_valid(self, form):
    work = form.save(commit=False)
    work.user = self.request.user
    work.save()
    messages.success(self.request, "Homework added successfully")
    return super().form_valid(form)
  
  def form_invalid(self, form):
    for error in form.errors:
        messages.error(self.request, error)
    result = super(HomeWorkView, self).form_invalid(form)
    return result
  
  def get_template_names(self):
    if self.request.htmx:
      return "dashboard/partials/homeworks_list.html"
    # super().get_template_names()
    return "dashboard/homework.html"
  
  def get_success_url(self):
    return reverse("dashboard:homeworks")

@login_required
def complete_homework(request, pk):
  work = HomeWork.objects.get(id=pk)
  if work.is_finished:
    work.is_finished=False 
  else:
    work.is_finished=True 
  work.save()
  
  context = {
    "homeworks": HomeWork.objects.filter(user=request.user)
  }
  return render(request, "dashboard/partials/homeworks_list.html", context)


@login_required
def delete_homework(request, pk):
  work = HomeWork.objects.get(id=pk).delete()
  
  context = {
    "homeworks": HomeWork.objects.filter(user=request.user)
  }
  return render(request, "dashboard/partials/homeworks_list.html", context)


class YouTubeView(generic.TemplateView):
  template_name = "dashboard/youtube.html"
  
  def post(self, *args, **kwargs):
    text = self.request.POST.get("search")
    videos = VideosSearch(text, limit=10)
    print(videos.result()["result"])
    results = []
    for i in videos.result()["result"]:
      result_dict = {
        "text": text,
        "title": i["title"],
        "link": i["link"],
        "duration": i["duration"],
        "thumbnail": i["thumbnails"][0]["url"],
        "channel": i["channel"]["name"],
        "views": i["viewCount"]["short"],
        "published": i["publishedTime"],
      }
      desc = ""
      if i["descriptionSnippet"]:
        for j in i["descriptionSnippet"]:
          desc += j["text"]
      result_dict["description"] = desc 
      results.append(result_dict)
    context = {
      "results": results,
    }
    return render(self.request, "dashboard/youtube.html", context)


class TodoView(LoginRequiredMixin, generic.FormView):
  form_class = TodoForm 
  
  def get_context_data(self):
    context = super().get_context_data()
    context["tasks"] = Todo.objects.filter(user=self.request.user)
    return context
  
  def form_valid(self, form):
    task = form.save(commit=False)
    task.user = self.request.user
    task.save()
    messages.success(self.request, "Task added successfully")
    return super().form_valid(form)
  
  def form_invalid(self, form):
    for error in form.errors:
        messages.error(self.request, error)
    result = super(TodoView, self).form_invalid(form)
    return result
  
  def get_template_names(self):
    if self.request.htmx:
      return "dashboard/partials/todo_list.html"
    # super().get_template_names()
    return "dashboard/todo.html"
  
  def get_success_url(self):
    return reverse("dashboard:todo")


@login_required
def complete_task(request, pk):
  task = Todo.objects.get(id=pk)
  if task.is_done:
    task.is_done=False 
  else:
    task.is_done=True 
  task.save()
  
  context = {
    "tasks": Todo.objects.filter(user=request.user)
  }
  return render(request, "dashboard/partials/todo_list.html", context)


@login_required
def delete_task(request, pk):
  task = Todo.objects.get(id=pk).delete()
  
  context = {
    "tasks": Todo.objects.filter(user=request.user)
  }
  return render(request, "dashboard/partials/todo_list.html", context)


class BooksView(LoginRequiredMixin, generic.TemplateView):
  template_name = "dashboard/books.html"
  
  def post(self, *args, **kwargs):
    text = self.request.POST.get("search")
    url = "https://www.googleapis/books/v1/volumes/q?"+text 
    r= requests.get(url)
    answer = r.json()
    result_list = []
    for i in range(10):
      result_dict = {
        "title": answer["items"][i]["volumeInfo"]["title"],
        "subtitle": answer["items"][i]["volumeInfo"].get("subtitle"),
        "description": answer["items"][i]["volumeInfo"].get("description"),
        "count": answer["items"][i]["volumeInfo"].get("pageCount"),
        "categories": answer["items"][i]["volumeInfo"].get("categories"),
        "rating": answer["items"][i]["volumeInfo"].get("pageRating"),
        "thumbnail": answer["items"][i]["volumeInfo"].get("imageLink").get("thumbnail"),
        "preview": answer["items"][i]["volumeInfo"].get("previewLink"),
      }
      result_list.append(result_dict)
    context = {
      "results": result_list,
    }
    return render(self.request, "dashboard/books.html", context)


class DictionaryView(generic.TemplateView):
  template_name = "dashboard/dictionary.html"
  
  def post(self, *args, **kwargs):
    text = self.request.POST.get("search")
    url = "https://www.api.dictionaryapi.dev/api/v2/entries/en_US/"+text 
    r= requests.get(url)
    answer = r.json()
    try:
      phonetics = answer[0]["phonetics"][0]["text"],
      audio = answer[0]["phonetics"][0]["audio"],
      definition = answer[0]["meanings"][0]["definitions"][0]["definition"]
      example = answer[0]["meanings"][0]["definitions"][0]["example"]
      synonyms = answer[0]["meanings"][0]["definitions"][0]["synonyms"]
      
      context = {
        "input": text,
        "phonetics": phonetics,
        "definition": definition,
        "audio": audio,
        "example": example,
        "synonyms": synonyms,
      }
    except:
      context = {
        "input": text,
      }
    return render(self.request, "dashboard/dictionary.html", context)


class WikipediaView(generic.TemplateView):
  template_name = "dashboard/wiki.html"
  
  def post(self, *args, **kwargs):
    text = self.request.POST.get("search")
    search = wikipedia.page(text)
    context = {
      "title": search.title,
      "link": search.url,
      "details": search.summary,
    }
    return render(self.request, "dashboard/wiki.html", context)


class ConversionView(generic.TemplateView):
  template_name = "dashboard/conversion.html"
  
  def get_context_data(self):
    context = super().get_context_data()
    context["form"] = ConversionForm()
    return context 
  
  def post(self, *args, **kwargs):
    form = ConversionForm(self.request.POST)
    if self.request.POST["measurement"] == "length":
      measurement_form = ConversionLengthForm()
      context = self.get_context_data()
      context["form"] = form 
      context["m_form"] = measurement_form
      context["input"] = True 
      
    if self.request.POST["measurement"] == "mass":
      measurement_form = ConversionMassForm()
      context = self.get_context_data()
      context["form"] = form 
      context["m_form"] = measurement_form
      context["input"] = True 
      
    return render(self.request, "dashboard/partials/conversion_element.html", context)


def conversion_result(request):
  if "input" in request.POST:
    first = request.POST["measure1"]
    second = request.POST["measure2"]
    input = request.POST["input"]
    answer = ""
    if input and int(input) >= 0:
      if first == "yard" and second == "foot":
        answer = f"{input} yard = {int(input) * 3} foot"
      elif first == "foot" and second == "yard":
        answer = f"{input} foot = {int(input) / 3} yard"
      elif first == "pound" and second == "kilogram":
        answer = f"{input} pound = {int(input) * 0.453592} kilogram"
      elif first == "kilogram" and second == "pound":
        answer = f"{input} kilogram = {int(input) * 2.2062} pound"
  return HttpResponse(answer)


def check_username(request):
  username = request.POST.get("username")
  if get_user_model().objects.filter(username=username).exits():
    return HttpResponse("<div style='color: red;'>This user already exit</div>")
  else:
    return HttpResponse("<div style='color: green;'>This username is available</div>")


class CreateUserView(SuccessMessageMixin, generic.CreateView):
  template_name="register.html"
  form_class=UserRegistrationForm
  model=User 
  success_message = "Login successful"
  
  def form_valid(self, form):
    user = form.save(commit=False)
    user.set_password(user.password)
    user.save()
    return super(CreateUserView, self).form_valid(form) 
  
  def get_success_url(self):
    return reverse("login")
  

@require_POST
def check_username(request):
  username = request.POST.get("username")
  if get_user_model().objects.filter(username=username):
    return HttpResponse("<div style='color: red;'>This username already exit</div>")
  else:
    return HttpResponse("<div style='color: green;'>Available</div>")


@require_POST
def check_password(request):
  password1 = request.POST.get("password1")
  password2 = request.POST.get("password2")
  if password1 != password2:
    return HttpResponse("<div style='color: red;'>Password not match</div>")
  else:
    return HttpResponse("<div style='color: green;'>Password match</div>")


@require_POST
def check_login_username(request):
  username = request.POST.get("username")
  if get_user_model().objects.filter(username=username):
    return HttpResponse("<div style='color: green;'>Valid</div>")
  else:
    return HttpResponse("<div style='color: red;'>This username does not exit</div>")


class ProfileView(LoginRequiredMixin, generic.TemplateView):
  template_name = "dashboard/profile.html"
  
  def get_context_data(self):
    context = super().get_context_data()
    context["tasks"] = Todo.objects.filter(user=self.request.user, is_done=False)
    context["homeworks"] = HomeWork.objects.filter(user=self.request.user, is_finished=False)
    return context