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
