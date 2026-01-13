from django.apps import AppConfig


class TodolistConfig(AppConfig):
    name = "todolist"

    def ready(self):
        import todolist.signals
