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

def process_status(process_output, process_status,
                   ip, build_info_obj):
    is_success = False
    deployment_status = False
    if (process_status == 0):
        is_success = True
        deployment_status = True
    build_info_item = ServerBuildInfo(
            is_success=is_success,
            console_output=process_output,
            ip=ip,
            build_info=build_info_obj)
    build_info_obj.deployment_status = deployment_status
    build_info_obj.save()
    build_info_item.save()


def check_if_repo_exists(reponame):
    return os.path.isdir(os.path.join(settings.BASE_DIR, reponame))


def git_pull(reponame, branch, vcs_revision):
    process_output = subprocess.check_output(
        ['bash', 'pull_branch_commit.sh', reponame, branch, vcs_revision],
        stdin=subprocess.PIPE)


def git_clone(vcs_url):
    repo_path = vcs_url.replace('https://github.com/', '', 1)
    process_output = subprocess.check_output(
        ['bash', 'clone_code.sh', 'git@github.com:' + repo_path +'.git'],
        stdin=subprocess.PIPE)


def open_just_config(reponame):
    if (os.path.isfile(os.path.join(settings.BASE_DIR,
                                    reponame, 'just_config.yaml'))):
        file_path = os.path.join(settings.BASE_DIR,
                                 reponame, 'just_config.yaml')
        with open(file_path, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                return exc


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

def save_build_object(request):
    build_info_obj = BuildInfo(
            circleci_json=request.data,
            branch=request.data['payload']['branch'],
            commiter=request.data['payload']['author_name'],
            circleci_url=request.data['payload']['build_url'],
            vcs_revision=request.data['payload']['vcs_revision'])
    build_info_obj.save()
    return build_info_obj

def clone_or_pull_repo(request):
    if (check_if_repo_exists(request.data['payload']['reponame'])):
        print('repository exists')
        git_pull(request.data['payload']['reponame'],
                 request.data['payload']['branch'],
                 request.data['payload']['vcs_revision'])
    else:
        git_clone(request.data['payload']['vcs_url'])

def deploy_build(request, config_dict, allowed_branches):
    for branch in allowed_branches:
        if (request.data['payload']['branch'] == branch):
            print('branch in just_config' + branch)
            branch_dict = config_dict['Deploy'][branch]
            deployment_script_path = branch_dict['deployment_script_path']
            ip_addresses = branch_dict['ip_addresses']
            user = branch_dict.get('user', '')
            pem_path = branch_dict.get('pem_path', '')
            for ip in ip_addresses:
                try:
                    console_output = ssh_to_ip(pem_path, ip,
                                               deployment_script_path,
                                               user)
                    process_status(
                            request, console_output, 0, ip,
                            build_info_obj)
                except subprocess.CalledProcessError as e:
                    process_status(
                            request, e.output, 1, ip,
                            build_info_obj)
