from django.test import TestCase

# Create your tests here.


from django.test import TestCase
from mock import MagicMock, patch
from just_cd.deploy_app.deploy_manager import git_pull, git_clone
import subprocess


class GitTestCase(TestCase):

    @patch('subprocess.check_output')
    def test_git_pull(self, subprocess_check_output):
        val = git_pull('test_repo', 'test_cd',
                       '11b5d65eb6faebb43dd3b2a559c3b5cb6e1bdf42')
        subprocess_check_output.assert_called_once_with(
            ['bash', 'pull_branch_commit.sh', 'test_repo',
             'test_cd', '11b5d65eb6faebb43dd3b2a559c3b5cb6e1bdf42'],
            stdin=subprocess.PIPE)

    @patch('subprocess.check_output')
    def test_git_clone(self, subprocess_check_output):
        val = git_clone('https://github.com/test_repo')
        subprocess_check_output.assert_called_once_with(
            ['bash', 'clone_code.sh', 'git@github.com:' + 'test_repo.git'],
            stdin=subprocess.PIPE)
