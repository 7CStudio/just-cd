from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from just_cd.deploy_app.models import (BuildInfo,
                                       ServerBuildInfo)
import subprocess
from django.shortcuts import render_to_response
import yaml
from django.shortcuts import get_object_or_404
import os
from django.conf import settings
from just_cd.deploy_app.deploy_manager import *


@api_view(['POST'])
def deploy_view(request):
    if request.data['payload']['outcome'] == 'success':
        build_info_obj = save_build_object(request)
        clone_or_pull_repo(request)
        config_dict = open_just_config(request.data['payload']['reponame'])
        if (config_dict == None):
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        allowed_branches = config_dict['Deploy'].keys()
        deploy_build(request, config_dict, allowed_branches)
        
    return Response(status=status.HTTP_200_OK)

def build_list_view(request):
    build_info = BuildInfo.objects.all().order_by('-id')[:10]
    return render_to_response(
        'build_list.html', {'build_list': build_info})

def build_detail_view(request, id):
    build_info = get_object_or_404(BuildInfo, id=id)
    serverbuildinfo_list = build_info.serverbuildinfo_set.all().order_by('-id')
    return render_to_response(
        'build_info.html',
        {'build_info_item': build_info,
         'serverbuildinfo_list': serverbuildinfo_list})
