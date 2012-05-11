from django.db import models

from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length = 30)


class DeployItem(models.Model):
    DEPLOY_TYPE = {
        'WAR': 'war',
        'PATCH': 'patch'
    }
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    version = models.CharField(max_length = 11)
    deploy_type = models.CharField(max_length=15)
    folder_path = models.FilePathField(null = True)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField(null = True)


class DeployRecord(models.Model):
    DEPLOY_STATUS = {
        'PREPARE': 'prepare',
        'PUBLISING': 'publishing',
        'SUCCESS': 'success',
        'FAILURE': 'failure',
        'ROLLBACK': 'rollback',
    }
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    deploy_item = models.ForeignKey(DeployItem, null = True)
    create_time = models.DateTimeField()
    status = models.CharField(max_length = 15)
    
    

class PublishLock(models.Model):
    user = models.ForeignKey(User)
    deploy_record = models.ForeignKey(DeployRecord)
    is_locked = models.BooleanField(default = False)
    locked_time = models.DateTimeField()