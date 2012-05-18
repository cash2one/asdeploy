#coding:utf-8

import os
import threading

from django.core.cache import cache

from deployment.models import *
from deployment.deploysetting import *

class Deployer(threading.Thread):
    def __init__(self, record):
        threading.Thread.__init__(self)
        self.record = record
        self.item = record.deploy_item
    
    def run(self):
        record_id_str = unicode(self.record.id)
        status_key = 'log_is_writing_' + record_id_str
        deploy_result_key = 'deploy_result_' + record_id_str
        cache.set(status_key, True, 7200)
        flag = _deploy_item(self.item)
        cache.set(deploy_result_key, flag)
        cache.delete(status_key)

# 获取文件上传存储的路径
def get_target_folder(proj_name, version):
    return ITEM_ROOT_PATH + proj_name + '-' + version + '/'


def _deploy_item(item):
    flag = False
    if not item:
        return False;
    
    if item.deploy_type == DeployItem.WAR:
        flag = _deploy_war(item)
    elif item.deploy_type == DeployItem.PATCH:
        flag = _deploy_patch(item)
    else:
        return False
    return flag

def _deploy_war(item):
    sh_path = _get_war_sh_path_by_item(item);
    sh_param = item.project.name + '-' + item.version
    sh_command = 'sh ' + sh_path + ' ' + sh_param + ' > ' + DEPLOY_LOG_PATH
    flag = os.system(sh_command)
    return flag == 0

def _get_war_sh_path_by_item(item):
    name = item.project.name + '-deploy'
    return SHELL_ROOT_PATH + name + '/' + name + '.sh'

def _deploy_patch(item):
    item_name = item.file_name
    rindex = item_name.lower().rindex('.zip')
    if rindex > 0:
        item_name = trim_compress_suffix(item_name)
    sh_path = _get_patch_sh_path_by_item(item)
    sh_param = ITEM_ROOT_PATH + item.project.name + '-' + item.version + '/' + item_name
    sh_command = 'sh ' + sh_path + ' ' + sh_param + ' > ' + DEPLOY_LOG_PATH
    flag = os.system(sh_command)
    return flag == 0

def _get_patch_sh_path_by_item(item):
    return SHELL_ROOT_PATH + 'patch-shell/start_patch_main.sh'

def trim_compress_suffix(filename):
    if not filename or len(filename) == 0:
        return filename
    filename = filename.lower()
    rindex = filename.rindex('.zip')
    if rindex > 0:
        filename = filename[:rindex]
    return filename

if __name__ == '__main__':
    pass
