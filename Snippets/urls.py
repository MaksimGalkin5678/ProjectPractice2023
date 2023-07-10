from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page),
    path('add_snippet/', views.add_snippet_page, name='add_snippets'),
    path('view_snippets/', views.snippets_page, name='view_snippets'),
    path('add_snippet/', views.create_snippet, name='create_snippet'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
