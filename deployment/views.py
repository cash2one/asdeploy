#coding:utf-8

import json
from datetime import datetime

from django.core.cache import cache
from django.db.models import Q

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
from deployment.logutil import *

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
        proj_id_str = request.POST.get('projId')
        deploy_type = request.POST.get('deployType')
        version = request.POST.get('version')
        cur_lock = _check_lock()
        if not proj_id_str or not deploy_type or not version:
            error_msg = '输入参数有误'
        elif cur_lock:
            return HttpResponseRedirect('/')
        else:
            proj_id = int(proj_id_str)
            project = Project.objects.get(pk = proj_id)
            _params = {
                'project': project,
                'deployType': deploy_type,
                'version': version,
            }
            (record, lock) = _before_deploy_project(request, _params)
            _params['record'] = record
            _params['lock'] = lock
            params = RequestContext(request, _params)
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

@login_required
def unlock_deploy(request):
    curUser = request.user
    curLock = _check_lock()
    # 这里应该取出权限信息进行判定，先简单写成这样吧
    if curLock and (curUser.username == 'admin' or curUser.id == curLock.user.id):
        curLock.is_locked = False
        curLock.save()
    return HttpResponseRedirect('/')

#@login_required
#def deploy_project_page(request):
#    params = RequestContext(request, {
#        'project': 'passport',
#        'version': '1.1',
#        'deployType': 'war',
#    })
#    return render_to_response('deploy_project_page.html', params)

@login_required
def deploy_record_list_page(request, page_num=1):
#    username = request.GET.get('username')
#    begin_date = request.GET.get('begin_date')
#    end_date = request.GET.get('end_date')
#    project_name = request.GET.get('project_name')
    projects = Project.objects.all()
    conditions = []
    query_params = {}
    if request.POST:
        username = request.POST.get('username')
        if username:
            query_params['username'] = username
            conditions.append(Q(user__username__icontains = username))
        proj_id = int(request.POST.get('project'))
        if proj_id:
            query_params['project'] = proj_id
            conditions.append(Q(project__id = proj_id))
        version = request.POST.get('version')
        if version:
            query_params['version'] = version
            conditions.append(Q(deploy_item__version = version))
        deploy_type = request.POST.get('deployType')
        if deploy_type:
            query_params['deploy_type'] = deploy_type
            conditions.append(Q(deploy_item__deploy_type = deploy_type))
        start_time = request.POST.get('startTime')
        if start_time:
            query_params['start_time'] = start_time
            conditions.append(Q(create_time__gte = start_time))
        end_time = request.POST.get('endTime')
        if end_time:
            query_params['end_time'] = end_time
            conditions.append(Q(create_time__lte = end_time))
    records = DeployRecord.objects.filter(*conditions).order_by('-id')
    for record in records:
        record.formated_create_time = record.create_time.strftime('%Y-%m-%d %H:%M:%S')
    params = RequestContext(request, {
        'projects': projects,
        'records': records,
        'query_params': query_params,
    })
    return render_to_response('deploy_record_list_page.html', params) 

@login_required
def deploy_record_detail_page(request, record_id):
    record = DeployRecord.objects.get(pk = record_id)
    params = RequestContext(request, {
        'record': record
    })
    return render_to_response('deploy_record_detail_page.html', params)

@login_required
def upload_deploy_item(request):
    params = {}
    if request.POST and request.FILES:
        proj_id = int(request.POST.get('projId'))
        record_id = int(request.POST.get('recordId'))
        version = request.POST.get('version')
        deploy_type = request.POST.get('deployType')
        deploy_item_file = request.FILES.get('deployItemField')
        filename = deploy_item_file.name
        size = deploy_item_file.size
        # 路径配置信息待改
        folderpath = _generate_folder_path()
        destination = open(folderpath + filename, 'wb+')
        for chunk in deploy_item_file.chunks():
            destination.write(chunk)
        destination.close()
        
        items = DeployItem.objects.filter(file_name__exact = filename )
        item = (items and len(items) > 0) and items[0] or None
        now_time = datetime.now()
        if not item:
            item = DeployItem(
                user = request.user,
                project = Project.objects.get(pk = proj_id),
                version = version,
                deploy_type = deploy_type,
                file_name = filename,
                folder_path = folderpath,
                create_time = now_time,
                update_time = now_time
            )
        else:
            item.update_time = now_time
        item.save()
        
        record = DeployRecord.objects.get(pk = record_id)
        if record:
            record.status = DeployRecord.UPLOADED
            record.deploy_item = item;
            record.save()
            
        params['filename'] = filename
        params['size'] = size
        params['isSuccess'] = True
    else:
        params['isSuccess'] = False
    return HttpResponse(json.dumps(params))

@login_required
def start_deploy(request):
    # 注意发布前还要检查状态，至少为uploaded
    params = None
    if request.POST and request.POST.get('recordId'):
        record_id_str = request.POST.get('recordId')
        if not cache.get('log_is_writing_' + record_id_str):
            record_id = int(record_id_str)
            filepath = _generate_folder_path()
            filename = _get_file_name()
            log_reader = LogReader(record_id, filename, filepath)
            cache.set('log_reader_' + record_id_str, log_reader, 300)
            log_writer = LogWriter(
                record_id = record_id, 
                filename = filename, 
                filepath = filepath
            )
            log_writer.start()
            params = {
                'beginDeploy': True,
            }
            
    if not params:
        params = {
            'beginDeploy': False
        }
    return HttpResponse(json.dumps(params))

@login_required
def read_deploy_log_on_realtime(request):
    record_id_str = request.GET.get('recordId')
    params = {}
    if record_id_str:
        # log_reader在start_deploy的时候生成并放入cache
        log_reader_key = 'log_reader_' + record_id_str
        log_reader = cache.get(log_reader_key)
        if log_reader:
            params['logInfo'] = log_reader.read_lines()
            params['isFinished'] = False
            if cache.get('log_is_writing_' + record_id_str):
                cache.set(log_reader_key, log_reader, 300)
            else:
                cache.delete(log_reader_key)
            return HttpResponse(json.dumps(params))
    params['isFinished'] = True
    return HttpResponse(json.dumps(params))

def _generate_folder_path():
    return 'c:/tempfiles/'

def _get_file_name():
    return 'test.log'
