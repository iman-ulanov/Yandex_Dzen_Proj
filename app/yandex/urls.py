from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts import views as acc_views
from posts.views import PostViewSet

acc_router = DefaultRouter()
acc_router.register('register', acc_views.AuthorRegisterAPIView)
post_router = DefaultRouter()
post_router.register('posts', PostViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),

    path('api/accounts/', include(acc_router.urls)),
    path('api/', include(post_router.urls)),


]
