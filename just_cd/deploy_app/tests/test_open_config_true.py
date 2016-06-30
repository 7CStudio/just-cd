from django.test import TestCase

# Create your tests here.


from just_cd.deploy_app.views import open_just_config
import os
from django.conf import settings
import shutil
import yaml


class OpenConfigValidTestCase(TestCase):
    def setUp(self):
        path = os.path.join(settings.BASE_DIR, 'test_repo')
        if not os.path.isdir(path):
            os.mkdir(path)
        d = {'Deploy': 'test'}
        with open(os.path.join(settings.BASE_DIR, 'test_repo',
                  'just_config.yaml'), 'w') as yaml_file:
            yaml_file.write(yaml.dump(d, default_flow_style=False))

    def test_open_config_file_correct(self):
        result = open_just_config('test_repo')
        print(result)
        assert ('Deploy' in result)

    def tearDown(self):
        path = os.path.join(settings.BASE_DIR, 'test_repo')
        # os.remove(os.path.join(settings.BASE_DIR,
        #           'test_repo', 'just_config.yaml'))
        # os.rmdir(path)
        shutil.rmtree(path)
