from django.urls import path, include
from django.views import generic
from . import views

app_name = "dashboard"

urlpatterns = [
  path("", views.HomeView.as_view(), name="home"),
  path("notes/", views.NoteView.as_view(), name="notes"),
  path("note-detail/<int:pk>/", views.NoteDetailView.as_view(), name="note-detail"),
  path("homeworks/", views.HomeWorkView.as_view(), name="homeworks"),
  path("youtube/", views.YouTubeView.as_view(), name="youtube"),
  path("todo/", views.TodoView.as_view(), name="todo"),
  path("books/", views.BooksView.as_view(), name="books"),
  path("dictionary/", views.DictionaryView.as_view(), name="dictionary"),
  path("wikipedia/", views.WikipediaView.as_view(), name="wikipedia"),
  path("conversion/", views.ConversionView.as_view(), name="conversion"),
  path("profile/", views.ProfileView.as_view(), name="profile"),
]

htmx_url = [
  path("delete-note/<int:pk>/", views.delete_note, name="delete-note"),
  path("update-note/<int:pk>/", views.update_note, name="update-note"),
  path("complete-homework/<int:pk>/", views.complete_homework, name="complete-homework"),
  path("delete-homework/<int:pk>/", views.delete_homework, name="delete-homework"),
  path("complete-task/<int:pk>/", views.complete_task, name="complete-task"),
  path("delete-task/<int:pk>/", views.delete_task, name="delete-task"),
  path("conversion-result/", views.conversion_result, name="conversion-result"),
  path("check-username/", views.check_username, name="check-username"),
  path("check-password/", views.check_password, name="check-password"),
  path("check-login-username/", views.check_login_username, name="check-login-username"),
]

urlpatterns += htmx_url