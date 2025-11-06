from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "is_verified", "is_staff", "date_joined")
    list_filter = ("is_staff", "is_verified")
    search_fields = ("email", "username", "full_name")
    ordering = ("-date_joined",)
    readonly_fields = ("date_joined", "last_login")

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Personal Info", {"fields": ("full_name",)}),
        ("Security", {"fields": ("is_verified")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {"fields": ("email", "username", "password1", "password2")}),
    )

    actions = ["enable_2fa", "disable_2fa"]

    def enable_2fa(self, request, queryset):
        updated = queryset.update(two_factor_enabled=True)
        self.message_user(request, f"{updated} users: 2FA enabled.")
    enable_2fa.short_description = "Enable 2FA for selected users"

    def disable_2fa(self, request, queryset):
        updated = queryset.update(two_factor_enabled=False)
        self.message_user(request, f"{updated} users: 2FA disabled.")
    disable_2fa.short_description = "Disable 2FA for selected users"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "updated_at")
    search_fields = ("user__email", "phone_number")



