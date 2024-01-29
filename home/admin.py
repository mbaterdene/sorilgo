from django.contrib import admin
from .models import lesson_status, teacher_status, tuslamj, user_info, home_info, about_us, angi_info, angi, testimonial, clients, services, lesson_with_video, blog_post, User
from django.contrib.auth import get_user_model
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from mcq.models import MCQQuestion, Answer
from quiz.models import Quiz, Category, Question, Progress, Level, Sitting

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

admin.site.site_header = 'BOD.MN сайтны админ'
admin.site.site_title = "СОРИЛГО.МН"
admin.site.index_title = "СОРИЛГО.МН-д тавтай морил. Танд энэ өдрийн мэнд хүргэе."

class PostAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['queryset'] = get_user_model().objects.filter(username=request.user.username)
        return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    list_display = ('title', 'description', 'author', 'submision_date', )

class AnswerInline(admin.TabularInline):
    model = Answer

class QuizAdminForm(forms.ModelForm):
    class Meta:
        model = Quiz
        exclude = []

    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all().select_subclasses(),
        required=False,
        label="Questions",
        widget=FilteredSelectMultiple(
            verbose_name="Questions",
            is_stacked=False))

    def __init__(self, *args, **kwargs):
        super(QuizAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['questions'].initial = \
                self.instance.question_set.all().select_subclasses()

    def save(self, commit=True):
        quiz = super(QuizAdminForm, self).save(commit=False)
        quiz.save()
        quiz.question_set.set(self.cleaned_data['questions'])
        self.save_m2m()
        return quiz

def single_active(ModelAdmin,request, queryset):
    queryset.update(single_attempt = 'True')
def single_not_active(ModelAdmin,request, queryset):
    queryset.update(single_attempt = 'False')
def draft_active(ModelAdmin,request, queryset):
    queryset.update(draft = 'True')
def draft_not_active(ModelAdmin,request, queryset):
    queryset.update(draft = 'False')

class QuizAdmin(admin.ModelAdmin):
    form = QuizAdminForm
    list_display = ('title', 'description', 'url', 'exam_paper', 'draft','single_attempt', 'answers_at_end',)
    search_fields = ('description', )
    # list_editable = ('description', 'url','exam_paper', 'draft','single_attempt', 'answers_at_end')
    actions = [single_active, single_not_active, draft_active, draft_not_active]

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('category', )

class LevelAdmin(admin.ModelAdmin):
    search_fields = ('level', )

class MCQuestionAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['queryset'] = get_user_model().objects.filter(username=request.user.username)
        return super(MCQuestionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    list_display = ('content', 'quiz_get', 'explanation', 'video', 'level', 'point', 'author', )
    def quiz_get(self, obj):
        return "\n".join([p.title for p in obj.quiz.all()])
    list_filter = ('category', 'level', 'point', 'explanation', )
    fields = ('content', 'category', 'level', 'point',
              'figure', 'video', 'quiz', 'explanation', 'answer_order', 'author',)

    # search_fields = ('content', 'explanation', 'point', 'author',)
    filter_horizontal = ('quiz',)
    
    inlines = [AnswerInline]

class ProgressAdmin(admin.ModelAdmin):
    search_fields = ('user', 'score', )

def user_active(ModelAdmin,request, queryset):
    queryset.update(is_active = 'True')
def user_not_active(ModelAdmin,request, queryset):
    queryset.update(is_active = 'False')
def user_staff(ModelAdmin,request, queryset):
    queryset.update(is_staff = 'True')
def user_not_staff(ModelAdmin,request, queryset):
    queryset.update(is_staff = 'False')

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

class AngiAdmin(admin.ModelAdmin):
    list_display = ('angi_info', 'teacher')
    filter_horizontal = ('students',)

class userModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'phone', 'image']
    list_filter = ['gender']

admin.site.register(tuslamj)
admin.site.register(Level, LevelAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(MCQQuestion, MCQuestionAdmin)
# admin.site.register(Progress, ProgressAdmin)
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, LessonInline, TeacherInline, )
    list_display = ('username', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active', 'last_login','date_joined')
    actions = [user_active, user_not_active, user_staff, user_not_staff]
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )

admin.site.unregister(Group)
admin.site.register(Sitting)
admin.site.register(Progress)
admin.site.register(home_info)
admin.site.register(about_us)
admin.site.register(testimonial)
admin.site.register(clients)
admin.site.register(services)
admin.site.register(lesson_with_video)
admin.site.register(blog_post, PostAdmin)
admin.site.register(angi_info, AngiAdmin)
admin.site.register(angi)
admin.site.register(user_info, userModelAdmin)
