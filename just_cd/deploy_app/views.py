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


@api_view(['POST'])
def deploy_view(request):
    if request.data['payload']['outcome'] == 'success':
        if (check_if_repo_exists(request.data['payload']['reponame'])):
            print('repository exists')
            git_pull(request.data['payload']['reponame'],
                     request.data['payload']['branch'],
                     request.data['payload']['vcs_revision'])
        else:
            git_clone(request.data['payload']['vcs_url'])
        config_dict = open_just_config(request.data['payload']['reponame'])
        allowed_branches = config_dict['Deploy'].keys()
        for branch in allowed_branches:
            if (request.data['payload']['branch'] == branch):
                print('branch in just_config' + branch)
                branch_dict = config_dict['Deploy'][branch]
                deployment_script_path = branch_dict['deployment_script_path']
                ip_addresses = branch_dict['ip_addresses']
                user = branch_dict['user']
                pem_path = branch_dict.get('pem_path', '')
                for ip in ip_addresses:
                    ssh_to_ip(pem_path, ip, deployment_script_path, user)
            else:
                continue
    return Response(status=status.HTTP_400_BAD_REQUEST)


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


def process_status(
        request, process_output, process_status,
        ip, server_type, build_info_obj):
    print(process_output)
    if process_status == 0:
        build_info_item = ServerBuildInfo(
            is_success=True,
            console_output=process_output,
            ip=ip,
            server_type=server_type,
            build_info=build_info_obj)
        build_info_obj.deployment_status = True
        build_info_obj.save()
        build_info_item.save()
    else:
        build_info_item = ServerBuildInfo(
            is_success=False,
            console_output=process_output,
            ip=ip,
            server_type=server_type,
            build_info=build_info_obj)
        build_info_obj.deployment_status = False
        build_info_obj.save()
        build_info_item.save()


def check_if_repo_exists(reponame):
    print(os.path.join(os.getcwd(), reponame))
    print(os.path.isdir(os.path.join(os.getcwd(), reponame)))
    return os.path.isdir(os.path.join(os.getcwd(), reponame))


def git_pull(reponame, branch, vcs_revision):
    process_output = subprocess.check_output(
        ['bash', 'pull_branch_commit.sh', reponame, branch, vcs_revision],
        stdin=subprocess.PIPE)
    print(process_output)


def git_clone(vcs_url):
    repo_path = vcs_url.replace('https://github.com/', '', 1)
    process_output = subprocess.check_output(
        ['yes', '|', 'yes', 'git', 'clone', 'git@github.com:' + repo_path],
        stdin=subprocess.PIPE)
    print(process_output)


def open_just_config(reponame):
    if (os.path.isfile(os.path.join(os.getcwd(),
                                    reponame, 'just_config.yml'))):
        file_path = os.path.join(os.getcwd(), reponame, 'just_config.yml')
        with open(file_path, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)


def ssh_to_ip(pem_path, ip_addr, deployment_script_path, user):
    if (len(pem_path) > 0):
        process_output = subprocess.check_output(['bash', 'ssh_with_pem.sh',
                                                 pem_path, ip_addr,
                                                 deployment_script_path],
                                                 stdin=subprocess.PIPE)
        return(process_output)
    else:
        ssh_ip_with_user = user + '@' + ip_addr
        print(ssh_ip_with_user)
        process_output = subprocess.check_output(['bash', 'ssh_sans_pem.sh',
                                                 ssh_ip_with_user,
                                                 deployment_script_path],
                                                 stdin=subprocess.PIPE)
        return(process_output)
