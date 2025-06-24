from django.test import TestCase
from blog.forms import CommentForm


class CommentFormTest(TestCase):

    def setUp(self):
        self.form = CommentForm(
            data={"name": "John", "email": "john@example.com", "body": "Test comment"}
        )

    def test_valid_comment_form(self):

        self.assertTrue(self.form.is_valid())

    def test_missing_name(self):
        form = CommentForm(data={"email": "john@example.com", "body": "Test comment"})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_missing_email(self):
        form = CommentForm(data={"name": "John", "body": "Test comment"})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_missing_body(self):
        form = CommentForm(data={"name": "John", "email": "john@example.com"})
        self.assertFalse(form.is_valid())
        self.assertIn("body", form.errors)

    def test_invalid_email(self):
        form = CommentForm(
            data={"name": "John", "email": "not-an-email", "body": "Test comment"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_cleaned_data(self):
        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.cleaned_data["name"], "John")
        self.assertEqual(self.form.cleaned_data["email"], "john@example.com")
        self.assertEqual(self.form.cleaned_data["body"], "Test comment")
