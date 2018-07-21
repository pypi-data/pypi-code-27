from django.contrib.auth.models import User


class SeleniumLoginMixin:

    def setUp(self):
        User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@example.com')
        super().setUp()

    def login(self):
        """Edc login with custom template.
        """
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('admin')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('admin')
        self.selenium.find_element_by_xpath('//input[@value="Login"]').click()
        self.selenium.implicitly_wait(3)
