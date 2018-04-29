from django import forms

class SearchReqForm(forms.Form):
  datefrom = forms.DateTimeField()
  dateto = forms.DateTimeField()
  users = forms.CharField() #need splitting
  topics = forms.CharField() #need splitting
  search = forms.CharField()