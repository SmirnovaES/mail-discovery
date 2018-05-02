from django import forms

class SearchReqForm(forms.Form):
  datefrom = forms.CharField()
  dateto = forms.CharField()
  users = forms.CharField() #need splitting
  topics = forms.CharField() #need splitting
  search = forms.CharField()
