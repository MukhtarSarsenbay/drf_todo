from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Todo, Category


class TodoTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Work")

    def test_create_todo(self):
        response = self.client.post(
            "/api/todos/",
            {"title": "Test Todo", "description": "Details", "category": self.category.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 1)
        self.assertEqual(Todo.objects.get().title, "Test Todo")

    def test_list_todos(self):
        Todo.objects.create(title="Todo1", category=self.category)
        Todo.objects.create(title="Todo2", category=self.category)
        response = self.client.get("/api/todos/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_todo(self):
        todo = Todo.objects.create(title="Old", category=self.category)
        response = self.client.put(
            f"/api/todos/{todo.id}/",
            {"title": "Updated", "category": self.category.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        todo.refresh_from_db()
        self.assertEqual(todo.title, "Updated")

    def test_delete_todo(self):
        todo = Todo.objects.create(title="Delete me", category=self.category)
        response = self.client.delete(f"/api/todos/{todo.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)


class CategoryTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_category(self):
        response = self.client.post("/api/categories/", {"name": "Personal"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, "Personal")

    def test_list_categories(self):
        Category.objects.create(name="Work")
        Category.objects.create(name="Personal")
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_category(self):
        category = Category.objects.create(name="OldName")
        response = self.client.put(
            f"/api/categories/{category.id}/", {"name": "NewName"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.name, "NewName")

    def test_delete_category(self):
        category = Category.objects.create(name="ToDelete")
        response = self.client.delete(f"/api/categories/{category.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)
