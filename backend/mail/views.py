from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from mail.models import mails
from mail.models import users
from mail.serializers import mailsSerializer
import json
import numpy as np
import datetime


@csrf_exempt
def letter_list(request):
  """
  List all letters, or create a new letter.
  """
  if request.method == 'GET':
    letters = mails.objects.all()
    serializer = mailsSerializer(letters, many=True)
    return JsonResponse(serializer.data, safe=False)
      
  elif request.method == 'POST':
    data = JSONParser().parse(request)
    serializer = mailsSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def letter_detail(request, date_from, time_from, date_before, time_before):
  """
  Retrieve, update or delete a letter.
  """
  try:
    ts = time_from.split(':')
    ds = date_from.split('-')
    date_time_from = datetime.datetime(int(ds[0]), int(ds[1]), int(ds[2]), int(ts[0]), int(ts[1]))
    
    ts = time_before.split(':')
    ds = date_before.split('-')
    date_time_before = datetime.datetime(int(ds[0]), int(ds[1]), int(ds[2]), int(ts[0]), int(ts[1]))

    letter = mails.objects.filter(Date__range=[date_time_from,date_time_before])
  except mails.DoesNotExist:
    return HttpResponse(status=404)

  if request.method == 'GET':
    
    
    q_set = letter
    
    nodes = []
    links = []
             
    d = dict()
    s = set()
    for q_elem in q_set:
      send_rec = (q_elem.AddressFrom, q_elem.AddressTo)
      s.add(q_elem.AddressFrom)
      s.add(q_elem.AddressTo)
      if (d.get(send_rec) == None):
        d[send_rec] = [1, False] # [num of occurrencies, flag if this send_rec is already in links array]
      else:
        d[send_rec][0] += 1

    for elem in s:
      data = {}
      data["id"] = elem
      group = users.objects.filter(Address=elem)[0].Department
      data["group"] = group
      nodes.append(data)

    for q_elem in q_set:

      data = {}
      send_rec = (q_elem.AddressFrom, q_elem.AddressTo)
      if d[send_rec][1]:
        continue
      
      data["source"] = q_elem.AddressFrom
      data["target"] = q_elem.AddressTo
      data["value"] = d[send_rec][0]
      links.append(data)
      d[send_rec][1] = True
    
    data = {}
    data["nodes"] = nodes
    data["links"] = links
    return JsonResponse(data)
  
  #    serializer = LetterSerializer(letter, many=True)
  #    return JsonResponse(serializer.data, safe=False)
  
  elif request.method == 'PUT':
    data = JSONParser().parse(request)
    serializer = mailsSerializer(letter, data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)

  elif request.method == 'DELETE':
    letter.delete()
    return HttpResponse(status=204)

