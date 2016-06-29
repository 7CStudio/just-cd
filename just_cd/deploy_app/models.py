from django.db import models

# Create your models here.


class ServerType(object):
    APP_SERVER = 'app_server'
    WORKER = 'celery_worker'


class BuildInfo(models.Model):
    circleci_json = models.TextField()
    branch = models.CharField(max_length=255)
    commiter = models.CharField(max_length=255)
    circleci_url = models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    vcs_revision = models.CharField(max_length=255)
    deployment_status = models.BooleanField(default=False)


class ServerBuildInfo(models.Model):
    ip = models.GenericIPAddressField()
    server_type = models.CharField(max_length=255)
    is_success = models.BooleanField(default=False)
    console_output = models.TextField()
    build_info = models.ForeignKey(BuildInfo)
