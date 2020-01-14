from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Page


class PageModelTestCase(TestCase):
	def test_create(self):
		title = "Hamza's Pizza"
		content = "Pizza that tastes really good."
		page = Page.objects.create(
			title=title,
			content=content,
			)
		self.assertEqual(page.title, title)
		self.assertEqual(page.content, content)

	def test_model_admin_page(self):
		user = User.objects.create_user(username='user', password='1234567890-=', is_superuser=True, is_staff=True)
		user.save()
		self.client.login(username='user', password='1234567890-=')

		url = reverse("admin:pages_page_add")
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

	def test_get_absolute_url(self):
		page = Page.objects.create(
			title="title",
			content="content",
		)
		response = self.client.get(page.get_absolute_url())
		self.assertEqual(response.status_code, 200)


class ListPageTestCase(TestCase):
	@classmethod
	def setUpTestData(cls):
		for i in range(0, 5):
			Page.objects.create(
				title=f"title-{i}",
				content=f"content-{i}",
			)

	def test_page_exists(self):
		url = reverse("page-list")
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200, msg="check the list page url name")

	def test_template(self):
		url = reverse("page-list")
		response = self.client.get(url)
		self.assertTemplateUsed(response, 'list.html')

	def test_pages_displayed(self):
		url = reverse("page-list")
		response = self.client.get(url)

		pages = Page.objects.all()
		for page in pages:	
			self.assertContains(response, page.title, msg_prefix="are you displaying the pages title in the pages list template")

	def test_details_page_linked(self):
		url = reverse("page-list")
		response = self.client.get(url)
		self.assertContains(response, reverse("page-detail",kwargs={'page_id':4}))



class DetailPageTestCase(TestCase):
	@classmethod
	def setUpTestData(cls):
		for i in range(0, 5):
			Page.objects.create(
				title=f"title-{i}",
				content=f"content-{i}",
			)

	def test_page_exists(self):
		url = reverse("page-detail", kwargs={'page_id':4})
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200, msg="check the detail page url name")

	def test_template(self):
		url = reverse("page-detail", kwargs={'page_id':4})
		response = self.client.get(url)
		self.assertTemplateUsed(response, 'detail.html')

	def test_pages_displayed(self):
		page_id = 3
		url = reverse("page-detail", kwargs={'page_id':page_id})
		response = self.client.get(url)

		pages = Page.objects.all()
		for page in pages:
			if page.id == page_id:	
				self.assertContains(response, page.title)
				self.assertContains(response, page.content)
			else:
				self.assertNotContains(response, page.title)
				self.assertNotContains(response, page.content)

