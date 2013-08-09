# Create your views here.
from django.http import HttpResponse
from diary.models import Diary_entry, feedback
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from diary.forms import DiaryForm, SecondDiaryForm, ThirdDiaryForm, FourthDiaryForm
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields, models, formsets, widgets
from django.db import connection, transaction
from django.views import generic





def index(request):
    return HttpResponseRedirect('/foody/accounts/login/')	
	
	
	
def detail(request, diary_entry_id):
    s1='AND d.user_id = %s ' % request.user.id
    s2=' AND d.id = %s' % diary_entry_id
    s3='SELECT d.id, d.entry_date,( f.per_kg_emmision * d.serving_size ) AS total,d.meal_type, f.food_type_name,d.additional_info, d.serving_size, f.per_kg_emmision FROM diary_diary_entry d, diary_food_type f WHERE d.food_type_id = f.id %s ' % s1
    s3 = s3 +s2
    the_request = Diary_entry.objects.raw(s3)
    #the_request = 'test'

    return render_to_response('diary/viewDetail.html',{'full_name' : request.user.username , 'the_request':the_request } ,context_instance = RequestContext(request))

def results(request, diary_entry_id):
    return HttpResponse("You're looking at the results of poll %s." % diary_entry_id)

def enter(request, diary_entry_id):
    d = get_object_or_404(Diary_entry, pk=diary_entry_id)
    selected_choice = d.get('1')
    return HttpResponse("You're voting on poll %s." % diary_entry_id)

def create(request):

    if request.POST:
      the_date = request.POST["the_date2"]
      the_meal = request.POST["3-meal_type"]
      cforms3 = ThirdDiaryForm(request.POST, request.FILES)

      if cforms3.is_valid():
       obj3 = cforms3.save(commit=False)
       if 'image' in request.FILES:
        obj3.image = request.FILES['image']
       if 'additional_info' in request.POST:
        obj3.additional_info = request.POST['additional_info']  		
       obj3.user = request.user
       obj3.meal_type = the_meal 
       obj3.entry_date = the_date
       obj3.save()
 
       return HttpResponseRedirect('/foody/create', {'full_name' : request.user.username})
       
      else:
        the_error = 'There was a problem with your diary entry details, please re-enter details'
        return HttpResponseRedirect('/foody/create', {'full_name' : request.user.username, 'the_error':the_error})
    else:
     
     cforms3 = FourthDiaryForm(instance=Diary_entry())
     random_feed = feedback.objects.order_by('?')[1]	 
     q1 = Diary_entry.objects.all().order_by('-entry_date')
     latest_diary_list = q1.filter(user=request.user)[:15]
     recent_three = Diary_entry.objects.raw('SELECT d.id, d.entry_date,( f.per_kg_emmision * d.serving_size ) AS total,d.meal_type, f.food_type_name, (d.serving_size*1000) AS serving_size , f.per_kg_emmision FROM diary_diary_entry d, diary_food_type f WHERE d.food_type_id = f.id AND d.user_id = %s  ORDER BY  d.id DESC LIMIT 0 , 3' , [ request.user.id] )
     recent_feedback = Diary_entry.objects.raw('SELECT DISTINCT d.id, f.feedback  FROM diary_diary_entry d, diary_food_type f WHERE d.food_type_id = f.id AND d.user_id = %s GROUP BY d.food_type_id ORDER BY  d.id DESC LIMIT 0 , 10' , [ request.user.id] )
     all_user_diary_list = Diary_entry.objects.raw('SELECT DISTINCT u.id AS id, u.username, AVG( f.per_kg_emmision * d.serving_size ) AS avg, SUM( f.per_kg_emmision * d.serving_size ) AS total FROM diary_diary_entry d, diary_food_type f, auth_user u WHERE d.food_type_id = f.id AND d.user_id = u.id GROUP BY d.user_id ORDER BY avg ASC LIMIT 0 , 5')
     date_diary_list = Diary_entry.objects.raw('SELECT DISTINCT d.id, d.entry_date, SUM( f.per_kg_emmision * d.serving_size ) AS total FROM diary_diary_entry d, diary_food_type f WHERE d.food_type_id = f.id AND d.user_id = %s GROUP BY d.entry_date ORDER BY  d.entry_date LIMIT 0 , 10' , [ request.user.id] )
     top_emmisions = Diary_entry.objects.raw('SELECT DISTINCT * FROM diary_diary_entry d, diary_food_type f WHERE d.food_type_id = f.id and d.user_id = %s GROUP BY f.food_type_name ORDER BY f.per_kg_emmision DESC LIMIT 0 , 5' , [ request.user.id] )
     cursor = connection.cursor()
     cursor.execute('SELECT SUM( f.per_kg_emmision ) AS total FROM diary_diary_entry d, diary_food_type f WHERE d.food_type_id = f.id AND d.user_id = %s', request.user.id)
     row = cursor.fetchone()
     image_list = Diary_entry.objects.raw('SELECT id, image FROM diary_diary_entry WHERE image <>  "" AND user_id = %s LIMIT 0 , 20' , [ request.user.id] )


     return render_to_response('diary/create_diary.html', {'all_user_diary_list':all_user_diary_list,'recent_feedback':recent_feedback,'recent_three':recent_three, 'date_diary_list':date_diary_list,'choice_forms3': cforms3, 'latest_diary_list': latest_diary_list, 'full_name' : request.user.username, 'top_emmisions':top_emmisions, 'row': row, 'image_list':image_list, 'random_feed':random_feed},context_instance = RequestContext(request))


def language(request, language='en-gb'):
    response = HttpResponse("setting language to %s" % language)
	
    response.set_cookie('lang', language)
    request.session['lang'] = language
    return response

#def login(request):
 #   c = {}
    #c.update(csrf(request))
 #   return render_to_response( 'diary/login.html',c,context_instance = RequestContext(request))
	
def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
	
    if user is not None:
     auth.login(request, user)
     return HttpResponseRedirect('/foody/create')
    else:
     return HttpResponseRedirect('/foody/accounts/invalid')
	 
def loggedin(request):
    return render_to_response('diary/loggedin.html', {'full_name' : request.user.username})

def invalid_login(request):
    return HttpResponse("You Login is INVALID, please Go back and re-try")
	
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/foody/accounts/login/')

def login(request):
    if request.method == 'POST':
     form = UserCreationForm(request.POST)
     if form.is_valid():
      form.save()
      return HttpResponseRedirect('/foody/accounts/register_success')
    args = {}

    args.update(csrf(request))

    args['form'] = UserCreationForm()
    print args
    return render_to_response('diary/login.html', args, context_instance = RequestContext(request))
	
def gallery(request):
#
    image_list = Diary_entry.objects.raw('SELECT id, image FROM diary_diary_entry WHERE image <>  "" AND user_id = %s LIMIT 0 , 20' , [ request.user.id] )
    return render_to_response('diary/gallery.html',{'full_name' : request.user.username, 'image_list':image_list } ,context_instance = RequestContext(request))
	
def history(request):
#
    q1 = Diary_entry.objects.all().order_by('-entry_date')
    full_list = q1.filter(user=request.user)
    #full_list = Diary_entry.objects.raw('SELECT id, image FROM diary_diary_entry WHERE image <>  "" AND user_id = %s LIMIT 0 , 20' , [ request.user.id] )
    return render_to_response('diary/history.html',{'full_name' : request.user.username, 'full_list':full_list } ,context_instance = RequestContext(request))
	
class DetailView(generic.DetailView):
    model = Diary_entry
    template_name = 'foody/deatil.html'
	
def register_success(request):
    return render_to_response('foody/register_success.html')
