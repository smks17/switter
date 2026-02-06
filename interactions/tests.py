from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from posts.models import Post
from interactions.models import Comment, FollowLinks, Like


@override_settings(USE_KAFKA=False)
class LikeTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
        self.post = Post.objects.create(author=self.user2, content="Some content")
        self.client.force_authenticate(user=self.user1)
        self.like_url = f"/api/v1/social/posts/{self.post.id}/likes/"

    def test_like_post(self):
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(user=self.user1, post=self.post).exists())

    def test_duplicate_like(self):
        Like.objects.create(user=self.user1, post=self.post)
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            Like.objects.filter(user=self.user1, post=self.post).count(), 1
        )

    def test_unlike_post(self):
        Like.objects.create(user=self.user1, post=self.post)
        response = self.client.delete(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Like.objects.filter(user=self.user1, post=self.post).exists())


@override_settings(USE_KAFKA=False)
class CommentTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
        self.post = Post.objects.create(author=self.user2, content="Some content")
        self.comment_content = "Test comment"
        self.client.force_authenticate(user=self.user1)
        self.comment_url = f"/api/v1/social/posts/{self.post.id}/comments/"

    def test_comment_post(self):
        response = self.client.post(
            self.comment_url, data={"content": self.comment_content}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Comment.objects.filter(user=self.user1, post=self.post).exists()
        )
        self.assertEqual(
            Comment.objects.filter(user=self.user1, post=self.post).get().content,
            self.comment_content,
        )


@override_settings(USE_KAFKA=False)
class FollowingTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
        self.client.force_authenticate(user=self.user1)
        self.follow_url = f"/api/v1/social/users/{self.user2.id}/follow/"

    def test_follow_post(self):
        response = self.client.post(self.follow_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            FollowLinks.objects.filter(
                follower=self.user1, following=self.user2
            ).exists()
        )

    def test_duplicate_follow(self):
        FollowLinks.objects.create(follower=self.user1, following=self.user2)
        response = self.client.post(self.follow_url)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            FollowLinks.objects.filter(
                follower=self.user1, following=self.user2
            ).count(),
            1,
        )

    def test_unfollow_user(self):
        FollowLinks.objects.create(follower=self.user1, following=self.user2)
        response = self.client.delete(self.follow_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            FollowLinks.objects.filter(
                follower=self.user1, following=self.user2
            ).exists()
        )
