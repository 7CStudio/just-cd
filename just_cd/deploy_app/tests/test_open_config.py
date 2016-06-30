from django.test import TestCase

# Create your tests here.


from just_cd.deploy_app.views import open_just_config


class OpenConfigTestCase(TestCase):
    def setUp(self):
        path = os.path.join(settings.BASE_DIR, 'test_repo')
        os.mkdir(path)
        open(os.path.join(settings.BASE_DIR, 'test_repo', 'just_config.yaml'))

    def test_open_config_file_not_present(self):
        


    def tearDown(self):
        self.widget.dispose()

