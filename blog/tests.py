from django.test import TestCase
from django.urls import reverse
from blog.models import Post, Comment
from django.contrib.auth.models import User

class TestPostsView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        
        for i in range(10):
            Post.objects.create(title=f'Test Post {i}', content=f'Test content {i}', author=self.user)
    
    def test_posts_view(self):
        url = reverse('home')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        # Checking if  the number of posts in the context matches the number created
        self.assertEqual(len(response.context['posts']), 5)


class TestPostDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        
        self.post = Post.objects.create(title='Test Post', content='Test content', author=self.user)
    
    def test_post_detail_view(self):
        url = reverse('detail_post', args=[self.post.slug])
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        


class TestPostCreationView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
    
    def test_post_creation_view(self):
        self.client.login(username='testuser', password='password')
        
        response = self.client.post(reverse('create_post'), {
            'title': 'New Test Post',
            'content': 'New test content'
        })
        
        # Checking if the post was created successfully
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(title='New Test Post').exists())

class TestCommentCreationView(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')
        
        self.post = Post.objects.create(title='Test Post', content='Test content', author=self.user)
    
    def test_comment_creation_view(self):
        self.client.login(username='testuser', password='password')
        
        response = self.client.post(reverse('add_comment', args=[self.post.slug]), {
            'content': 'New test comment'
        })
        
        # Checking that the comment was created successfully or not
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Comment.objects.filter(post=self.post, content='New test comment').exists())
