from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from mail.models import mails
from mail.models import users
from mail.serializers import mailsSerializer
from datetime import datetime, date
from django.db.models import Max
from django.db.models import Min
from collections import Counter
from mail.utils import request_date_to_datetime

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
    Return text of particular message
    TO-DO: add topics filtration
    """
    if request.GET.get('get_text'):
      req_source = request.GET['source']
      req_target = request.GET['target']
      date,time = request.GET['date'].split(',')
      req_date = request_date_to_datetime(date, time)
      # topic = request.GET['topic']


      filtered_letters = mails.objects.filter(addressfrom=req_source).filter(addressto__contains=req_target).filter(date=req_date)
      if filtered_letters:
        data = [{"text": letter.message} for letter in filtered_letters]
        return JsonResponse(data, safe=False)
      return JsonResponse({"text:": "sasat"}, safe=False)

