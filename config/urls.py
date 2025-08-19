# config/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todos.views import CategoryViewSet, TodoViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("todos", TodoViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
