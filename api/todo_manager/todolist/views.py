from django.shortcuts import render, redirect, get_object_or_404
from todolist.models import Task
from django.views.decorators.cache import cache_page
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
import json


@login_required
def homepage(request):
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(completed=True).count()
    pending_tasks = total_tasks - completed_tasks
    recent_tasks = Task.objects.all().order_by("-id")[:5]  # Get last 5 tasks

    context = {
        "page_title": "Home Page",
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "recent_tasks": recent_tasks,
    }
    return render(request, "home.html", context)


@login_required
def todolist(request):
    # Server-rendered todo list: handle create via POST, otherwise render tasks
    if request.method == "POST":
        # create a new task from form
        text = request.POST.get("task", "").strip()
        if text:
            t = Task.objects.create(task=text, completed=False)
            messages.success(request, f"Task '{t.task}' created.")
        else:
            messages.error(request, "Task cannot be empty.")
        return redirect("todolist")

    task = Task.objects.all().order_by("id")
    context = {"page_title": "Todo List Page", "tasks": task}
    return render(request, "todolist.html", context)


@login_required
def toggle_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)
        task.completed = not task.completed
        task.save()
        messages.success(
            request,
            f"Task '{task.task}' marked {'completed' if task.completed else 'pending'}.",
        )
    return redirect("todolist")


@cache_page(5)  # cache the task list briefly (seconds)
def api_tasks(request):
    if request.method == "GET":
        qs = Task.objects.all().order_by("id")
        data = [{"id": t.id, "task": t.task, "completed": t.completed} for t in qs]
        return JsonResponse(data, safe=False)
    return HttpResponseNotAllowed(["GET"])


def api_create_task(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body.decode())
        except Exception:
            payload = request.POST
        task_text = payload.get("task", "").strip()
        if not task_text:
            return JsonResponse({"error": "Task cannot be empty."}, status=400)
        t = Task.objects.create(task=task_text, completed=False)
        return JsonResponse({"id": t.id, "task": t.task, "completed": t.completed})
    return HttpResponseNotAllowed(["POST"])


def api_update_task(request, task_id):
    if request.method in ["POST", "PUT"]:
        task = get_object_or_404(Task, id=task_id)
        try:
            payload = json.loads(request.body.decode())
        except Exception:
            payload = request.POST
        task_text = payload.get("task")
        if task_text is not None:
            task.task = task_text
        if "completed" in payload:
            task.completed = bool(payload.get("completed"))
        task.save()
        return JsonResponse(
            {"id": task.id, "task": task.task, "completed": task.completed}
        )
    return HttpResponseNotAllowed(["POST", "PUT"])


def api_delete_task(request, task_id):
    if request.method in ["POST", "DELETE"]:
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return JsonResponse({"status": "ok"})
    return HttpResponseNotAllowed(["POST", "DELETE"])


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        text = request.POST.get("task", "").strip()
        if text:
            task.task = text
            task.save()
            messages.success(request, f"Task updated successfully!")
        else:
            messages.error(request, "Task cannot be empty.")
        return redirect("todolist")
    context = {"task": task}
    return render(request, "edit_task.html", context)


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task_name = task.task
    task.delete()
    messages.success(request, f"Task '{task_name}' deleted successfully!")
    return redirect("todolist")


def contact(request):
    context = {"page_title": "Contact Page"}
    return render(request, "contact.html", context)


def about(request):
    context = {"page_title": "About Page"}
    return render(request, "about.html", context)


# Create your views here.

# Create your views here.
