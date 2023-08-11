from rest_framework.reverse import reverse

from apps.inventory.models import Brand, Mobile
from apps.location.models import Country
from core.tests.test import TokenAPITestCases


class MobileViewTestCase(TokenAPITestCases):
    def setUp(self):
        # Create a test country
        self.country = Country.objects.create(title="Some Country")

        # Create a test brand
        self.brand = Brand.objects.create(
            title=self.fake.company(), nationality=self.country  # Assign the country instance here
        )

        # Create a test mobile
        self.mobile = Mobile.objects.create(
            brand=self.brand,
            model=self.fake.word(),
            price=self.fake.random_int(min=100, max=1000),
            color_name=self.fake.color_name(),
            size=self.fake.random_int(min=4, max=7),
            producer_country=self.country,  # Assign the country instance here
            is_available=True,
        )

    def test_create_mobile_view(self):
        response = self.client.get(reverse("add_mobile"))
        self.assertEqual(response.status_code, 200)

        data = {
            "brand": self.brand.pk,
            "model": self.fake.word(),
            "price": self.fake.random_int(min=100, max=1000),
            "color_name": self.fake.color_name(),
            "size": self.fake.random_int(min=4, max=7),
            "producer_country": "Some Country",
            "is_available": True,
        }

        response = self.client.post(reverse("add_mobile"), data)
        self.assertEqual(response.status_code, 200)  # Should redirect to list_mobiles

    def test_list_mobiles_view(self):
        response = self.client.get(reverse("list_mobiles"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.mobile.brand.title)

    def test_edit_mobile_view(self):
        response = self.client.get(reverse("edit_mobile", args=[self.mobile.pk]))
        self.assertEqual(response.status_code, 200)

        data = {
            "brand": self.brand.pk,
            "model": self.fake.word(),
            "price": self.fake.random_int(min=100, max=1000),
            "color_name": self.fake.color_name(),
            "size": self.fake.random_int(min=4, max=7),
            "producer_country": "Some Country",
            "is_available": False,
        }

        response = self.client.post(reverse("edit_mobile", args=[self.mobile.pk]), data)
        self.assertEqual(response.status_code, 200)
