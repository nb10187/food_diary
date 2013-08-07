from django.contrib import admin
from diary.models import Food_type
#from diary.models import Food_feedback
from diary.models import User
from diary.models import Diary_entry


admin.site.register(Food_type)
#admin.site.register(Food_feedback)
admin.site.unregister(User) 
admin.site.register(Diary_entry)