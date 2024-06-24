from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login

class OrgreportTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        super().setUp()

    def test_login(self):
        response = self.client.get(reverse('orgreport:login'))
        self.assertEqual(response.status_code, 200)

    def test_home(self):
        response = self.client.get(reverse('orgreport:home'))
        self.assertEqual(response.status_code, 200)

    def test_find_resources(self):
        response = self.client.get(reverse('orgreport:find_resources'))
        self.assertEqual(response.status_code, 200)
    
    def test_submit_report(self):
        response = self.client.get(reverse('orgreport:report'))
        self.assertEqual(response.status_code, 200)

    def test_search_reports(self):
        response = self.client.get(reverse('orgreport:search_reports'))
        self.assertEqual(response.status_code, 200)
   
    def test_view_submitted_report(self):
        response = self.client.get(reverse('orgreport:s3_folder_view'))
        self.assertEqual(response.status_code, 200)

class CorrectTemplateTests(TestCase):
    def setUp(self):
        self.client = Client()
        super().setUp()
    def test_login_uses_correct_template(self):
        response = self.client.get(reverse('orgreport:login'))
        self.assertTemplateUsed(response, 'whistleblower_site/login.html')

    def test_home_uses_correct_template(self):
        response = self.client.get(reverse('orgreport:home'))
        self.assertTemplateUsed(response, 'whistleblower_site/home.html')

    def test_find_resources_uses_correct_template(self):
        response = self.client.get(reverse('orgreport:find_resources'))
        self.assertTemplateUsed(response, 'whistleblower_site/resources.html')

    def test_submit_report_correct_template(self):
        response = self.client.get(reverse('orgreport:report'))
        self.assertTemplateUsed(response, 'whistleblower_site/report.html')
    
    def test_search_reports_correct_template(self):
        response = self.client.get(reverse('orgreport:search_reports'))
        self.assertTemplateUsed(response, 'whistleblower_site/search_reports.html')
    
    def test_view_submitted_report_correct_template(self):
        response = self.client.get(reverse('orgreport:s3_folder_view'))
        self.assertTemplateUsed(response, 'whistleblower_site/s3_folder_view.html')

    def test_profile_uses_correct_template(self):
        email = 'user@gmail.com'
        user = User.objects.create_user(username='testuser', email=email)
        user.is_active = True
        user.save()

        self.client.force_login(user)

        response = self.client.get(reverse('orgreport:profile'))

        self.assertTemplateUsed(response, 'whistleblower_site/profile.html')


class ButtonRedirectTests(TestCase):
    def setUp(self):
        self.client = Client()
        email = 'user@gmail.com'
        user = User.objects.create_user(username='testuser', email=email)
        user.is_active = True
        user.save()
        self.client.force_login(user)
    
    def test_home_redirects_to_logout(self):
        home_response = self.client.get(reverse('orgreport:home'))
        self.assertEqual(home_response.status_code, 200)
        
        logout_response = self.client.post(reverse('orgreport:logout'))
        self.assertEqual(logout_response.status_code, 200)
    
    def test_home_redirects_to_find_resources(self):
        home_response = self.client.get(reverse('orgreport:home'))
        self.assertEqual(home_response.status_code, 200)

        find_resources_response = self.client.post(reverse('orgreport:find_resources'))
        self.assertEqual(find_resources_response.status_code, 200)
    
    def test_find_resources_redirects_to_home(self):
        find_resources_response = self.client.get(reverse('orgreport:find_resources'))
        self.assertEqual(find_resources_response.status_code, 200)

        home_response = self.client.post(reverse('orgreport:home'))
        self.assertEqual(home_response.status_code, 200)

    def test_home_redirects_to_search_reports(self):
        home_response = self.client.get(reverse('orgreport:home'))
        self.assertEqual(home_response.status_code, 200)

        search_report = self.client.post(reverse('orgreport:search_reports'))
        self.assertEqual(search_report.status_code, 200)
    

    def test_search_reports_redirects_to_home(self):
        search_report = self.client.get(reverse('orgreport:search_reports'))
        self.assertEqual(search_report.status_code, 200)

        home = self.client.post(reverse('orgreport:home'))
        self.assertEqual(home.status_code, 200)
    
    def test_home_redirects_to_submit_report(self):
        home_response = self.client.get(reverse('orgreport:home'))
        self.assertEqual(home_response.status_code, 200)

        submit_report = self.client.post(reverse('orgreport:report'))
        self.assertEqual(submit_report.status_code, 200)

    def test_submit_report_redirects_to_home(self):
        submit_report = self.client.get(reverse('orgreport:report'))
        self.assertEqual(submit_report.status_code, 200)

        home = self.client.post(reverse('orgreport:home'))
        self.assertEqual(home.status_code, 200)

    def test_home_redirects_to_view_submitted_report(self):
        home_response = self.client.get(reverse('orgreport:home'))
        self.assertEqual(home_response.status_code, 200)

        view_submitted_report = self.client.post(reverse('orgreport:s3_folder_view'))
        self.assertEqual(view_submitted_report.status_code, 200)
    
    def test_view_submitted_report_redirects_to_home(self):
        view_submitted_report = self.client.get(reverse('orgreport:s3_folder_view'))
        self.assertEqual(view_submitted_report.status_code, 200)

        home = self.client.post(reverse('orgreport:home'))
        self.assertEqual(home.status_code, 200)
    
    def test_home_redirects_to_profile(self):
        home_response = self.client.get(reverse('orgreport:home'))
        self.assertEqual(home_response.status_code, 200)

        profile = self.client.post(reverse('orgreport:profile'))
        self.assertEqual(profile.status_code, 200)
    
    def test_profile_redirects_to_home(self):
        profile = self.client.get(reverse('orgreport:profile'))
        self.assertEqual(profile.status_code, 200)

        home = self.client.post(reverse('orgreport:home'))
        self.assertEqual(home.status_code, 200)


class ButtonRedirectTests_Anonymous(TestCase):
    def setUp(self):
        self.client = Client()
        super().setUp()
    
    def test_home_redirects_to_logout(self):
        home_response = self.client.get(reverse('orgreport:home'))
        self.assertEqual(home_response.status_code, 200)
        
        logout_response = self.client.post(reverse('orgreport:logout'))
        self.assertEqual(logout_response.status_code, 200)
    
    def test_home_redirects_to_find_resources(self):
        home_response = self.client.get(reverse('orgreport:home'))
        self.assertEqual(home_response.status_code, 200)

        find_resources_response = self.client.post(reverse('orgreport:find_resources'))
        self.assertEqual(find_resources_response.status_code, 200)
    
    def test_find_resources_redirects_to_home(self):
        find_resources_response = self.client.get(reverse('orgreport:find_resources'))
        self.assertEqual(find_resources_response.status_code, 200)

        home_response = self.client.post(reverse('orgreport:home'))
        self.assertEqual(home_response.status_code, 200)

    def test_home_redirects_to_search_reports(self):
        home_response = self.client.get(reverse('orgreport:home'))
        self.assertEqual(home_response.status_code, 200)

        search_report = self.client.post(reverse('orgreport:search_reports'))
        self.assertEqual(search_report.status_code, 200)
    

    def test_search_reports_redirects_to_home(self):
        search_report = self.client.get(reverse('orgreport:search_reports'))
        self.assertEqual(search_report.status_code, 200)

        home = self.client.post(reverse('orgreport:home'))
        self.assertEqual(home.status_code, 200)
    
    def test_home_redirects_to_submit_report(self):
        home_response = self.client.get(reverse('orgreport:home'))
        self.assertEqual(home_response.status_code, 200)

        submit_report = self.client.post(reverse('orgreport:report'))
        self.assertEqual(submit_report.status_code, 200)

    def test_submit_report_redirects_to_home(self):
        submit_report = self.client.get(reverse('orgreport:report'))
        self.assertEqual(submit_report.status_code, 200)

        home = self.client.post(reverse('orgreport:home'))
        self.assertEqual(home.status_code, 200)

    def test_home_redirects_to_view_submitted_report(self):
        home_response = self.client.get(reverse('orgreport:home'))
        self.assertEqual(home_response.status_code, 200)

        view_submitted_report = self.client.post(reverse('orgreport:s3_folder_view'))
        self.assertEqual(view_submitted_report.status_code, 200)
    
    def test_view_submitted_report_redirects_to_home(self):
        view_submitted_report = self.client.get(reverse('orgreport:s3_folder_view'))
        self.assertEqual(view_submitted_report.status_code, 200)

        home = self.client.post(reverse('orgreport:home'))
        self.assertEqual(home.status_code, 200)
    