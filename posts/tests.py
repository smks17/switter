from unittest.mock import Mock, patch
from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from posts.models import Post


@override_settings(USE_KAFKA=False, USE_CACHE=False)
class PostTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")

        self.post1 = Post.objects.create(author=self.user1, content="Post1")
        self.post2 = Post.objects.create(author=self.user1, content="Post2")
        self.post3 = Post.objects.create(author=self.user1, content="Post3")

        self.list_create_url = "/api/v1/social/posts/"

    def test_create_post_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        data = {"content": "New Post Content"}

        response = self.client.post(self.list_create_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 4)
        self.assertEqual(Post.objects.last().author, self.user1)

    def test_delete_post_permission(self):
        self.client.force_authenticate(user=self.user2)
        url = f"/api/v1/social/posts/{self.post1.id}/"

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Post.objects.filter(id=self.post1.id).exists())

    def test_delete_own_post(self):
        self.client.force_authenticate(user=self.user1)
        url = f"/api/v1/social/posts/{self.post1.id}/"

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post1.id).exists())

    @patch("posts.views.requests.get")
    def test_post_explore(self, mock_get):
        url = "/api/v1/social/posts/explore/"

        mock_response = Mock()
        mock_response.json.return_value = {"ids": [self.post3.id, self.post1.id]}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 2)

        returned_ids = [post["id"] for post in response.data]
        self.assertIn(self.post1.id, returned_ids)
        self.assertIn(self.post3.id, returned_ids)
        self.assertNotIn(self.post2.id, returned_ids)
