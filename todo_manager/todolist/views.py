from django.shortcuts import render, redirect, get_object_or_404
from todolist.models import Task, Review
from django.views.decorators.cache import cache_page
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import json


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, f"Welcome {user.username}! Your account has been created."
            )
            return redirect("homepage")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def homepage(request):
    user_tasks = Task.objects.filter(user=request.user)
    total_tasks = user_tasks.count()
    completed_tasks = user_tasks.filter(completed=True).count()
    pending_tasks = total_tasks - completed_tasks
    recent_tasks = user_tasks.order_by("-id")[:5]  # Get last 5 tasks

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
        priority = request.POST.get("priority", "medium")
        if text:
            t = Task.objects.create(
                user=request.user, task=text, completed=False, priority=priority
            )
            messages.success(request, f"Task '{t.task}' created.")
        else:
            messages.error(request, "Task cannot be empty.")
        return redirect("todolist")

    # Handle search and filtering
    search_query = request.GET.get("search", "")
    status_filter = request.GET.get("status", "")
    priority_filter = request.GET.get("priority", "")

    tasks = Task.objects.filter(user=request.user)

    if search_query:
        tasks = tasks.filter(task__icontains=search_query)

    if status_filter:
        if status_filter == "completed":
            tasks = tasks.filter(completed=True)
        elif status_filter == "pending":
            tasks = tasks.filter(completed=False)

    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)

    tasks = tasks.order_by("-created_at")

    context = {
        "page_title": "Todo List Page",
        "tasks": tasks,
        "search_query": search_query,
        "status_filter": status_filter,
        "priority_filter": priority_filter,
    }
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
        priority = request.POST.get("priority", task.priority)
        if text:
            task.task = text
            task.priority = priority
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


@login_required
def submit_review(request, review_type):
    if review_type not in ["website", "todolist"]:
        return redirect("home")

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment", "").strip()

        if not rating or not rating.isdigit() or int(rating) not in range(1, 6):
            messages.error(request, "Please select a valid rating (1-5 stars).")
            return redirect(request.META.get("HTTP_REFERER", "home"))

        rating = int(rating)

        # Check if user already reviewed this type
        existing_review = Review.objects.filter(
            user=request.user, review_type=review_type
        ).first()
        if existing_review:
            existing_review.rating = rating
            existing_review.comment = comment
            existing_review.save()
            messages.success(request, f"Your {review_type} review has been updated!")
        else:
            Review.objects.create(
                user=request.user,
                rating=rating,
                comment=comment,
                review_type=review_type,
            )
            messages.success(request, f"Thank you for your {review_type} review!")

        return redirect(request.META.get("HTTP_REFERER", "home"))

    return redirect("home")


@login_required
def reviews(request):
    website_reviews = Review.objects.filter(review_type="website").order_by(
        "-created_at"
    )
    todolist_reviews = Review.objects.filter(review_type="todolist").order_by(
        "-created_at"
    )

    # Calculate averages
    website_avg = website_reviews.aggregate(avg=models.Avg("rating"))["avg"] or 0
    todolist_avg = todolist_reviews.aggregate(avg=models.Avg("rating"))["avg"] or 0

    context = {
        "page_title": "Reviews",
        "website_reviews": website_reviews,
        "todolist_reviews": todolist_reviews,
        "website_avg": round(website_avg, 1),
        "todolist_avg": round(todolist_avg, 1),
    }
    return render(request, "reviews.html", context)


# Create your views here.

# Create your views here.
