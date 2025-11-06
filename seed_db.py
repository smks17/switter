import os
import django
from random import choice, sample
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "switter.settings")
django.setup()

from django.contrib.auth import get_user_model
from posts.models import Post
from interactions.models import FollowLinks, Comment, Like

fake = Faker()
User = get_user_model()


def run_seed(users=10, posts=30, comments=50, likes=80, follows=20, clear=False):
    if clear:
        print("Clearing existing data...")
        FollowLinks.objects.all().delete()
        Like.objects.all().delete()
        Comment.objects.all().delete()
        Post.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

    #######Users#######
    users_list = [
        User.objects.create_user(
            username=fake.unique.user_name(),
            email=fake.email(),
            password="test1234",
        )
        for _ in range(users)
    ]
    print(f"Created {len(users_list)} users")

    #######Posts#######
    posts_list = [
        Post.objects.create(
            author=choice(users_list), content=fake.text(max_nb_chars=200)
        )
        for _ in range(posts)
    ]
    print(f"Created {len(posts_list)} posts")

    #######Comments#######
    comments_list = [
        Comment.objects.create(
            user=choice(users_list),
            post=choice(posts_list),
            content=fake.sentence(nb_words=15),
        )
        for _ in range(comments)
    ]
    print(f"Created {len(comments_list)} comments")

    #######Likes#######
    likes_created = 0
    for _ in range(likes):
        u = choice(users_list)
        p = choice(posts_list)
        if not Like.objects.filter(user=u, post=p).exists():
            Like.objects.create(user=u, post=p)
            likes_created += 1
    print(f"Created {likes_created} likes")

    #######Follow Links#######
    follows_created = 0
    for _ in range(follows):
        follower, following = sample(users_list, 2)
        if not FollowLinks.objects.filter(
            follower=follower, following=following
        ).exists():
            FollowLinks.objects.create(follower=follower, following=following)
            follows_created += 1
    print(f"Created {follows_created} follow links")

    print("Seeding completed!")


if __name__ == "__main__":
    run_seed(users=10, posts=30, comments=50, likes=100, follows=20, clear=True)
