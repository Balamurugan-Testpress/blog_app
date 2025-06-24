from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Comment, Post


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.post = Post.objects.create(
            title="Test Title",
            slug="test-title",
            body="Test body",
            author=self.user,
            status="published",
        )

    def test_str(self):
        self.assertEqual(str(self.post), "Test Title")

    def test_absolute_url_start(self):
        url = self.post.get_absolute_url()
        self.assertTrue(url.startswith("/blog/"))

    def test_absolute_url_end(self):
        url = self.post.get_absolute_url()
        self.assertTrue(url.endswith("/test-title/"))

    def test_published_manager(self):
        posts = Post.published.all()
        for post in posts:
            self.assertTrue(post.status == "published")

    def test_draft_post_not_in_published_manager(self):
        draft = Post.objects.create(
            title="Draft Post",
            slug="draft-post",
            body="Hidden content",
            author=self.user,
            status="draft",
        )
        self.assertNotIn(draft, Post.published.all())

    def test_post_ordering(self):
        older_post = Post.objects.create(
            title="Old Post",
            slug="old-post",
            body="Old content",
            author=self.user,
            publish=timezone.now() - timezone.timedelta(days=1),
            status="published",
        )
        self.assertEqual(list(Post.objects.all())[0], self.post)  # self.post is newer


class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.post = Post.objects.create(
            title="Test Title",
            slug="test-title",
            body="Test body",
            author=self.user,
            status="published",
        )
        self.comment = Comment.objects.create(
            post=self.post,
            name="John Doe",
            email="john@example.com",
            body="Nice post!",
            active=True,
        )

    def test_str(self):
        test_str = f"Comment by {self.comment.name} on {self.comment.post}"
        self.assertEqual(str(self.comment), test_str)

    def test_comment_in_post(self):
        self.assertIn(self.comment, self.post.comments.all())

    def test_comment_ordering(self):
        c2 = Comment.objects.create(
            post=self.post,
            name="Another User",
            email="a@example.com",
            body="Second comment",
            active=True,
        )
        comments = list(self.post.comments.all())
        self.assertLessEqual(comments[0].created, comments[1].created)
