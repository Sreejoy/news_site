'''
    imports
'''
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from .models import users,news
from django.db.models import Q
from datetime import datetime,timedelta
import os,binascii
import simplejson


#generates random token for authentication
def generate_token():
    return str(binascii.b2a_hex(os.urandom(200)))

#validates token from "users" table
def validate_token(token):
    try:
        login_status = True
        try:
            user = users.objects.get(token=token)
        except:
            login_status = False

        if login_status:
            expire_time = user.token_expire_time
            now=timezone.now()
            if now < expire_time:
                return True
            else:
                return False
        else:
            return False
    except Exception,e:
        print e
        return False

#creates new story, input - title,body,author, writes to "news" table of database, returns code '1' if successful, '0' if otherwise
def create_story(request):
    result = {}
    if request.method == "POST":
        try:
            title = str(request.POST['title'].encode('utf-8').strip())
            body = str(request.POST['body'].encode('utf-8').strip())
            author = str(request.POST['author'].encode('utf-8').strip())
            token = str(request.POST['token'].encode('utf-8').strip())
            if not validate_token(token): #authorization by token
                result['code'] = '0'
                result['message'] = "Unauthorized request"
                result = simplejson.dumps(result)
                return HttpResponse(result, content_type='application/json')

            insert_status = True
            try:
                news_object = news(
                    title=title,
                    body=body,
                    author=author
                )
                news_object.save()
            except Exception,e:
                print e
                insert_status = False


            if insert_status:
                result['code'] = '1'
                result['message'] = "Successfully created story."
            else:
                result['code'] = '0'
                result['message'] = "Couldn't create story."
        except:
            result['code'] ='0'
            result['message']="Couldn't create story."
    result = simplejson.dumps(result)
    return HttpResponse(result, content_type='application/json')

def get_xml_string(key,value):
    return "<%s>%s</%s>"%(key,value,key)

#(used in story search)reads story, input - search_text,method(text/json), returns news in json/text, returns code '1' if successful, '0' if otherwise
def read_story(request):
    result = {}
    if request.method == "GET":
        try:
            search_text = str(request.GET.get(u'search_text', '').encode('utf-8').strip())
            try:
                news_id = int(search_text)
            except:
                news_id = -1
            method = str(request.GET.get(u'method', '').encode('utf-8').strip()) # can be text or json
            token = str(request.GET.get(u'token', '').encode('utf-8').strip())
            item_per_page = int(request.GET.get(u'item_per_page', '').encode('utf-8').strip())
            item_page_current = int(request.GET.get(u'item_page_current', '').encode('utf-8').strip())
            start_ = (item_per_page) * (item_page_current - 1)
            end_ = start_ + item_per_page
            if not validate_token(token): #authorization by token
                result['code'] = '0'
                result['message'] = "Unauthorized request"
                result = simplejson.dumps(result)
                return HttpResponse(result, content_type='application/json')

            try:
                stories = news.objects.filter(Q(title__contains=search_text)|Q(author__contains=search_text)|Q(body__contains=search_text)|Q(news_id=news_id)).order_by('news_id').reverse()
            except Exception,e:
                print e
                stories = False

            story_data = []
            for story in stories:
                story_data.append([story.news_id, story.title, story.body, story.author])

            if str(method) == 'json': #for json format
                if stories: # news found by given id
                    Heading = ['News']

                    result['TableData'] = story_data
                    result['count'] = len(result['TableData'])
                    result['TableData']= result['TableData'][start_:end_]
                    #result['TableData']=story

                    result['code'] = 1
                    result['Heading']=Heading
                else:
                    result['TableData'] = []
                    result['code'] = '0'
                    result['message'] = "Couldn't find story for search='%s'" % search_text

                json = simplejson.dumps(result)
                return HttpResponse(json, content_type='application/json')
            else: #for text/xml format
                xml_string="<all_news>"
                if story_data: # news found by given id
                    xml_string += get_xml_string('code', '1')
                    for each in story_data:
                        xml_string += "<news>"
                        xml_string += get_xml_string('news_id', each[0])
                        xml_string += get_xml_string('title', each[1])
                        xml_string += get_xml_string('body', each[2])
                        xml_string += get_xml_string('author', each[3])
                        xml_string += "</news>"
                else:
                    xml_string += get_xml_string('code', '0')
                    xml_string += get_xml_string('message', "Couldn't find story for search_text='%s'" % search_text)
                xml_string += "</all_news>"
                return HttpResponse(xml_string, content_type='application/xml')

        except Exception,e:
            print e
            result['code'] ='0'
            result['message']="Couldn't read story"
    result = simplejson.dumps(result)
    return HttpResponse(result, content_type='application/json')


#updates story in json format, input - news_id,title,body,author, updates "news" table of database, returns code '1' if successful, '0' if otherwise
def update_story(request):
    result = {}
    if request.method == "POST":
        try:
            news_id = str(request.POST['news_id'].encode('utf-8').strip())
            title = str(request.POST['title'].encode('utf-8').strip())
            body = str(request.POST['body'].encode('utf-8').strip())
            author = str(request.POST['author'].encode('utf-8').strip())
            token = str(request.POST['token'].encode('utf-8').strip())
            if not validate_token(token):  # authorization by token
                result['code'] = '0'
                result['message'] = "Unauthorized request"
                result = simplejson.dumps(result)
                return HttpResponse(result, content_type='application/json')

            exist_status = True
            try:
                news.objects.get(news_id=news_id)
            except Exception,e:
                print e
                exist_status = False

            if exist_status:
                update_dict={
                    'title':title,
                    'body':body,
                    'author':author
                }

                update_status = True
                try:
                    news.objects.filter(news_id=news_id).update(**update_dict)
                except Exception, e:
                    print e
                    update_status = False

                if update_status:
                    result['code'] = '1'
                    result['message'] = "Successfully updated story."
                else:
                    result['code'] = '0'
                    result['message'] = "Couldn't update story."
            else:
                result['code'] = '0'
                result['message'] = "Couldn't find story with id='%s'"%news_id
        except:
            result['code'] ='0'
            result['message']="Couldn't update story."
    result = simplejson.dumps(result)
    return HttpResponse(result, content_type='application/json')


#deletes story, input - news_id, deletes story from "news" table of database, returns code '1' if successful, '0' if otherwise
def delete_story(request):
    result = {}
    if request.method == "GET":
        try:
            news_id = str(request.GET.get('news_id','').encode('utf-8').strip())
            token = str(request.GET.get('token','').encode('utf-8').strip())
            if not validate_token(token):  # authorization by token
                result['code'] = '0'
                result['message'] = "Unauthorized request"
                result = simplejson.dumps(result)
                return HttpResponse(result, content_type='application/json')

            exist_status = True
            try:
                news.objects.get(news_id=news_id)
            except Exception, e:
                print e
                exist_status = False

            if exist_status:
                delete_status = True
                try:
                    news.objects.filter(news_id=news_id).delete()
                except Exception, e:
                    print e
                    delete_status = False
                if delete_status:
                    result['code'] = '1'
                    result['message'] = "Successfully deleted story."
                else:
                    result['code'] = '0'
                    result['message'] = "Couldn't delete story."
            else:
                result['code'] = '0'
                result['message'] = "Couldn't find story with id='%s'"%news_id
        except:
            result['code'] ='0'
            result['message']="Couldn't delete story."
    result = simplejson.dumps(result)
    return HttpResponse(result, content_type='application/json')


#creates new user, input - username,password1,password2, returns the token if signup is successful,writes to "users" table of database, returns code '1' if successful, '0' if otherwise
def signup(request):
    result = {}
    if request.method == "POST":
        try:
            username = str(request.POST['username'].encode('utf-8'))
            password1 = str(request.POST['password1'].encode('utf-8'))
            password2 = str(request.POST['password2'].encode('utf-8'))

            if username == "" or password1 == "" or password2 == "":
                result['code'] = '0'
                result['message'] = "Username or Password can't be empty"
                result = simplejson.dumps(result)
                return HttpResponse(result, content_type='application/json')

            if password1 != password2:
                result['code'] = '0'
                result['message'] = "Passwords didn't match"
                result = simplejson.dumps(result)
                return HttpResponse(result, content_type='application/json')

            login_status = True
            try:
                users.objects.get(user_name=username)
            except:
                login_status = False

            if not login_status:
                token = generate_token()

                insert_status = True

                try:
                    user = users(
                        user_name=username,
                        password=password1,
                        token=token,
                        token_expire_time = datetime.now()+timedelta(days=7)
                    )
                    user.save()
                except:
                    insert_status = False

                if insert_status:
                    result['code'] = '1'
                    result['message'] = "Successfully created user."
                    result['token'] = token
                else:
                    result['code'] = '0'
                    result['message'] = "Couldn't create user"
            else:
                result['code'] = '0'
                result['message'] = "Username already exists"
        except Exception,e:
            result['code'] ='0'
            result['message']="Couldn't create user."
    result = simplejson.dumps(result)
    return HttpResponse(result, content_type='application/json')


#lets user to log in, input - username,password writes to "users" table of database,it updates the token and token expire date and return the token, returns code '1' if successful, '0' if otherwise
def login(request):
    result = {}
    if request.method == "POST":
        try:
            username = str(request.POST['username'].encode('utf-8'))
            password = str(request.POST['password'].encode('utf-8'))

            if username == "" or password == "":
                result['code'] = '0'
                result['message'] = "Username or Password can't be empty"
                result = simplejson.dumps(result)
                return HttpResponse(result, content_type='application/json')

            login_status = True
            try:
                users.objects.get(user_name=username, password=password)
            except:
                login_status = False

            if login_status:
                token = generate_token()

                update_dict={
                    'token': token,
                    'token_expire_time':datetime.now()+timedelta(days=7)
                }

                update_status = True
                try:
                    users.objects.filter(user_name=username).update(**update_dict)
                except:
                    update_status = False

                if update_status:
                    result['code'] = '1'
                    result['message'] = "Login successful"
                    result['token'] = token
                else:
                    result['code'] = '0'
                    result['message'] = "Incorrect Username/Password"
            else:
                result['code'] = '0'
                result['message'] = "Incorrect Username/Password"
        except:
            result['code'] ='0'
            result['message']="Bad Request"
    result = simplejson.dumps(result)
    return HttpResponse(result, content_type='application/json')


#lets user to log out, input - username,token writes to "users" table of database,it deletes the token and return the token, returns code '1' if successful, '0' if otherwise
def logout(request):
    result = {}
    if request.method == "GET":
        try:
            username = str(request.GET.get('username','').encode('utf-8'))
            token = str(request.GET.get('token','').encode('utf-8'))

            if username == "" or token == "":
                result['code'] = '0'
                result['message'] = "Username or Token can't be empty"
                result = simplejson.dumps(result)
                return HttpResponse(result, content_type='application/json')

            login_status = True
            try:
                users.objects.get(user_name=username)
            except:
                login_status = False

            if login_status:
                update_dict={
                    'token': ''
                }

                update_status = True
                try:
                    users.objects.filter(user_name=username).update(**update_dict)
                except:
                    update_status = False

                if update_status:
                    result['code'] = '1'
                    result['message'] = "Logout successful"
                else:
                    result['code'] = '0'
                    result['message'] = "Couldn't logout"
            else:
                result['code'] = '0'
                result['message'] = "User not logged in"
        except:
            result['code'] ='0'
            result['message']="Bad Request"
    result = simplejson.dumps(result)
    return HttpResponse(result, content_type='application/json')


#UI Related functions

def LoginPage(request):
    return render_to_response('login.html', {}, context_instance=RequestContext(request))

def all_story(request):
    return render_to_response('story.html', {}, context_instance=RequestContext(request))

#gives user search suggestions
def search_suggestions(request):
    if request.is_ajax():
        if request.method == 'GET':
            items_per_page = 10
            has_next_page = False
            requested_page = int(request.GET.get(u'page', ''))
            value = request.GET.get(u'term', '')
            start = items_per_page * (requested_page - 1)
            end = start + items_per_page

            try:
                stories = news.objects.filter(Q(title__contains=value)|Q(author__contains=value)|Q(body__contains=value)).order_by('news_id').reverse()
            except Exception,e:
                print e
                stories = False

            story_data = []
            for story in stories:
                story_data.append([story.news_id, story.title])

            if end < len(story_data):
                has_next_page = True
            story_data = story_data[start:end]
            results = []

            result_dict = {}
            result_dict['id'] = value
            result_dict['text'] = value + ' - ' + 'Text'
            result_dict['type'] = 'Text'
            results.append(result_dict)

            for each_item in story_data:
                result_dict = {}
                result_dict['id'] = each_item[0]
                result_dict['text'] = each_item[1] + ' - News'
                result_dict['type'] = 'News'
                results.append(result_dict)



            Dict = {
                'items': results,
                'more': has_next_page
            }
            result = simplejson.dumps(Dict)
            return HttpResponse(result, content_type='application/json')