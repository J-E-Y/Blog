from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category
from django.utils import timezone
from django.contrib.auth.models import User


def create_category(name='life', description=''):
    category, is_created = Category.objects.get_or_create(
        name=name,
        description=description
    )

    category.slug = category.name.replace(' ', '-').replace('/', '')
    category.save()

    return category


def create_post(title, content, author, category=None):
    blog_post = Post.objects.create(
        title=title,
        content=content,
        created=timezone.now(),
        author=author,
        category=category,
    )

    return blog_post


class TestModel(TestCase):
    def setUp(self):
        self.client = Client()
        self.author_000 = User.objects.create(username='smith', password='nopassword')

    def test_category(self):
        category = create_category()

        post_000 = create_post(
            title='The first post',
            content='Hello World. We are the world.',
            author=self.author_000,
            category=category
        )

        self.assertEqual(category.post_set.count(), 1)

    def test_post(self):
        category = create_category()

        post_000 = create_post(
            title='The first post',
            content='Hello World. We are the world.',
            author=self.author_000,
            category=category
        )


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.author_000 = User.objects.create(username='smith', password='nopassword')

    def check_navbar(self, soup):
        navbar = soup.find('div', id='navbar')
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)

    def check_right_side(self,soup):
        # category card 에서

        category_card = soup.find("div", id="category-card")
        # 1 우선 찾고 2 찾게 하기위해서 우선 html 가서 id 값을 지정한다 like <div class="card my-4" id="category-card">

        self.assertIn("unclassified(1)", category_card.text)  # 미분류 있어야함(1)
        self.assertIn("political_society(1)", category_card.text)  # 정치/사회있어야함(1)


    def test_post_list_no_posts(self):
        response = self.client.get('/blog/')

        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        self.assertEqual(title.text, 'Blog')

        self.check_navbar(soup)

        # navbar = soup.find('div', id='navbar')
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About me', navbar.text)

        self.assertEqual(Post.objects.count(), 0)
        self.assertIn('아직 게시물이 없습니다.', soup.body.text)

    def test_post_list_with_post(self):
        post_000 = create_post(
            title='The first post',
            content='Hello World. We are the world.',
            author=self.author_000,

        )

        post_001 = create_post(

            title='The sceond post',
            content='The sceond,The sceond,The sceond',
            author=self.author_000,
            category=create_category(name="political_society")

        )

        self.assertGreater(Post.objects.count(), 0)

        response = self.client.get('/blog/')

        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.body

        self.assertNotIn('아직 게시물이 없습니다.', body.text)
        self.assertIn(post_000.title, body.text)

        self.check_right_side(soup)

        ### main_div에는

        main_div = soup.find("div", id="main-div")  # 우선 찾고

        self.assertIn("political_society", main_div.text)  # main_div에는 정치/사회
        self.assertIn("unclassified", main_div.text)  # main_div에는

        #post_000_read_more_btn = body.find('a', id="read-more-post-{}".format(post_000.pk))
        #print(post_000_read_more_btn)



    def test_post_detail(self):
        post_000 = create_post(
            title='The first post',
            content='Hello World. We are the world.',
            author=self.author_000,
        )

        post_001 = create_post(

            title='The sceond post',
            content='The sceond,The sceond,The sceond',
            author=self.author_000,
            category=create_category(name="political_society")

        )

        self.assertGreater(Post.objects.count(), 0)
        post_000_url = post_000.get_absolute_url()
        self.assertEqual(post_000_url, '/blog/{}/'.format(post_000.pk))

        response = self.client.get(post_000_url)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        self.assertEqual(title.text, '{} - Blog'.format(post_000.title))

        self.check_navbar(soup)

        body = soup.body

        main_div = body.find('div', id='main-div')
        self.assertIn(post_000.title, main_div.text)
        self.assertNotIn(post_000.author.username, main_div.text)

        self.assertIn(post_000.content, main_div.text)

        self.check_right_side(soup)

    def test_post_list_by_category(self):
        category_politics = create_category(name='political_society')

        post_000 = create_post(
            title='The first post',
            content='Hello World. We are the world.',
            author=self.author_000,
        )

        post_001 = create_post(
            title='The second post',
            content='Second Second Second',
            author=self.author_000,
            category=category_politics
        )

        response = self.client.get(category_politics.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        #self.asserEqual('blog - {}'.format(category_politics.name), soup.title.text)

        main_div = soup.find('div', id='main-div')
        self.assertNotIn('unclassified', main_div.text)
        self.assertIn(category_politics.name, main_div.text)