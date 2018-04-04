from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from mail.models import Letter
from mail.serializers import LetterSerializer
import json
import numpy as np


@csrf_exempt
def letter_list(request):
  """
  List all letters, or create a new letter.
  """
  if request.method == 'GET':
    letters = Letter.objects.all()
    serializer = LetterSerializer(letters, many=True)
    return JsonResponse(serializer.data, safe=False)
      
  elif request.method == 'POST':
    data = JSONParser().parse(request)
    serializer = LetterSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def letter_detail(request, date_from, date_before):
  """
  Retrieve, update or delete a letter.
  """
  try:
    letter = Letter.objects.filter(date_rec__range=[date_from,date_before])
  except Letter.DoesNotExist:
    return HttpResponse(status=404)

  if request.method == 'GET':
    
    
    q_set = letter
    
    nodes = [
             {"id": "Myriel", "group": 1},
             {"id": "Napoleon", "group": 1},
             {"id": "Mlle.Baptistine", "group": 1},
             {"id": "Mme.Hucheloup", "group": 8}
             ]
    links = []
             
    d = dict()
    for q_elem in q_set:
      send_rec = (q_elem.sender, q_elem.receiver)
      if (d.get(send_rec) == None):
        d[send_rec] = [1, False] # [num of occurrencies, flag if this send_rec is already in links array]
      else:
        d[send_rec][0] += 1

    for q_elem in q_set:
      data = {}
      send_rec = (q_elem.sender, q_elem.receiver)
      if d[send_rec][1]:
        continue
      
      data["source"] = q_elem.sender
      data["target"] = q_elem.receiver
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
    serializer = LetterSerializer(letter, data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)

  elif request.method == 'DELETE':
    letter.delete()
    return HttpResponse(status=204)

