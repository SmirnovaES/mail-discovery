from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from mail.models import mails
from mail.models import users
from mail.serializers import mailsSerializer
import json
import numpy as np
from datetime import datetime, date
import calendar
import re
from django.db.models import Max
from django.db.models import Min
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
      yyyy, mm, dd = date_from.split('-')
      hours, mins = time_from.split(':')
      date_time_from = datetime(int(yyyy), int(mm), int(dd), int(hours), int(mins))

      date_to,time_to = request.GET['dateTo'].split(',')
      yyyy, mm, dd = date_to.split('-')
      hours, mins = time_to.split(':')
      date_time_to = datetime(int(yyyy), int(mm), int(dd), int(hours), int(mins))
      
      letters_in_date_range = mails.objects.filter(date__range=[date_time_from,date_time_to])

      users_by_dep = {}

      for letter in letters_in_date_range:
        dep = users.objects.filter(address=letter.addressfrom)[0].department
        users_by_dep.setdefault(dep, set({})).add(letter.addressfrom)
        
        adresses_to = letter.addressto.replace('\n',' ').replace('\t', ' ').replace(',', ' ').split()
        for adress_to in adresses_to:
          dep = users.objects.filter(address=adress_to)[0].department
          users_by_dep.setdefault(dep, set({})).add(adress_to)

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
  Return letters containing key words
  TO-DO: add topics filtration, AIS search
  """
  if request.GET.get('search_ais'):
    key_words = request.GET['words'].split(',')

    filtered_letters = mails.objects
    if not key_words:
      filtered_letters = filtered_letters.all().order_by('?')[:5]
    else:
      for word in key_words:
        filtered_letters = filtered_letters.filter(Q(message__iregex=r"^.*[,.!? \t\n]%s[,.!? \t\n].*$" % word) |
                                                   Q(subject__iregex=r"^.*[,.!? \t\n]%s[,.!? \t\n].*$" % word))

    data = [{"source": letter.addressfrom, "target": letter.addressto, "date": letter.date,
             "topic": "NULL", "summary": letter.message[:300]} for letter in filtered_letters]
    return JsonResponse(data, safe=False)


