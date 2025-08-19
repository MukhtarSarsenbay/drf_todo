from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.response import Response   # 👈 add this import
from .models import Todo, Category
from .serializers import TodoSerializer, CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def list(self, request, *args, **kwargs):
        cached_data = cache.get("todos")
        if cached_data:
            return Response(cached_data) 

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        cache.set("todos", serializer.data, timeout=60)
        return Response(serializer.data)
