'''
    handles all kind of database connection tasks
'''

from django.db import models


class users(models.Model):
    """Store users information"""

    user_name = models.CharField(max_length=50,null=False,blank=False,primary_key=True)
    password = models.CharField(max_length=50,null=False,blank=False)
    token = models.CharField(max_length=500,null=False,blank=False)
    token_expire_time = models.DateTimeField(null=False,blank=False)

class news(models.Model):
    """Store news information"""
    news_id =  models.AutoField(serialize=True, auto_created=True, primary_key=True)
    title = models.CharField(max_length=50000, null=False, blank=False)
    body = models.CharField(max_length=50000, null=False, blank=False)
    author = models.CharField(max_length=50000, null=False, blank=False)

