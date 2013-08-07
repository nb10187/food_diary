from django import forms
from diary.models import Diary_entry
from django.forms import fields, models, formsets, widgets


class DiaryForm(forms.ModelForm) :

	class Meta:
		model = Diary_entry
        #exclude = ('user',)
		fields = ('food_type','serving_size')
		

#DiaryFormset = formsets.formset_factory(DiaryForm)

		
class SecondDiaryForm(forms.ModelForm) :

	class Meta:
		model = Diary_entry
#       #exclude = ('user',)
		fields = ('food_type','serving_size',)

class ThirdDiaryForm(forms.ModelForm) :

	class Meta:
		model = Diary_entry
#       #exclude = ('user',)
		fields = ('food_type','serving_size',)

class FourthDiaryForm(forms.ModelForm) :

	class Meta:
		model = Diary_entry
#       #exclude = ('user',)
		fields = ('food_type','serving_size')
