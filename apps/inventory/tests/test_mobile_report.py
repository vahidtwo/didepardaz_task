from django.urls import reverse

from apps.inventory.models import Brand, Mobile
from apps.location.models import Country
from core.tests.test import TokenAPITestCases


class MobileReportViewTestCase(TokenAPITestCases):
    def setUp(self):
        self.country = Country.objects.create(title="Some Country")
        self.korea = Country.objects.create(title="Korea")
        self.brand = Brand.objects.create(title=self.fake.company(), nationality=self.country)
        self.mobile = Mobile.objects.create(
            brand=self.brand,
            model=self.fake.word(),
            price=self.fake.random_int(min=100, max=1000),
            color_name=self.fake.color_name(),
            size=self.fake.random_int(min=4, max=7),
            producer_country=self.country,
            is_available=True,
        )

    def test_korean_mobiles_report(self):
        # Create another test mobile with a Korean brand
        korean_brand = Brand.objects.create(title=self.fake.company(), nationality=self.korea)
        korean_mobile = Mobile.objects.create(
            brand=korean_brand,
            model=self.fake.word(),
            price=self.fake.random_int(min=100, max=1000),
            color_name=self.fake.color_name(),
            size=self.fake.random_int(min=4, max=7),
            producer_country=self.korea,
            is_available=True,
        )
        response = self.client.get(reverse("korean_mobiles"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, korean_mobile.brand.title)
        self.assertNotContains(response, self.mobile.brand.title)
