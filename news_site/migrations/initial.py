from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('user_name', models.CharField(max_length=50,null=False,blank=False,primary_key=True)),
                ('password', models.CharField(max_length=50,null=False,blank=False)),
                ('token', models.CharField(max_length=500,null=False,blank=False)),
                ('token_expire_time', models.DateTimeField(null=False,blank=False)),
            ],
        ),

        migrations.CreateModel(
            name='news',
            fields=[
                ('news_id', models.AutoField(serialize=True,auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50000, null=False, blank=False)),
                ('body', models.CharField(max_length=50000, null=False, blank=False)),
                ('author', models.CharField(max_length=50000,null=False, blank=False)),
            ],
        ),
    ]
