#coding:utf-8

from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.template import RequestContext
#from django.template import Context
#from django.template.loader import get_template
from django.shortcuts import render_to_response

from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from deployment.forms import *

@login_required
def main_page(request):
    params = RequestContext(request, {
        'user': request.user
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
        project = request.POST.get('project')
        deploy_type = request.POST.get('deployType')
        if not project or not deploy_type:
            error_msg = '输入参数有误'
        else:
            #检查工程当前是否在发布， 并添加标识进入发布状态的代码
            #也可以把下面这些信息先写数据库里
            params = RequestContext(request, {
                'project': project,
                'deployType': deploy_type,
            })
            return render_to_response('deploy_project_page.html', params)
    params = RequestContext(request, {
        'error_msg': error_msg
    })
    return render_to_response('deploy_init_option_page.html', params)

@login_required
def deploy_project_page(request):
    params = RequestContext(request, {
        'project': 'passport',
        'environment': 'alpha',
        'deployType': 'war包',
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
