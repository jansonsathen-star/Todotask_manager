from django.urls import path
from todolist import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name="register"),
    path("todolist/", views.todolist, name="todolist"),
    path("todolist/toggle/<int:task_id>/", views.toggle_task, name="toggle_task"),
    path("edit_task/<int:task_id>/", views.edit_task, name="edit_task"),
    path("delete_task/<int:task_id>/", views.delete_task, name="delete_task"),
    # API endpoints used by React frontend (no DRF)
    path("todolist/api/tasks/", views.api_tasks, name="api_tasks"),
    path("todolist/api/tasks/create/", views.api_create_task, name="api_create_task"),
    path(
        "todolist/api/tasks/<int:task_id>/update/",
        views.api_update_task,
        name="api_update_task",
    ),
    path(
        "todolist/api/tasks/<int:task_id>/delete/",
        views.api_delete_task,
        name="api_delete_task",
    ),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("submit_review/<str:review_type>/", views.submit_review, name="submit_review"),
    path("reviews/", views.reviews, name="reviews"),
]
