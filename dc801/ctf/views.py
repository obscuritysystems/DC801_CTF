from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render_to_response
from ctf.forms import *
from ctf.models import *
from datetime import datetime  
import time

def index(request):

    if not request.user.is_authenticated():
        return render_to_response('ctf/index.html', RequestContext(request))
    user_captures = Capture.objects.filter(user=request.user)
    score = len(user_captures)
    return render_to_response('ctf/index.html', RequestContext(request,{'my_captures':user_captures,'score':score}))

def login(request):

    if request.method == 'POST':
        user_name = request.POST['username']
        u_password = request.POST['password']

        user = authenticate(username=user_name, password=u_password)

        if user is not None:
            if user.is_active:
                print "You provided a correct username and password!"
            else:
                print "Your account has been disabled!"
        else:
            print "Your username and password were incorrect."
    else:
        return render_to_response('ctf/login.html',variables)

def score_board(request):
    users_list = Capture.objects.raw('select id,username from auth_user')
    user_scores = []
    for a_user in users_list:
        score = Capture.objects.filter(user__id__exact=a_user.id)
        user_scores.append( {'username': a_user.username , 'score': len(score)})
    #sorted(user_scores,key=lambda scores: scores[1])   
    list = sorted(user_scores,key=lambda k: k['score'])
    return render_to_response('ctf/score_board.html',RequestContext(request,{'user_scores':reversed(list)}))

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
                    message= 'You have already captured flag %s.'
                    variables = RequestContext(request, {'form': form,'capture_msg': message})
                    return render_to_response('ctf/flag_submit.html',variables)
                    #return HttpResponse('flag found %s , yours ' % cap.id)
                else:   
                    
                    cap = Capture(flag=flag_obj,user=request.user,capture_date=datetime.now())
                    cap.save()
                    message = "Flag captured"
                    variables = RequestContext(request, {'form': form,'capture_msg': message})
                    return render_to_response('ctf/flag_submit.html',variables)
                    #return HttpResponse('flag found %s , yours ' % cap.id)
            else:
                message = 'Flag not found'
                variables = RequestContext(request, {'form': form,'capture_msg':message})
                return render_to_response('ctf/flag_submit.html',variables)
                #return HttpResponse('No Flags found')
    else:
        form = FlagSubmitForm()
        variables = RequestContext(request, {'form': form})
        #return render_to_response('registration/register.html', variables)
        return render_to_response('ctf/flag_submit.html',variables)

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

