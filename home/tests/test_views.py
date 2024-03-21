from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from home.forms import (
    PostSearchForm,
    CommentCreateForm,
    PostCreateUpdateForm,
)
from home.models import Post, Comment, Vote


class TestHomeView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view_GET(self):
        request = self.client.get(reverse('home:home'))
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'home/index.html')
        self.failUnless(request.context['form'], PostSearchForm)


class TestPostDetailView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='beni',
            email='beni@gmail.com',
            password='1234'
        )
        self.post = Post.objects.create(
            user=self.user,
            body='this is first post',
            slug='first-post',
            title='first post'
        )

    def test_post_detail_view_GET(self):
        request = self.client.get(reverse('home:post_detail', args=(self.post.id, self.post.slug)))
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'home/detail.html')
        self.failUnless(request.context['form'], CommentCreateForm)

    def test_post_detail_view_POST(self):
        self.client.login(
            username=self.user.username,
            email=self.user.email,
            password='1234'
        )
        request = self.client.post(
            reverse('home:post_detail', args=(self.post.id, self.post.slug)),
            data={
                'body': 'this is first comment',
            }
        )

        self.assertEqual(Comment.objects.count(), 1)
        self.assertRedirects(request, reverse('home:post_detail', args=(self.post.id, self.post.slug)))


class TestPostDeleteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='beni',
            email='beni@gmail.com',
            password='1234'
        )
        self.client.login(
            username=self.user.username,
            email=self.user.email,
            password='1234'
        )
        self.post = Post.objects.create(
            user=self.user,
            body='this is first post',
            slug='first-post',
            title='first post'
        )

    def test_post_delete_view_GET(self):
        request = self.client.get(reverse('home:post_delete', args=(self.post.id,)))
        self.assertEqual(request.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)
        self.assertRedirects(request, reverse('home:home'))


class TestPostUpdateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='beni',
            email='beni@gmail.com',
            password='1234'
        )
        self.client.login(
            username=self.user.username,
            email=self.user.email,
            password='1234'
        )
        self.post = Post.objects.create(
            user=self.user,
            body='this is first post',
            slug='first-post',
            title='first post'
        )

    def test_post_update_view_GET(self):
        request = self.client.get(reverse('home:post_update', args=(self.post.id,)))
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'home/update.html')
        self.failUnless(request.context['form'], PostCreateUpdateForm)

    def test_post_update_view_POST(self):
        body = self.post.body
        request = self.client.post(
            reverse('home:post_update', args=(self.post.id,)),
            data={
                'body': 'this is first post :)'
            }
        )
        self.post = Post.objects.last()
        self.assertEqual(request.status_code, 302)
        self.assertFalse(Post.objects.filter(body=body).exists())
        self.assertRedirects(request, reverse('home:post_detail', args=(self.post.id, self.post.slug)))


class TestPostCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='beni',
            email='beni@gmail.com',
            password='1234'
        )
        self.client.login(
            username=self.user.username,
            email=self.user.email,
            password='1234'
        )

    def test_post_create_view_GET(self):
        request = self.client.get(reverse('home:post_create'))
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'home/create.html')
        self.failUnless(request.context['form'], PostCreateUpdateForm)

    def test_post_create_view_POST(self):
        request = self.client.post(reverse('home:post_create'), data={'body': 'this is first post'})
        self.assertEqual(request.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.last()
        self.assertRedirects(request, reverse('home:post_detail', args=(post.id, post.slug)))


class TestPostAddReplyView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='beni',
            email='beni@gmail.com',
            password='1234'
        )
        self.client.login(
            username=self.user.username,
            email=self.user.email,
            password='1234'
        )
        self.post = Post.objects.create(
            user=self.user,
            body='this is first post',
            slug='first-post',
            title='first post'
        )
        self.comment = Comment.objects.create(
            user=self.user,
            post=self.post,
            body='first comment'
        )

    def test_post_add_reply_view_POST(self):
        request = self.client.post(
            reverse('home:add_reply', args=(self.post.id, self.comment.id)),
            data={
                'body': 'this is reply'
            }
        )

        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, reverse('home:post_detail', args=(self.post.id, self.post.slug)))


class TestPostLikeView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='beni',
            email='beni@gmail.com',
            password='1234'
        )
        self.client.login(
            username=self.user.username,
            email=self.user.email,
            password='1234'
        )
        self.post = Post.objects.create(
            user=self.user,
            body='this is first post',
            slug='first-post',
            title='first post'
        )

    def test_post_like_view_GET(self):
        request = self.client.get(reverse('home:post_like', args=(self.post.id,)))
        self.assertEqual(request.status_code, 302)
        self.assertTrue(Vote.objects.filter(post=self.post, user=self.user).exists())
        self.assertRedirects(request, reverse('home:post_detail', args=(self.post.id, self.post.slug)))
