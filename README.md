# Just-CD
[![CircleCI](https://circleci.com/gh/7CStudio/just-cd/tree/master.svg?style=svg)](https://circleci.com/gh/7CStudio/just-cd/tree/master)
> Bare Bones continous deployment using circleci and Django

Just-CD lets you quickly set up Continous Integration and Deployment using CircleCi and Django.
All you have to do is deploy this on one of your servers and set up circleci.
Upon getting the webhook form CircleCI, just-cd ssh gets your latest code and reads the ```just_config.yaml```
file where you pass a list of branchs to process and respective ips ; pem_path or users depending if how you want 
to ssh into the machinem, and then sshes into your servers and runs the deployment script which should be a .sh file.

## Installation

OS X & Linux:

```
pip install -r /path/to/requirements.txt
```
and then deploy it like how you would deploy any other Django App
https://docs.djangoproject.com/en/1.9/howto/deployment/

## Usage example

For Just-CD to deploy your code make a just_config.yaml file like the follows:

```
Deploy:
  test_branch_name:
    deployment_script_path: path_to_deployment_script
    ip_addresses: [list of ip address for that branch]
    user: root/user for the server *optional
    pem_path: *optional
```
Also while setting up CircleCI in your circle.yml file, 
make sure you set up webhook for the app and make the appropriate changes in urls.py .
https://circleci.com/docs/configuration/#notify

## Meta

Manas Dadheech– [@MyFacebook](https://facebook.com/manas.dadheech) – manas@7cstudio.com

Distributed under the MIT license. See ``LICENSE.md`` for more information.


