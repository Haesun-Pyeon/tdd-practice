# TDD 연습정리

## 1. 가상환경 설정
### 1-1. 프로젝트 디렉토리 생성 및 이동
```bash
mkdir tdd-practice
cd tdd-practice
```
### 1-2. 가상환경 생성
```bash
python -m venv venv
```
### 1-3. 가상환경 활성화
```bash
source ./venv/bin/activate
```
### 1-4. 필요 모듈 설치
```bash
pip install django, bs4
```

## 2. 장고 프로젝트 기본 설계
### 2-1. 장고 프로젝트 생성
```bash
django-admin startproject tddpractice .
```
### 2-2. blog, main 앱 생성
```bash
python manage.py startapp blog
python manage.py startapp main
```
### 2-3. tddpractice/settings.py 수정
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
### 2-4. DB 마이그레이트 및 서버 실행 확인
```bash
python manage.py migrate
python manage.py runserver
```

## 3. Model 작성
### 3-1. blog/models.py
```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
```
### 3-2. 모델 적용
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

## 4. URL 연결
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

## 5. Views 설정
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

## 6. Templates 설정
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
        <p>푸터</p>
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
<h1>게시글 목록</h1>

<input type="text" name="q" id="search-input">
<button id="search-btn">검색</button>

<section class='contents-section'>
{% for post in post_list %}
<a href='{% url "post_detail" post.pk %}'>
    <h2 class='contents-heading'>{{ post.title }}</h2>
    <p class='contents-text'>{{ post.content }}</p>
    <p class='contents-updated'>{{ post.updated_at }}</p>
</a>
<hr>
{% empty %}
<p>게시물이 존재하지 않습니다. 첫번째 게시물의 주인공이 되세요!</p>
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
<h1>게시글 상세보기</h1>

<section class='contents-section'>
    <h2 class='contents-heading'>{{ post.title }}</h2>
    <p class='contents-text'>{{ post.content }}</p>
    <p class='contents-updated'>{{ post.updated_at }}</p>
</section>
{% endblock content %}
```

## 7. Test 코드 작성 및 확인
### 7-1. blog/tests.py
```python
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

class Test(TestCase):
    urls = ['/', '/about/', '/contact/', '/blog/', '/blog/1/']
    texts = ['Home', 'About', 'Contact', 'Blog', 'Blog Detail']

    def setUp(self):
        print('-- blog app 테스트 시작 --')
        self.client = Client()
        Post.objects.create(
            title = '첫 번째 포스트입니다.',
            content = 'Hello World. We are the world.',
        )
        Post.objects.create(
            title = '두 번째 포스트입니다.',
            content = 'Hello World. We are the world.',
        )

    def test_connect(self):
        print('-- 접속 확인 --')
        # 1. 접속 확인
        # 1.1 Home, About, Contact, Blog, Blog Detail 각각의 페이지를 가져옵니다.
        # 1.2 정상 접속이 되면 status code가 200번입니다.
        # 1.3 정상 접속 시 타이틀에는 각각의 문구가 있습니다.
        for url, text in zip(self.urls, self.texts):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            self.assertEqual(soup.title.text, text)
            
            print(text + ' 접속 확인 완료')

    def test_inherit(self):
        print('-- 상속 확인 --')
        # 2. 상속 확인
        # 2.1 위 5개 페이지에서 header, body, footer가 제대로 상속 되는지 확인합니다.
        # 2.2 nav태그 내부에는 Home, About, Blog, 'Contact'라는 메뉴가 있습니다.
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
                        
            print(url+' 상속 확인 완료')
            

    def test_post_list(self):        
        print('-- 게시물 리스트 확인 --')
        # 3. 게시물 리스트 확인
        # 3.1 게시물이 없으면 '게시물이 존재하지 않습니다. 첫번째 게시물의 주인공이 되세요!'가 출력되어야 합니다.
        # 3.2 게시물이 있으면 h2가 1개 이상이어야 합니다.
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')

        if Post.objects.count() == 0:
            print('게시물이 없는 경우')
            self.assertIn('게시물이 존재하지 않습니다. 첫번째 게시물의 주인공이 되세요!', soup.body.text)
        else:
            print('게시물이 있는 경우')
            print('게시물 개수: '+ str(Post.objects.count()))
            print('h2태그 개수: '+ str(len(soup.body.select('h2'))))
            self.assertGreater(len(soup.body.select('h2')), 1)

        print('-- 게시물 목록 구조 확인 --')
        # 4. 게시물 작성 구조 확인 (게시물이 1개 이상일 경우)
        # 4.1 해당 게시물의 제목(title)이 section 영역에 있어야 합니다.
        # 4.2 해당 게시물의 내용(content)이 section 영역에 있어야 합니다.
        # 4.3 해당 게시물의 최종수정날짜(updated_at)가 section 영역에 있어야 합니다.
        for i in range(1, Post.objects.count()+1):
            post = Post.objects.get(id=i)
            section = soup.find('section')
            self.assertIn(post.title, section.text)
            self.assertIn(post.content, section.text)
            self.assertIn(post.updated_at.strftime('%Y년 %m월 %d일'), section.text)
            print(str(i)+'번 게시물 확인 완료')

    def test_post_detail(self):
        print('-- 게시물 상세페이지(Blog Detail) 확인 --')
        # 5. 게시물 상세페이지 확인 (1번 게시글)
        post = Post.objects.get(id=1)
        response = self.client.get('/blog/1/')
        soup = BeautifulSoup(response.content, 'html.parser')

        # 접속과 상속은 확인했으므로 게시글 내용을 확인합니다.
        # 5.1 해당 게시글의 제목(title)이 contents-heading 클래스를 가진 h2태그 영역에 있어야 합니다.
        self.assertIn(post.title, soup.find('h2', 'contents-heading').text)
        # 5.2 해당 게시글의 내용(content)이 contents-text 클래스를 가진 p태그 영역에 있어야 합니다.
        self.assertIn(post.content, soup.find('p', 'contents-text').text)
        # 5.3 해당 게시글의 최종 수정날짜(updated_at)가 contents-updated 클래스를 가진 p태그 영역에 있어야 합니다.
        self.assertIn(post.updated_at.strftime('%Y년 %m월 %d일'), soup.find('p', 'contents-updated').text)
        print('게시물 상세페이지 확인 완료')

```
### 7-2. 테스트 실행
```bash
python manage.py test
```
### 7-3. 결과
```
Found 4 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
-- blog app 테스트 시작 --
-- 접속 확인 --
Home 접속 확인 완료
About 접속 확인 완료
Contact 접속 확인 완료
Blog 접속 확인 완료
Blog Detail 접속 확인 완료
.-- blog app 테스트 시작 --
-- 상속 확인 --
/ 상속 확인 완료
/about/ 상속 확인 완료
/contact/ 상속 확인 완료
/blog/ 상속 확인 완료
/blog/1/ 상속 확인 완료
.-- blog app 테스트 시작 --
-- 게시물 상세페이지(Blog Detail) 확인 --
게시물 상세페이지 확인 완료
.-- blog app 테스트 시작 --
-- 게시물 리스트 확인 --
게시물이 있는 경우
게시물 개수: 2
h2태그 개수: 2
-- 게시물 목록 구조 확인 --
1번 게시물 확인 완료
2번 게시물 확인 완료
.
----------------------------------------------------------------------
Ran 4 tests in 0.087s

OK
Destroying test database for alias 'default'...
```