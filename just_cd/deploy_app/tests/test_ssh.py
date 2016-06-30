from django.test import TestCase

# Create your tests here.


from django.test import TestCase
from mock import MagicMock, patch
from just_cd.deploy_app.views import ssh_to_ip
import subprocess


class ConfigTestCase(TestCase):

    @patch('subprocess.check_output')
    def test_ssh_to_ip(self, subprocess_check_output):
        subprocess_check_output.return_value = "test"

        val = ssh_to_ip('pem_path', '1.0.0.0', 'deployment_script_path', '')

        subprocess_check_output.assert_called_once_with(
            ['bash', 'ssh_with_pem.sh', 'pem_path', '1.0.0.0',
             'deployment_script_path'],
            stdin=subprocess.PIPE)
        assert val == "test"

    @patch('subprocess.check_output')
    def test_ssh_to_ip_sans_pem_path(self, subprocess_check_output):
        subprocess_check_output.return_value = "test"

        val = ssh_to_ip('', '1.0.0.0', 'deployment_script_path', 'root')

        subprocess_check_output.assert_called_once_with(
            ['bash', 'ssh_sans_pem.sh', 'root@1.0.0.0',
             'deployment_script_path'],
            stdin=subprocess.PIPE)
        assert val == "test"
