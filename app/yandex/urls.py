from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


from accounts import views as acc_views
from posts.views import PostViewSet
from posts.views import CommentListCreateAPIView
from posts.views import CommentRetrieveUpdateDestroyAPIView
from posts.views import RatePostViewSet

acc_router = DefaultRouter()
acc_router.register('register', acc_views.AuthorRegisterViewSet)
post_router = DefaultRouter()
post_router.register('posts', PostViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Yandex Dzen",
        default_version='v-1.0',
        description="API для yandex dzen",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ulanoviman3@gmail.com"),
        license=openapi.License(name="No Licence"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),

    path('api/accounts/', include(acc_router.urls)),
    path('api/', include(post_router.urls)),
    path('api/posts/<int:post_id>/comments/', CommentListCreateAPIView.as_view()),
    path('api/posts/<int:post_id>/comments/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view()),
    path('api/posts/<int:post_id>/rate/', RatePostViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),

    # documentation URL
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_doc'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc_doc'),

]
