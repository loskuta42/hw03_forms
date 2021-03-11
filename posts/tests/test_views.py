from django.test import TestCase, Client
from posts.models import Post, Group
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import forms
import datetime as dt

User = get_user_model()


class PostPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='test_user')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title='test_group',
            slug='test-slug',
            description='test_description'
        )
        cls.post = Post.objects.create(
            text='test_post',
            group=cls.group,
            author=User.objects.get(username='test_user')
        )

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            'index.html': reverse('index'),
            'group.html': reverse('group_posts', kwargs={'slug': 'test-slug'}),
            'new.html': reverse('new_post')
        }

        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_new_show_correct_context(self):
        """Шаблон new сформирован с правильным контекстом."""
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        response = self.authorized_client.get(reverse('new_post'))
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)

    def test_index_page_list_is_1(self):
        # Удостоверимся, что на страницу с постами передаётся
        # ожидаемое количество объектов
        response = self.authorized_client.get(reverse('index'))
        self.assertEqual(len(response.context['posts']), 1)

    def test_group_page_list_is_1(self):
        # Удостоверимся, что на страницу с постами передаётся
        # ожидаемое количество объектов
        response = self.authorized_client.get(reverse('group_posts', kwargs={'slug': 'test-slug'}))
        correct_group = response.context['posts'][0].group.title
        self.assertEqual(len(response.context['posts']), 1)
        self.assertEqual(correct_group, 'test_group')

    def test_index_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('index'))
        # Взяли первый элемент из списка и проверили, что его содержание
        # совпадает с ожидаемым
        first_object = response.context['posts'][0]
        post_text_0 = first_object.text
        post_pub_date_0 = first_object.pub_date.date()
        post_group_0 = first_object.group.title
        post_author_0 = first_object.author.username
        self.assertEqual(post_text_0, 'test_post')
        self.assertEqual(post_pub_date_0, dt.datetime.now().date())
        self.assertEqual(post_group_0, 'test_group')
        self.assertEqual(post_author_0, 'test_user')

    def test_group_slug_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('group_posts', kwargs={'slug': 'test-slug'}))
        # Взяли первый элемент из списка и проверили, что его содержание
        # совпадает с ожидаемым
        first_object = response.context['posts'][0]
        post_text_0 = first_object.text
        post_pub_date_0 = first_object.pub_date.date()
        post_group_0 = first_object.group.title
        post_group_slug_0 = first_object.group.slug
        post_group_desc_0 = first_object.group.description
        post_author_0 = first_object.author.username
        self.assertEqual(post_text_0, 'test_post')
        self.assertEqual(post_pub_date_0, dt.datetime.now().date())
        self.assertEqual(post_group_0, 'test_group')
        self.assertEqual(post_group_slug_0, 'test-slug')
        self.assertEqual(post_group_desc_0, 'test_description')
        self.assertEqual(post_author_0, 'test_user')


