# TDD ��������

## 1. ����ȯ�� ����
### 1-1. ������Ʈ ���丮 ���� �� �̵�
```bash
mkdir tdd-practice
cd tdd-practice
```
### 1-2. ����ȯ�� ����
```bash
python -m venv venv
```
### 1-3. ����ȯ�� Ȱ��ȭ
```bash
source ./venv/bin/activate
```
### 1-4. �ʿ� ��� ��ġ
```bash
pip install django, bs4
```

## 2. ��� ������Ʈ �⺻ ����
### 2-1. ��� ������Ʈ ����
```bash
django-admin startproject tddpractice .
```
### 2-2. blog, main �� ����
```bash
python manage.py startapp blog
python manage.py startapp main
```
### 2-3. tddpractice/settings.py ����
```python
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    ...
    "blog",
    "main",
]

TEMPLATES = [
    {
        ...
        "DIRS": [BASE_DIR/'templates'],
        ...
    },
]
...
LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'
```
### 2-4. DB ���̱׷���Ʈ �� ���� ���� Ȯ��
```bash
python manage.py migrate
python manage.py runserver
```

## 3. Model �ۼ�
### 3-1. blog/models.py
```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
```
### 3-2. �� ����
```bash
python manage.py makemigrations
python manage.py migrate
```
### 3-3. blog/admin.py
```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

## 4. URL ����
### 4-1. tddpractice/urls.py
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('blog/', include('blog.urls')),
]
```
### 4-2. blog/urls.py
```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
]
```
### 4-3. main/urls.py
```python
# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
```

## 5. Views ����
### 5-1. blog/views.py
```python
from django.shortcuts import render
from .models import Post
from django.db.models import Q
from django.views.generic import ListView, DetailView

class PostList(ListView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_keyword = self.request.GET.get('q')
        if search_keyword:
            context['search'] = search_keyword
            context['page_url'] = f'/blog/?q={search_keyword}&page='
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_keyword = self.request.GET.get('q')
        if search_keyword:
            queryset = queryset.filter(Q(title__icontains=search_keyword) | Q(content__icontains=search_keyword)).distinct()
        return queryset
    
class PostDetail(DetailView):
    model = Post

post_list = PostList.as_view()
post_detail = PostDetail.as_view()
```
### 5-2. main/views.py
```python
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')
```

## 6. Templates ����
### 6-1. templates/base.html
```html
<!DOCTYPE html>
<html lang="ko-KR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {% block head %}{% endblock head %}
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href='{% url "index" %}'>Home</a></li>
                <li><a href='{% url "post_list" %}'>Blog</a></li>
                <li><a href='{% url "about" %}'>About</a></li>
                <li><a href='{% url "contact" %}'>Contact</a></li>
            </ul>
        </nav>
        
    </header>
    {% block content %}
    {% endblock content %}

    <footer>
        <p>Ǫ��</p>
    </footer>
</body>
</html>
```
### 6-2. templates/main/index.html
```html
{% extends "base.html" %}
{% block head %}
<title>Home</title>
{% endblock head %}

{% block content %}
<h1>Home</h1>
{% endblock content %}
```
### 6-3. templates/main/about.html
```html
{% extends "base.html" %}
{% block head %}
<title>About</title>
{% endblock head %}

{% block content %}
<h1>About</h1>
{% endblock content %}
```
### 6-4. templates/main/contact.html
```html
{% extends "base.html" %}
{% block head %}
<title>Contact</title>
{% endblock head %}

{% block content %}
<h1>Contact</h1>
{% endblock content %}
```
### 6-5. templates/blog/post_list.html
```html
{% extends "base.html" %}
{% block head %}
<title>Blog</title>
{% endblock head %}

{% block content %}
<h1>�Խñ� ���</h1>

<input type="text" name="q" id="search-input">
<button id="search-btn">�˻�</button>

<section class='contents-section'>
{% for post in post_list %}
<a href='{% url "post_detail" post.pk %}'>
    <h2 class='contents-heading'>{{ post.title }}</h2>
    <p class='contents-text'>{{ post.content }}</p>
    <p class='contents-updated'>{{ post.updated_at }}</p>
</a>
<hr>
{% empty %}
<p>�Խù��� �������� �ʽ��ϴ�. ù��° �Խù��� ���ΰ��� �Ǽ���!</p>
{% endfor %}
</section>

{% endblock content %}
```
### 6-6. templates/blog/post_detail.html
```html
{% extends "base.html" %}
{% block head %}
<title>Blog Detail</title>
{% endblock head %}

{% block content %}
<h1>�Խñ� �󼼺���</h1>

<section class='contents-section'>
    <h2 class='contents-heading'>{{ post.title }}</h2>
    <p class='contents-text'>{{ post.content }}</p>
    <p class='contents-updated'>{{ post.updated_at }}</p>
</section>
{% endblock content %}
```

## 7. Test �ڵ� �ۼ� �� Ȯ��
### 7-1. blog/tests.py
```python
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

class Test(TestCase):
    urls = ['/', '/about/', '/contact/', '/blog/', '/blog/1/']
    texts = ['Home', 'About', 'Contact', 'Blog', 'Blog Detail']

    def setUp(self):
        print('-- blog app �׽�Ʈ ���� --')
        self.client = Client()
        Post.objects.create(
            title = 'ù ��° ����Ʈ�Դϴ�.',
            content = 'Hello World. We are the world.',
        )
        Post.objects.create(
            title = '�� ��° ����Ʈ�Դϴ�.',
            content = 'Hello World. We are the world.',
        )

    def test_connect(self):
        print('-- ���� Ȯ�� --')
        # 1. ���� Ȯ��
        # 1.1 Home, About, Contact, Blog, Blog Detail ������ �������� �����ɴϴ�.
        # 1.2 ���� ������ �Ǹ� status code�� 200���Դϴ�.
        # 1.3 ���� ���� �� Ÿ��Ʋ���� ������ ������ �ֽ��ϴ�.
        for url, text in zip(self.urls, self.texts):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            self.assertEqual(soup.title.text, text)
            
            print(text + ' ���� Ȯ�� �Ϸ�')

    def test_inherit(self):
        print('-- ��� Ȯ�� --')
        # 2. ��� Ȯ��
        # 2.1 �� 5�� ���������� header, body, footer�� ����� ��� �Ǵ��� Ȯ���մϴ�.
        # 2.2 nav�±� ���ο��� Home, About, Blog, 'Contact'��� �޴��� �ֽ��ϴ�.
        for url in self.urls:
            response = self.client.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            self.assertTrue(soup.header)
            self.assertTrue(soup.body)
            self.assertTrue(soup.footer)
            
            navbar = soup.find('nav')
            self.assertIn('Home', navbar.text)
            self.assertIn('About', navbar.text)
            self.assertIn('Blog', navbar.text)
            self.assertIn('Contact', navbar.text)
                        
            print(url+' ��� Ȯ�� �Ϸ�')
            

    def test_post_list(self):        
        print('-- �Խù� ����Ʈ Ȯ�� --')
        # 3. �Խù� ����Ʈ Ȯ��
        # 3.1 �Խù��� ������ '�Խù��� �������� �ʽ��ϴ�. ù��° �Խù��� ���ΰ��� �Ǽ���!'�� ��µǾ�� �մϴ�.
        # 3.2 �Խù��� ������ h2�� 1�� �̻��̾�� �մϴ�.
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')

        if Post.objects.count() == 0:
            print('�Խù��� ���� ���')
            self.assertIn('�Խù��� �������� �ʽ��ϴ�. ù��° �Խù��� ���ΰ��� �Ǽ���!', soup.body.text)
        else:
            print('�Խù��� �ִ� ���')
            print('�Խù� ����: '+ str(Post.objects.count()))
            print('h2�±� ����: '+ str(len(soup.body.select('h2'))))
            self.assertGreater(len(soup.body.select('h2')), 1)

        print('-- �Խù� ��� ���� Ȯ�� --')
        # 4. �Խù� �ۼ� ���� Ȯ�� (�Խù��� 1�� �̻��� ���)
        # 4.1 �ش� �Խù��� ����(title)�� section ������ �־�� �մϴ�.
        # 4.2 �ش� �Խù��� ����(content)�� section ������ �־�� �մϴ�.
        # 4.3 �ش� �Խù��� ����������¥(updated_at)�� section ������ �־�� �մϴ�.
        for i in range(1, Post.objects.count()+1):
            post = Post.objects.get(id=i)
            section = soup.find('section')
            self.assertIn(post.title, section.text)
            self.assertIn(post.content, section.text)
            self.assertIn(post.updated_at.strftime('%Y�� %m�� %d��'), section.text)
            print(str(i)+'�� �Խù� Ȯ�� �Ϸ�')

    def test_post_detail(self):
        print('-- �Խù� ��������(Blog Detail) Ȯ�� --')
        # 5. �Խù� �������� Ȯ�� (1�� �Խñ�)
        post = Post.objects.get(id=1)
        response = self.client.get('/blog/1/')
        soup = BeautifulSoup(response.content, 'html.parser')

        # ���Ӱ� ����� Ȯ�������Ƿ� �Խñ� ������ Ȯ���մϴ�.
        # 5.1 �ش� �Խñ��� ����(title)�� contents-heading Ŭ������ ���� h2�±� ������ �־�� �մϴ�.
        self.assertIn(post.title, soup.find('h2', 'contents-heading').text)
        # 5.2 �ش� �Խñ��� ����(content)�� contents-text Ŭ������ ���� p�±� ������ �־�� �մϴ�.
        self.assertIn(post.content, soup.find('p', 'contents-text').text)
        # 5.3 �ش� �Խñ��� ���� ������¥(updated_at)�� contents-updated Ŭ������ ���� p�±� ������ �־�� �մϴ�.
        self.assertIn(post.updated_at.strftime('%Y�� %m�� %d��'), soup.find('p', 'contents-updated').text)
        print('�Խù� �������� Ȯ�� �Ϸ�')

```
### 7-2. �׽�Ʈ ����
```bash
python manage.py test
```
### 7-3. ���
```
Found 4 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
-- blog app �׽�Ʈ ���� --
-- ���� Ȯ�� --
Home ���� Ȯ�� �Ϸ�
About ���� Ȯ�� �Ϸ�
Contact ���� Ȯ�� �Ϸ�
Blog ���� Ȯ�� �Ϸ�
Blog Detail ���� Ȯ�� �Ϸ�
.-- blog app �׽�Ʈ ���� --
-- ��� Ȯ�� --
/ ��� Ȯ�� �Ϸ�
/about/ ��� Ȯ�� �Ϸ�
/contact/ ��� Ȯ�� �Ϸ�
/blog/ ��� Ȯ�� �Ϸ�
/blog/1/ ��� Ȯ�� �Ϸ�
.-- blog app �׽�Ʈ ���� --
-- �Խù� ��������(Blog Detail) Ȯ�� --
�Խù� �������� Ȯ�� �Ϸ�
.-- blog app �׽�Ʈ ���� --
-- �Խù� ����Ʈ Ȯ�� --
�Խù��� �ִ� ���
�Խù� ����: 2
h2�±� ����: 2
-- �Խù� ��� ���� Ȯ�� --
1�� �Խù� Ȯ�� �Ϸ�
2�� �Խù� Ȯ�� �Ϸ�
.
----------------------------------------------------------------------
Ran 4 tests in 0.087s

OK
Destroying test database for alias 'default'...
```