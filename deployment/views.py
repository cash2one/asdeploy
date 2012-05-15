#coding:utf-8

import json
from datetime import datetime

from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.template import RequestContext
#from django.template import Context
#from django.template.loader import get_template
from django.shortcuts import render_to_response

from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from deployment.models import *
from deployment.forms import *

@login_required
def main_page(request):
    cur_lock = _check_lock()
    params = RequestContext(request, {
        'user': request.user,
        'curLock': cur_lock
    })
    return render_to_response('main_page.html', params)

@login_required
def user_page(request, username):
    try:
        user = User.objects.get(username = username)
    except:
        raise Http404('Requested user not found.')
    
    params = RequestContext(request, {
        'username': user.username,
    })
    return render_to_response('user_page.html', params)

@login_required
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username = form.cleaned_data.get('username'), 
                password = form.cleaned_data.get('password1'),
                email = form.cleaned_data.get('email')
            )
            return HttpResponseRedirect('/register/success')
    else:
        form = RegistrationForm()
    params = RequestContext(request, {
        'form': form,
    })
    return render_to_response('registration/register.html', params)


########业务相关########
@login_required
def deploy_init_option_page(request):
    error_msg = None
    if request.POST:
        proj_id_str = request.POST.get('project')
        deploy_type = request.POST.get('deployType')
        version = request.POST.get('version')
        cur_lock = _check_lock()
        if not proj_id_str or not deploy_type or not version:
            error_msg = '输入参数有误'
        elif cur_lock:
            return HttpResponseRedirect('/')
        else:
            #检查工程当前是否在发布， 并添加标识进入发布状态的代码
            #也可以把下面这些信息先写数据库里
            proj_id = int(proj_id_str)
            project = Project.objects.get(pk = proj_id)
            map = {
                'project': project,
                'deployType': deploy_type,
                'version': version,
            }
            (record, lock) = _before_deploy_project(request, map)
            map['record'] = record
            map['lock'] = lock
            params = RequestContext(request, map)
            return render_to_response('deploy_project_page.html', params)
    params = RequestContext(request, {
        'error_msg': error_msg,
        'projects': Project.objects.all()
    })
    return render_to_response('deploy_init_option_page.html', params)

def _check_lock():
    locks = DeployLock.objects.filter(is_locked = True)
    if len(locks) >= 1:
        return locks[0]
    return None

def _before_deploy_project(request, params):
    # create DeployRecord
    # create DeployLock and build the relationship between it and DeployRecord
    project = params.get('project');
    record = DeployRecord(
        user = request.user,
        project = project,
        create_time = datetime.now(),
        status = DeployRecord.PREPARE
    )
    record.save()
    lock = DeployLock(
        user = request.user,
        deploy_record = record,
        is_locked = True,
        locked_time = datetime.now()
    )
    lock.save()
    return (record, lock)

def unlock_deploy(request):
    curUser = request.user
    curLock = _check_lock()
    if curLock and (curUser.username == 'admin' or curUser.id == curLock.user.id):
        curLock.is_locked = False
        curLock.save()
    return HttpResponseRedirect('/')

@login_required
def deploy_project_page(request):
    params = RequestContext(request, {
        'project': 'passport',
        'version': '1.1',
        'deployType': 'war',
    })
    return render_to_response('deploy_project_page.html', params)

@login_required
def deploy_record_list_page(request, page_num=1):
#    username = request.GET.get('username')
#    begin_date = request.GET.get('begin_date')
#    end_date = request.GET.get('end_date')
#    project_name = request.GET.get('project_name')
    params = RequestContext(request, {
        'iters': range(25)
    })
    return render_to_response('deploy_record_list_page.html', params) 

@login_required
def deploy_record_detail_page(request, deploy_record_id):
    params = RequestContext(request)
    return render_to_response('deploy_record_detail_page.html', params)

@login_required
def upload_deploy_item(request):
    params = {}
    if request.POST and request.FILES:
        project = request.POST.get('project')
        version = request.POST.get('version')
        deploy_type = request.POST.get('deployType')
        deploy_item_file = request.FILES.get('deployItemField')
        filename = deploy_item_file.name
        size = deploy_item_file.size
        # 路径配置信息待改
        destination = open('c:/tempfiles/copys/' + filename, 'wb+')
        for chunk in deploy_item_file.chunks():
            destination.write(chunk)
        destination.close()
        params['filename'] = filename
        params['size'] = size
        params['isSuccess'] = True
    else:
        params['isSuccess'] = False
    return HttpResponse(json.dumps(params))
