from django.test import TestCase

# Create your tests here.


from just_cd.deploy_app.views import process_status
from just_cd.deploy_app.models import (BuildInfo,
                                       ServerBuildInfo)


class ProcessOutputTestCase(TestCase):

    def test_process_status_true(self):
        build_info_obj = BuildInfo(
            circleci_json='test request data',
            branch='test_branch',
            commiter='test_commiter',
            circleci_url='www.circleci.com',
            vcs_revision='11b5d65eb6faebb43dd3b2a559c3b5cb6e1bdf42')
        build_info_obj.save()

        process_status('test_string', 0, '1.0.0.1', build_info_obj)

        serverBuildInfo = ServerBuildInfo.objects.get(
            build_info=build_info_obj)
        assert (serverBuildInfo.console_output == 'test_string')
        db_build_info = BuildInfo.objects.get(
            vcs_revision='11b5d65eb6faebb43dd3b2a559c3b5cb6e1bdf42')
        assert (db_build_info.deployment_status is True)

    def test_process_status_false(self):
        build_info_obj = BuildInfo(
            circleci_json='test request data',
            branch='test_branch',
            commiter='test_commiter',
            circleci_url='www.circleci.com',
            vcs_revision='11b5d65eb6faebb43dd3b2a559c3b5cb6e1bdf43')
        build_info_obj.save()

        process_status('test_string', 1, '1.0.0.1', build_info_obj)

        serverBuildInfo = ServerBuildInfo.objects.get(
            build_info=build_info_obj)
        assert (serverBuildInfo.console_output == 'test_string')
        db_build_info = BuildInfo.objects.get(
            vcs_revision='11b5d65eb6faebb43dd3b2a559c3b5cb6e1bdf43')
        assert (db_build_info.deployment_status is False)
