from django.db import models

from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length = 30)
    
    def __unicode__(self):
        return 'name=[' + self.name + ']';
    
    class Meta:
        db_table = 'dpl_project'


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
    
    class Meta:
        db_table = 'dpl_deployitem'


class DeployRecord(models.Model):
    PREPARE = 'prepare'
    PUBLISING = 'deploying'
    SUCCESS = 'success'
    FAILURE = 'failure'
    ROLLBACK = 'rollback'
    
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    deploy_item = models.ForeignKey(DeployItem, null = True)
    create_time = models.DateTimeField()
    status = models.CharField(max_length = 15)
    
    class Meta:
        db_table = 'dpl_deployrecord'
    
    

class DeployLock(models.Model):
    user = models.ForeignKey(User)
    deploy_record = models.ForeignKey(DeployRecord)
    is_locked = models.BooleanField(default = False)
    locked_time = models.DateTimeField()
    
    class Meta:
        db_table = 'dpl_deploylock'