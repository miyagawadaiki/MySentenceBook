from django.urls import path

from . import views


app_name = 'sentences'
urlpatterns = [
    # main
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.UpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),
    # category
    path('category/', views.CategoryIndexView.as_view(), name='cate_index'),
    path('category/create/', views.CategoryCreateView.as_view(), name='cate_create'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='cate_detail'),
    path('category/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='cate_update'),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='cate_delete'),
    # tags
    path('tag/', views.TagIndexView.as_view(), name='tag_index'),
    path('tag/create/', views.TagCreateView.as_view(), name='tag_create'),
    path('tag/<int:pk>/', views.TagDetailView.as_view(), name='tag_detail'),
    path('tag/<int:pk>/update/', views.TagUpdateView.as_view(), name='tag_update'),
    path('tag/<int:pk>/delete/', views.TagDeleteView.as_view(), name='tag_delete'),
]
