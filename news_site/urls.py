"""
    handles url
"""
from django.conf.urls import include, url
from django.contrib import admin
from views import *

urlpatterns = [
    url(r'^$', LoginPage),
    url(r'^all_story/$', all_story),
    url(r'^all_story/search_suggestions/$', search_suggestions),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^all_story/create_story/$', create_story),
    url(r'^all_story/read_story/$', read_story),
    url(r'^all_story/update_story/$', update_story),
    url(r'^all_story/delete_story/$', delete_story),
    url(r'^signup/$', signup),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
]
