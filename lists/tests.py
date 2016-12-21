from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item


# Create your tests here.


# 下面代码做初始化用
# class SmokeTest(TestCase):
#     def test_bad_maths(self):
#         self.assertEqual(1+1,3)


# 单元测试--默认页面测试
class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func,home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        # 这里测试的是响应返回的常量
        # self.assertTrue(response.content.startswith(b'<html>'))
        # self.assertIn(b'<title>To-Do lists</title>',response.content)
        # self.assertTrue(response.content.endswith(b'</html>'))

        #测试返回的变量
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(),expected_html)


    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'A new list item')

    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertEqual(
            response.status_code,302
        )
        self.assertEqual(
            response['location'],'/lists/the-only-list-in-the-world/'
        )

        # self.assertIn('A new list item',response.content.decode())
        # expected_html = render_to_string(
        #     'home.html',
        #     {'new_item_text':'A new list item'}
        # )
        # self.assertEqual(response.content.decode(),expected_html)
        # print(expected_html)

    # def test_home_page_displays_all_list_items(self):
    #     Item.objects.create(text='item 1')
    #     Item.objects.create(text = 'item 2')
    #
    #     request = HttpRequest()
    #     response = home_page(request)
    #
    #     self.assertIn(
    #         'item 1',response.content.decode()
    #     )
    #     self.assertIn(
    #         'item 2',response.content.decode()
    #     )
        # self.assertTrue(
        #     all(['item 1' in response.content.decode(),
        #         'item 2' in response.content.decode()])
        # )


class ListViewTest(TestCase):

    def test_display_all_items(self):
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(
            response,'item 1'
        )
        self.assertContains(
            response,'item 2'
        )

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response,'list.html')



# 单元测试--数据模型测试
class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(
            saved_items.count(),2
        )

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(
            first_saved_item.text,'The first (ever) list item'
        )
        self.assertEqual(
            second_saved_item.text,'Item the second'
        )

