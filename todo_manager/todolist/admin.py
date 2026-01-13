from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils.html import format_html
from django.utils import timezone
from .models import Task, Review, LoginHistory


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("task", "user", "completed", "priority", "created_at", "updated_at")
    list_filter = ("completed", "priority", "created_at", "updated_at")
    search_fields = ("task", "user__username")
    ordering = ("-created_at",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "review_type", "rating", "comment", "created_at")
    list_filter = ("review_type", "rating", "created_at")
    search_fields = ("user__username", "comment")
    ordering = ("-created_at",)


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "ip_address", "login_time", "location", "user_agent_short")
    list_filter = ("login_time", "user")
    search_fields = ("user__username", "ip_address", "user_agent")
    readonly_fields = ("user", "ip_address", "user_agent", "login_time", "location")

    def user_agent_short(self, obj):
        return (
            obj.user_agent[:50] + "..." if len(obj.user_agent) > 50 else obj.user_agent
        )

    user_agent_short.short_description = "User Agent"


# Custom admin dashboard
class CustomAdminSite(admin.AdminSite):
    site_header = "TaskMaster Administration"
    site_title = "TaskMaster Admin"
    index_title = "Welcome to TaskMaster Admin Dashboard"

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)

        # Add custom statistics
        if app_label is None:
            # User statistics
            total_users = User.objects.count()
            active_users = User.objects.filter(is_active=True).count()
            superusers = User.objects.filter(is_superuser=True).count()

            # Task statistics
            total_tasks = Task.objects.count()
            completed_tasks = Task.objects.filter(completed=True).count()
            pending_tasks = total_tasks - completed_tasks

            # Review statistics
            total_reviews = Review.objects.count()
            website_reviews = Review.objects.filter(review_type="website").count()
            todolist_reviews = Review.objects.filter(review_type="todolist").count()

            # Login statistics
            total_logins = LoginHistory.objects.count()
            recent_logins = LoginHistory.objects.filter(
                login_time__date__gte=timezone.now().date() - timezone.timedelta(days=7)
            ).count()

            # Add custom app for statistics
            stats_app = {
                "name": "Statistics",
                "app_label": "statistics",
                "app_url": "#",
                "has_module_perms": True,
                "models": [
                    {
                        "name": "User Analytics",
                        "object_name": "UserAnalytics",
                        "perms": {
                            "add": False,
                            "change": False,
                            "delete": False,
                            "view": True,
                        },
                        "admin_url": None,
                        "add_url": None,
                        "view_only": True,
                        "model_count": format_html(
                            """
                        <div style="padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; margin: 10px 0;">
                            <h4 style="margin: 0 0 10px 0;">📊 User Statistics</h4>
                            <p style="margin: 5px 0;"><strong>Total Users:</strong> {}</p>
                            <p style="margin: 5px 0;"><strong>Active Users:</strong> {}</p>
                            <p style="margin: 5px 0;"><strong>Superusers:</strong> {}</p>
                            <p style="margin: 5px 0;"><strong>Total Logins:</strong> {}</p>
                            <p style="margin: 5px 0;"><strong>Recent Logins (7 days):</strong> {}</p>
                        </div>
                        <div style="padding: 15px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; border-radius: 8px; margin: 10px 0;">
                            <h4 style="margin: 0 0 10px 0;">📝 Task Statistics</h4>
                            <p style="margin: 5px 0;"><strong>Total Tasks:</strong> {}</p>
                            <p style="margin: 5px 0;"><strong>Completed:</strong> {} ({:.1f}%)</p>
                            <p style="margin: 5px 0;"><strong>Pending:</strong> {} ({:.1f}%)</p>
                        </div>
                        <div style="padding: 15px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; border-radius: 8px; margin: 10px 0;">
                            <h4 style="margin: 0 0 10px 0;">⭐ Review Statistics</h4>
                            <p style="margin: 5px 0;"><strong>Total Reviews:</strong> {}</p>
                            <p style="margin: 5px 0;"><strong>Website Reviews:</strong> {}</p>
                            <p style="margin: 5px 0;"><strong>Todolist Reviews:</strong> {}</p>
                        </div>
                    """,
                            total_users,
                            active_users,
                            superusers,
                            total_logins,
                            recent_logins,
                            total_tasks,
                            completed_tasks,
                            (
                                (completed_tasks / total_tasks * 100)
                                if total_tasks > 0
                                else 0
                            ),
                            pending_tasks,
                            (
                                (pending_tasks / total_tasks * 100)
                                if total_tasks > 0
                                else 0
                            ),
                            total_reviews,
                            website_reviews,
                            todolist_reviews,
                        ),
                    }
                ],
            }

            app_list.insert(0, stats_app)

        return app_list


# Create custom admin site
custom_admin_site = CustomAdminSite(name="custom_admin")
custom_admin_site.register(Task, TaskAdmin)
custom_admin_site.register(Review, ReviewAdmin)
custom_admin_site.register(LoginHistory, LoginHistoryAdmin)

# The models are already registered with decorators above
