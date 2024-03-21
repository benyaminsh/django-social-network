from django.test import TestCase

from home.forms import (
    PostCreateUpdateForm,
    PostSearchForm,
    CommentCreateForm,
    CommentReplyForm
)


class TestPostSearchForm(TestCase):
    def test_valid_data(self):
        form = PostSearchForm(data={'search': 'first post'})
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_empty_data(self):
        form = PostSearchForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)


class TestCommentCreateForm(TestCase):
    def test_valid_data(self):
        form = CommentCreateForm(
            data={
                'body': 'this is first comment'
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_empty_data(self):
        form = CommentCreateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)


class TestCommentReplyForm(TestCase):
    def test_valid_data(self):
        form = CommentReplyForm(
            data={
                'body': 'this reply comment'
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_empty_data(self):
        form = CommentReplyForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)


class TestPostCreateUpdateForm(TestCase):
    def test_valid_data(self):
        form = PostCreateUpdateForm(
            data={
                'body': 'this is first post'
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_empty_data(self):
        form = PostCreateUpdateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
