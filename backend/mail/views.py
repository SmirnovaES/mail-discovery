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


@csrf_exempt
def letter_list(request):
  """
  List all letters, or create a new letter.
  """
  # if request.method == 'GET':
  #   letters = mails.objects.all()
  #   serializer = mailsSerializer(letters, many=True)
  #   return JsonResponse(serializer.data, safe=False)


# @csrf_exempt
# def letter_detail(request, date_from, time_from, date_before, time_before):
#   """
#   Retrieve, update or delete a letter.
#   """
#   try:
#     ts = time_from.split(':')
#     ds = date_from.split('-')
#     date_time_from = datetime(int(ds[0]), int(ds[1]), int(ds[2]), int(ts[0]), int(ts[1]))
    
#     ts = time_before.split(':')
#     ds = date_before.split('-')
#     date_time_before = datetime(int(ds[0]), int(ds[1]), int(ds[2]), int(ts[0]), int(ts[1]))

#     letter = mails.objects.filter(date__range=[date_time_from,date_time_before])
    
# # everything works without it:
# #    dtf_gm = calendar.timegm(date_time_from.timetuple())
# #    dtf = datetime.utcfromtimestamp(dtf_gm)
# #    dtb_gm = calendar.timegm(date_time_before.timetuple())
# #    dtb = datetime.utcfromtimestamp(dtb_gm)
# #    letter = mails.objects.filter(date__range=[dtf,dtb])

#   except mails.DoesNotExist:
#     return HttpResponse(status=404)

#   if request.method == 'GET':
    
#     q_set = letter
    
#     nodes = []
#     links = []
             
#     d = dict()
#     s = set()
#     for q_elem in q_set:
#       adr_to = q_elem.addressto.replace('\n',' ').replace('\t', ' ').replace(',', ' ').split()
#       for adr in adr_to:      
#         send_rec = (q_elem.addressfrom, adr)
#         s.add(q_elem.addressfrom)
#         s.add(adr)
#         if (d.get(send_rec) == None):
#           d[send_rec] = [1, False] # [num of occurrencies, flag if this send_rec is already in links array]
#         else:
#           d[send_rec][0] += 1

#     for elem in s:
#       data = {}
#       data["id"] = elem
#       if len(users.objects.filter(address=elem)) != 0: #сломается запрос фронта, если пользователя нет в базе (todo)
#         group = users.objects.filter(address=elem)[0].department
#         data["group"] = group
#         nodes.append(data)

#     for q_elem in q_set:

#       adr_to = q_elem.addressto.replace('\n',' ').replace('\t', ' ').replace(',', ' ').split()
#       for adr in adr_to:      
#         data = {}
	
#         send_rec = (q_elem.addressfrom, adr)
#         if d[send_rec][1]:
#           continue
#         data["source"] = q_elem.addressfrom
#         data["target"] = adr
#         data["value"] = d[send_rec][0]
#         links.append(data)
#         d[send_rec][1] = True
    
#     data = {}
#     data["nodes"] = nodes
#     data["links"] = links
#     return JsonResponse(data)

# @csrf_exempt
# def get_departments_for_time_period(request, date_from, time_from, date_before, time_before):
#   """
#   Return users from every department for the time period.
#   """
#   if request.method == 'GET':

#     ts = time_from.split(':')
#     ds = date_from.split('-')
#     date_time_from = datetime(int(ds[0]), int(ds[1]), int(ds[2]), int(ts[0]), int(ts[1]))

#     ts = time_before.split(':')
#     ds = date_before.split('-')
#     date_time_before = datetime(int(ds[0]), int(ds[1]), int(ds[2]), int(ts[0]), int(ts[1]))
    
#     letter = mails.objects.filter(date__range=[date_time_from,date_time_before])

#     return JsonResponse(date_time_before, safe=False)

@csrf_exempt
def letters_process(request):
  if request.method == 'GET':
    
    """
    Return date of the first and the last letters in database.
    """
    if request.GET.get('get_date'):
      first_letter_date = mails.objects.all().aggregate(Max('date'))["date__max"]  # 2044-01-04T14:48:58
      last_letter_date = mails.objects.all().aggregate(Min('date'))["date__min"]
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


