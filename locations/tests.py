from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import SportsFieldLocation, Booking, Favorite, Rating
from datetime import timedelta
from django.utils import timezone


class TestLocationsViews(TestCase):

    def setUp(self):
        """إعداد البيانات الأساسية للاختبارات."""
        self.client = Client()

        # إنشاء مستخدم
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        # إنشاء ملعب
        self.field = SportsFieldLocation.objects.create(
            name="Test Field",
            field_type="football",
            latitude=10.0,
            longitude=20.0,
            address="Test Address",
            description="Test Description",
            average_rating=4.5
        )

        # إنشاء حدث
        self.booking = Booking.objects.create(
            field=self.field,
            user=self.user,
            date=timezone.now().date(),
            time=(timezone.now() + timedelta(hours=1)).time(),
            duration=2
        )

    def test_get_field_types(self):
        """اختبار دالة get_field_types."""
        response = self.client.get(reverse('get_field_types'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("football", response.json())

    def test_get_field_names(self):
        """اختبار دالة get_field_names."""
        response = self.client.get(reverse('get_field_names'))
        self.assertEqual(response.status_code, 200)
        self.assertIn({'id': self.field.id, 'name': self.field.name}, response.json()) # noqa

    def test_get_field_locations(self):
        """اختبار دالة get_field_locations."""
        response = self.client.get(reverse('get_field_locations'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)

    def test_get_nearby_fields(self):
        """اختبار دالة get_nearby_fields."""
        response = self.client.get(reverse('get_nearby_fields'), {
            'latitude': 10.0,
            'longitude': 20.0,
            'max_distance': 5
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)

    def test_field_detail_authenticated(self):
        """اختبار صفحة تفاصيل الملعب للمستخدم المصادق عليه."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse(
            'field_detail', args=[self.field.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.field.name)

    def test_field_detail_guest(self):
        """اختبار صفحة تفاصيل الملعب للمستخدم الضيف."""
        response = self.client.get(reverse(
            'field_detail', args=[self.field.id]))
        self.assertEqual(response.status_code, 302) 

    def test_find_fields(self):
        """اختبار دالة find_fields."""
        response = self.client.get(reverse('find_fields'), {
            'type': 'football',
            'search': 'Test'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.field.name)

    def test_favorite_toggle(self):
        """اختبار إضافة/إزالة ملعب من المفضلة."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse(
            'field_detail', args=[self.field.id]), {
            'favorite': 'toggle'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Favorite.objects.filter(
            user=self.user, field=self.field).exists())

    def test_rating_field(self):
        """اختبار تقييم ملعب."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse(
            'field_detail', args=[self.field.id]), {
            'rating': 4
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Rating.objects.filter(
            user=self.user, field=self.field, rating=4).exists())
