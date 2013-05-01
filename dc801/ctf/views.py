from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render_to_response
from ctf.forms import *
from django.template import Context, loader
from ctf.models import *
from datetime import datetime  
import time

def index(request):
  return render_to_response('ctf/index.html', RequestContext(request))



def flag_submit(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')

    if request.method == 'POST':
        form = FlagSubmitForm(request.POST)

        if form.is_valid():
            temp_flag = form.cleaned_data['flag'].strip()
            flag_result = Flag.objects.filter(flag__exact=temp_flag)
            if len(flag_result) > 0 :

                flag_obj = flag_result[0]
                capture_result = Capture.objects.filter(flag=flag_obj).filter(user=request.user)

                if len(capture_result) > 0:
                    return HttpResponse('you have already captured this flag')
                else:   
                    cap = Capture(flag=flag_obj,user=request.user,capture_date=datetime.now())
                    cap.save()
                    return HttpResponse('flag found %s , yours ' % cap.id)
            else:
                return HttpResponse('No Flags found')
    else:
        form = FlagSubmitForm()
        variables = RequestContext(request, {'form': form})
        #return render_to_response('registration/register.html', variables)
        return render_to_response('ctf/flag_submit.html',variables)

'''
def user_page(request, username):
  try:
    user = User.objects.get(username=username)
  except:
    raise Http404('Requested user not found.')

  bookmarks = user.bookmark_set.all()

  variables = RequestContext(request, {
    'username': username,
    'bookmarks': bookmarks
 })
  return render_to_response('user_page.html', variables)
'''

def register_success(request):
  return render_to_response('registration/register_success.html', RequestContext(request))

def logout_page(request):
  logout(request)
  return HttpResponseRedirect('/')


def register_page(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      user = User.objects.create_user(
        username=form.cleaned_data['username'],
        password=form.cleaned_data['password1'],
        email=form.cleaned_data['email']
      )
      return HttpResponseRedirect('/register/success/')
  else:
    form = RegistrationForm()

  variables = RequestContext(request, {
    'form': form
  })
  return render_to_response('registration/register.html', variables)

