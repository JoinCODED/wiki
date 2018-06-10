from django.test import TestCase
from django.urls import reverse
from .models import Page

class PageModelTestCase(TestCase):
    def test_create(self):
        Page.objects.create(
            title="Pizza",
            content="It's yummy, but unfortunately unhealthy.",
            )

class PageViewTestCase(TestCase):
    def setUp(self):
        self.page_1 = Page.objects.create(title="page 1", content="This is page 1")
        self.page_2 = Page.objects.create(title="page 2", content="This is page 2")
        self.page_3 = Page.objects.create(title="page 3", content="This is page 3")

    def test_list_view(self):
        list_url = reverse("page-list")
        response = self.client.get(list_url)
        for page in Page.objects.all():
            self.assertContains(response, page.title)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(response.status_code, 200)

    def test_detail_view(self):
        detail_url = reverse("page-detail", kwargs={"page_id":self.page_1.id})
        response = self.client.get(detail_url)
        self.assertContains(response, self.page_1.title)
        self.assertContains(response, self.page_1.content)
        self.assertTemplateUsed(response, 'detail.html')
        self.assertEqual(response.status_code, 200)
