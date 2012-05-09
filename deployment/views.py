#coding:utf-8

from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.template import RequestContext
#from django.template import Context
#from django.template.loader import get_template
from django.shortcuts import render_to_response

from django.contrib.auth.models import User
from django.contrib.auth import logout

from deployment.forms import *

def main_page(request):
    params = RequestContext(request, {
        'user': request.user
    })
    return render_to_response('main_page.html', params)

def user_page(request, username):
    try:
        user = User.objects.get(username = username)
    except:
        raise Http404('Requested user not found.')
    
    params = RequestContext(request, {
        'username': user.username,
    })
    return render_to_response('user_page.html', params)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def register_page(request):
    error_message = None
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
            error_message = '注册信息有误'
    else:
        form = RegistrationForm()
    params = RequestContext(request, {
        'form': form,
#        error_message: error_message
    })
    return render_to_response('registration/register.html', params)


########业务相关########

def deploy_record_list_page(request, page_num=1):
#    username = request.GET.get('username')
#    begin_date = request.GET.get('begin_date')
#    end_date = request.GET.get('end_date')
#    project_name = request.GET.get('project_name')
    params = RequestContext(request, {
        'iters': range(25)
    })
    return render_to_response('deploy_record_list_page.html', params) 

def deploy_record_detail_page(request, deploy_record_id):
    return render_to_response('deploy_record_detail_page.html')
