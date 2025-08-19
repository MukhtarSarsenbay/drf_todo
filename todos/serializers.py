# todos/serializers.py
from rest_framework import serializers
from .models import Category, Todo
from .utils import decrypt_text

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "parent", "children"]

    def get_children(self, obj):
        return CategorySerializer(obj.children.all(), many=True).data

class TodoSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = ["id", "title", "description", "is_done", "category", "encrypted"]

    def get_description(self, obj):
        if obj.encrypted and obj.description:
            try:
                return decrypt_text(obj.description)
            except Exception:
                return "[CANNOT DECRYPT]"  
        return obj.description