from django.contrib import admin
from .models import Profile, teacher_status, lesson_status, user_info, User, whatsgrade, price_test
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin


def user_active(ModelAdmin,request, queryset):
    queryset.update(is_active = 'True')
def user_not_active(ModelAdmin,request, queryset):
    queryset.update(is_active = 'False')
def user_staff(ModelAdmin,request, queryset):
    queryset.update(is_staff = 'True')
def user_not_staff(ModelAdmin,request, queryset):
    queryset.update(is_staff = 'False')

class TestInline(admin.StackedInline):
    model = price_test
    can_delete = False
    verbose_name_plural = 'Тест ажиллах эрх'
    fk_name = 'user'

class GradeInline(admin.StackedInline):
    model = whatsgrade
    can_delete = False
    verbose_name_plural = 'Ангийн мэдээлэл'
    fk_name = 'user'

class TeacherInline(admin.StackedInline):
    model = teacher_status
    can_delete = False
    verbose_name_plural = 'Багш эсэх'
    fk_name = 'user'

class LessonInline(admin.StackedInline):
    model = lesson_status
    can_delete = False
    verbose_name_plural = 'Хичээл үзэх эрхтэй эсэх'
    fk_name = 'user'

class ProfileInline(admin.StackedInline):
    model = user_info
    can_delete = False
    verbose_name_plural = 'Нэмэлт мэдээлэл'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, LessonInline, TeacherInline, GradeInline, TestInline, )
    list_display = ('username', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active', 'last_login')
    actions = [user_active, user_not_active, user_staff, user_not_staff]
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff')}),
    )

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'phone', 'add_info')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'signup_confirmation')
    list_editable = ['signup_confirmation']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(user_info,UserInfoAdmin)
admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
