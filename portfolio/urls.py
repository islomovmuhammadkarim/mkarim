from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('works/', views.works, name='works'),  # oxirida / qo'shildi
    path('contact/', views.contact, name='contact'),  # home emas, alohida view
    path('credentials/', views.credentials, name='credentials'),  # alohida view kerak
    path('works/', views.works, name='works'),
    path('works/<slug:slug>/', views.work_details, name='work_details'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_details'),
    path('blog/<slug:slug>/add-comment/', views.add_comment, name='add_comment'),
    path('services/', views.service_view, name='services'),
]


