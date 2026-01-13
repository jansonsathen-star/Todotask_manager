from todo_manager.todo_manager.settings import *

# Override for Vercel
DEBUG = False
ALLOWED_HOSTS = ["*"]

# Use SQLite for Vercel
DATABASES["default"] = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": ":memory:",
}
