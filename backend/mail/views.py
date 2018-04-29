from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from mail.models import mails
from mail.models import users
from mail.serializers import mailsSerializer
from mail.forms import SearchReqForm
from mail.utils import request_date_to_datetime, get_data
import json
from django.db.models import Max
from django.db.models import Min
from django.db.models import Q
from collections import Counter


@csrf_exempt
def letters_process(request):
  if request.method == 'GET':
    
    """
    Return date of the first and the last letters in database.
    """
    if request.GET.get('get_date'):
      first_letter_date = mails.objects.all().aggregate(Min('date'))["date__min"]  # 2044-01-04T14:48:58
      last_letter_date = mails.objects.all().aggregate(Max('date'))["date__max"]
      first_letter_date = ','.join(str(first_letter_date).split(' '))  # "2044-01-04,14:48:58"
      last_letter_date = ','.join(str(last_letter_date).split(' '))
      first_letter_date = ':'.join(first_letter_date.split(':')[:-1])  # "2044-01-04,14:48"
      last_letter_date = ':'.join(last_letter_date.split(':')[:-1])
      response_list = [first_letter_date, last_letter_date]
      return JsonResponse(response_list, safe=False)

    """
    Return users from every department for the time period.
    """
    if request.GET.get('get_departments'):
      date_from,time_from = request.GET['dateFrom'].split(',')
      date_time_from = request_date_to_datetime(date_from, time_from)

      date_to,time_to = request.GET['dateTo'].split(',')
      date_time_to = request_date_to_datetime(date_to, time_to)
      
      letters_in_date_range = mails.objects.filter(date__range=[date_time_from,date_time_to])

      users_by_dep = {}

      for letter in letters_in_date_range:
        dep = users.objects.filter(address=letter.addressfrom)[0].department
        users_by_dep.setdefault(dep, set({})).add(letter.addressfrom)
        
        addresses_to = letter.addressto.replace('\n',' ').replace('\t', ' ').replace(',', ' ').split()
        for address_to in addresses_to:
          dep = users.objects.filter(address=address_to)[0].department
          users_by_dep.setdefault(dep, set({})).add(address_to)

      return_list = []
      for dep, emails in users_by_dep.items():
        tmp_dict = {}
        tmp_dict['group'] = dep
        tmp_dict['users'] = [{'id' : email} for email in emails]
        return_list.append(tmp_dict)

      return JsonResponse(return_list, safe=False)

    """
    Return top 5 users who have letters more than anyone else.
    """
    if request.GET.get('get_personal_top'):
      all_users = []
      all_users += mails.objects.values_list('addressfrom', flat=True)
      all_users += mails.objects.values_list('addressto', flat=True)  # contains sublists with addr_to
      all_users = [item for sublist in all_users for item in sublist.replace('\n',' ').replace('\t', ' ').replace(',', ' ').split()]
      top_users_info = Counter(all_users).most_common(5)
      ret_list = [{'value' : user_info[1], 'label' : user_info[0]} for user_info in top_users_info]
      return JsonResponse(ret_list, safe=False)

  """
  Return letters filtered by given data.
  TO-DO: add topics filtering
  """
  if request.method == 'POST':
    form = SearchReqForm(request.POST)
    if form.is_valid():
      date_to, time_to = form.cleaned_data['dateto'].split(',')
      date_from, time_from = form.cleaned_data['datefrom'].split(',')
      users = form.cleaned_data['users'].split(',')
      searchline = form.cleaned_data['search']

      date_time_from = request_date_to_datetime(date_from, time_from)
      date_time_to = request_date_to_datetime(date_to, time_to)

      filtered_letters = mails.objects.filter(date__range=[date_time_from, date_time_to]).filter(
        Q(addressto__in=users) | Q(addressfrom__in=users)).filter(
        Q(message__contains=searchline) | Q(subject__contains=searchline))

      return JsonResponse(get_data(filtered_letters, users))
