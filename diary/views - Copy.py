# Create your views here.
from django.http import HttpResponse
from diary.models import Diary_entry
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from diary.forms import DiaryForm, SecondDiaryForm
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields, models, formsets, widgets



def index(request):
    language = 'en-gb'
    session_language = 'en-gb'
	
    if 'lang' in request.COOKIES:
	 language = request.COOKIES['lang']
	 
    if 'lang' in request.session:
     session_language = request.session['lang']
	
    latest_diary_list = Diary_entry.objects.all().order_by('-entry_date')[:5]
    context = {'latest_diary_list': latest_diary_list, 'full_name' : request.user.username}
    return render(request, 'diary/index.html', context)	
	
	
	
def detail(request, diary_entry_id):
    return HttpResponse("You're looking at poll %s." % diary_entry_id)

def results(request, diary_entry_id):
    return HttpResponse("You're looking at the results of poll %s." % diary_entry_id)

def enter(request, diary_entry_id):
    d = get_object_or_404(Diary_entry, pk=diary_entry_id)
    selected_choice = d.get('1')
    return HttpResponse("You're voting on poll %s." % diary_entry_id)

def create(request):

    #forms = formsets.formset_factory(Diary_entry, can_delete=True)
    if request.POST:
     #the_date = request.POST.get('the_date', 'what')
     the_date = request.POST["the_date"]

     print the_date
     #formset = forms(request.POST)
     x=1
     pform = DiaryForm(request.POST, instance=Diary_entry())
     cforms = SecondDiaryForm(request.POST, prefix=str(x), instance=Diary_entry())
     x=2
     cforms2 = SecondDiaryForm(request.POST, prefix=str(x), instance=Diary_entry())

     if pform.is_valid() and cforms.is_valid():
      obj = pform.save(commit=False)
      obj.user = request.user
      obj.entry_date = the_date
      obj.save()
      obj2 = cforms.save(commit=False)
      obj2.user = request.user
      obj2.entry_date = the_date
      obj2.save()
      obj3 = cforms2.save(commit=False)
      obj3.user = request.user
      obj3.entry_date = the_date
      obj3.save()
#new_poll = pform.save()
#for cf in cforms:
#new_choice = cf.save(commit=False)
#new_choice.poll = new_poll
#new_choice.save()
     return HttpResponseRedirect('/diary/create')
    else:
     pform = DiaryForm(instance=Diary_entry())
     x=1
     cforms = SecondDiaryForm(prefix=str(x), instance=Diary_entry())
     x=2
     cforms2 = SecondDiaryForm(prefix=str(x), instance=Diary_entry())
     return render_to_response('diary/create_diary.html', {'poll_form': pform, 'choice_forms': cforms, 'choice_forms2': cforms2},context_instance = RequestContext(request))
     #if formset.is_valid():
     # entries = formset.save(commit=False)
     # for entry in entries:
     #  entry.user = request.user
     #  entry.save()
     #  return HttpResponseRedirect('/diary')
    #else:
    # args = {}

     #args.update(csrf(request))

     #args['forms'] = forms

    # return render_to_response('diary/create_diary.html', args, context_instance = RequestContext(request))
   # return HttpResponseRedirect('/diary/create')

	
    # form =  DiaryForm(request.POST)
     #form2 = SecondDiaryForm(request.POST)
     #if form.is_valid():
      #obj = form.save(commit=False)
      #obj.user = request.user
      #obj.save()
      #return HttpResponseRedirect('/diary')
#    else:
 #    form = DiaryForm()
  #   form2 = SecondDiaryForm()
#
 #   args = {}
#
  #  args.update(csrf(request))
#
 #   args['form'] = form
  #  args['form2'] = form2
#
 #   return render_to_response('diary/create_diary.html', args, context_instance = RequestContext(request))

def language(request, language='en-gb'):
    response = HttpResponse("setting language to %s" % language)
	
    response.set_cookie('lang', language)
    request.session['lang'] = language
    return response

def login(request):
    c = {}
    #c.update(csrf(request))
    return render_to_response( 'diary/login.html',c,context_instance = RequestContext(request))
	
def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
	
    if user is not None:
     auth.login(request, user)
     return HttpResponseRedirect('/diary/accounts/loggedin')
    else:
     return HttpResponseRedirect('/accounts/invalid')
	 
def loggedin(request):
    return render_to_response('diary/loggedin.html', {'full_name' : request.user.username})

def invalid_login(request):
    return render_to_response('invalid_login.html')
	
def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')

def register_user(request):
    if request.method == 'POST':
     form = UserCreationForm(request.POST)
     if form.is_valid():
      form.save()
      return HttpResponseRedirect('/diary/accounts/register_success')
    args = {}

    args.update(csrf(request))

    args['form'] = UserCreationForm()
    print args
    return render_to_response('diary/register.html', args, context_instance = RequestContext(request))
	
def register_success(request):
    return render_to_response('diary/register_success.html')