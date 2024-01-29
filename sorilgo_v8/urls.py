from django.views.static import serve
from django.contrib import admin
from django.urls import path, re_path
import home.views

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from home.views import help_page, QuizMarkingList1, angi, QuizProgressDetail, QuizListView, CategoriesListView,ViewQuizListByCategory, QuizUserProgressView, QuizMarkingList, QuizMarkingDetail, QuizDetailView, QuizTake, login_user, logout_user, QuizUsersProgressView

urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("superhun/ta/moril/", admin.site.urls),
    path("", home.views.home_page, name = 'home_page'),
    path("about/", home.views.about_page, name = 'about_page'),
    path("home/", home.views.home_page, name = 'home_page'),
    path("contact/", home.views.contact_page, name = 'contact_page'),
    path("exam/", home.views.exam_page, name = 'exam_page'),
    path("lesson/", home.views.lesson_page, name = 'lesson_page'),
    path("help/", home.views.help_page, name = 'help_page'),
    path("blog/", home.views.post_page, name = 'post_page'),
    path("blog_get/<int:blog_id>/", home.views.blog_post_get, name = 'blog_post_get'),
    path("angi/<int:teacher_id>/", home.views.angi, name = 'angi_info'),
    path("student_info/<int:pk>/", view=QuizMarkingList1.as_view(), name = 'student_info'),

    path('login/', home.views.login_user, name='login'),
    path('logout/', home.views.logout_user, name='logout'),
    path('quizzes/',view=QuizListView.as_view(),name='quiz_index'),
    path('category/',view=CategoriesListView.as_view(),name='quiz_category_list_all'),
    
    
    path('progress/',view=QuizUserProgressView.as_view(),name='quiz_progress'),
    path('marking/',view=QuizMarkingList.as_view(),name='quiz_marking'),
    
    
    path("category/<slug:category_name>/",view = ViewQuizListByCategory.as_view(),name='quiz_category_list_matching'),
 
    path("marking/<int:pk>/",view=QuizMarkingDetail.as_view(),name='quiz_marking_detail'),
    path("progress/<int:pk>/",view=QuizProgressDetail.as_view(),name='quiz_progress_detail'), 
    path("<slug:slug>/",view=QuizDetailView.as_view(),name='quiz_start_page'),
    path("<slug:quiz_name>/take/",view=QuizTake.as_view(),name='quiz_question'),
]
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
