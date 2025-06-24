from django.test import TestCase

from ..models import Post
from django.contrib.auth.models import User
from django.urls import reverse


class PostListViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser")
        # One published post
        self.published_post = Post.objects.create(
            title="Published Post",
            slug="published-post",
            author=self.user,
            body="This is a published post.",
            status="published",
        )
        # One draft post
        self.draft_post = Post.objects.create(
            title="Draft Post",
            slug="draft-post",
            author=self.user,
            body="This is a draft post.",
            status="draft",
        )

    def test_list_view_status_code(self):
        url = reverse("blog:post_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_uses_correct_template(self):
        url = reverse("blog:post_list")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "blog/post/list.html")

    def test_only_published_posts_shown(self):
        url = reverse("blog:post_list")
        response = self.client.get(url)
        posts = response.context["posts"]
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], self.published_post)


class PostDetailView(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.post = Post.objects.create(
            title="Published Post",
            slug="published-post",
            author=self.user,
            body="This is a published post.",
            status="published",
        )
        self.url = reverse(
            "blog:post_detail",
            args=[
                self.post.publish.year,
                self.post.publish.month,
                self.post.publish.day,
                self.post.slug,
            ],
        )

    def test_detail_view_status_code(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "blog/post/detail.html")


class SearchViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user")
        Post.objects.create(
            title="Django Tips",
            slug="django-tips",
            author=self.user,
            body="Tips for Django",
            status="published",
        )

    def test_search_results_found(self):
        response = self.client.get(reverse("blog:post_search"), {"query": "Django"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django Tips")

    def test_search_no_query(self):
        response = self.client.get(reverse("blog:post_search"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["results"]), 0)
