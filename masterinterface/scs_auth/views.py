from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.messages.api import get_messages
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from scs import __version__ as version
from masterinterface import settings
from xmlrpclib import ServerProxy
from masterinterface.settings import AUTH_SERVICES
from datetime import datetime, time
from tktauth import createTicket, validateTicket
import binascii


def done(request):
    """ login complete view """
    ctx = {
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend')
    }


    # create ticket
    tokens = ('foo','bar') #to be random generated
    user_data = '%s %s' % (request.user.first_name, request.user.last_name)
    tkt = createTicket(
        settings.SECRET_KEY,
        request.user.username,
        tokens=tokens,
        user_list=user_data
    )

    tkt64 = binascii.b2a_base64(tkt).rstrip()

    response = render_to_response(
        'scs_auth/done.html',
        ctx,
        RequestContext(request)
    )

    response.set_cookie( 'vph-tkt', tkt64 )

    return response


def bt_loginform(request):
    """ return the biomedtown login form """
    if request.method == 'POST' and request.POST.get('username'):
        name = settings('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
        request.session['saved_username'] = request.POST['username']
        backend = request.session[name]['backend']
        return redirect('socialauth_complete', backend=backend)

    return render_to_response('scs_auth/bt_loginform.html',
            {'version': version},
        RequestContext(request)
    )
def bt_login(request):
    """ return the biomedtown login page with and embedded login iframe"""

    return render_to_response('scs_auth/bt_login.html',
            {'version': version},
        RequestContext(request)
    )

def auth_loginform(request):
    """
    """

    service = ServerProxy(AUTH_SERVICES)
    response = {'version': version}

    if request.method == 'POST' and request.POST.get('biomedtown_username') and request.POST.get('biomedtown_password'):
        username=request.POST['biomedtown_username']
        password=request.POST['biomedtown_password']
        service_response = service.rpc_login(username, password)

        if service_response is not False:

            response['ticket']= binascii.a2b_base64(service_response)
            user_data=validateTicket(settings.SECRET_KEY,response['ticket'])
            if user_data:
                user_key =  ['language', 'country', 'postcode', 'fullname', 'nickname', 'email']
                user_value=user_data[3]
                user_dict={}

                for i in range(0, len(user_key)):
                    user_dict[user_key[i]]=user_value[i]


                new_user = RemoteUserBackend()
                user = new_user.authenticate(username)

                user.backend ='django.contrib.auth.backends.RemoteUserBackend'
                user.first_name = user_dict['fullname'].split(" ")[0]
                user.last_name =  user_dict['fullname'].split(" ")[1]
                user.email = user_dict['email']
                user.last_login = str(datetime.now())

                user.save()
                login(request,user)

                response['last_login'] ='biomedtown'

                new_tkt = createTicket(
                    settings.SECRET_KEY,
                    username,
                    user_data=user_value
                )
                tkt64 = binascii.b2a_base64(new_tkt).rstrip()

                response = render_to_response(
                    'scs_auth/done.html',
                    response,
                    RequestContext(request)
                )

                response.set_cookie( 'vph-tkt', tkt64 )

                return response

        else:
            response['info']="Username or password not valid."
    elif request.method == 'POST':
        response['info']="Login error"

    return render_to_response('scs_auth/auth_loginform.html',
        response,
        RequestContext(request)
    )


def auth_done(request,token):
    """ login complete view """
    ctx = {
        'version': version,
        'last_login': "biomedtown"
    }


    response = render_to_response(
        'scs_auth/done.html',
        ctx,
        RequestContext(request)
    )

    return response


def auth_login(request):
    """ return the biomedtown login page with and embedded login iframe"""

    return render_to_response('scs_auth/auth_login.html',
            {'version': version},
        RequestContext(request)
    )

@login_required
def logout(request):
    """Logs out user"""
    auth_logout(request)
    data = {'version': version}
    response = render_to_response(
        'scs/index.html',
        data,
        RequestContext(request)
    )
    response.delete_cookie('vph_cookie')

    return response

def validate_tkt(request):

    if request.GET.get('ticket'):
        ticket= binascii.a2b_base64(request.GET['ticket'])
        user_data=validateTicket(settings.SECRET_KEY,ticket)
        if user_data:
            user_key =  ['language', 'country', 'postcode', 'fullname', 'nickname', 'email']
            user_value=user_data[3]
            user_dict={}

            for i in range(0, len(user_key)):
                user_dict[user_key[i]]=user_value[i]

            user=User.objects.get(username=user_dict['nickname'])

            if user:
                return HttpResponse("VALID")

    return HttpResponse("NOT_VALID")

