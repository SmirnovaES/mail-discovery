from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from mail.models import mails
from mail.models import users
from mail.models import ml_topics
from mail.serializers import mailsSerializer
from mail.forms import SearchReqForm
from mail.utils import request_date_to_datetime, get_data, create_topics_table
import json
from django.db.models import Max
from django.db.models import Min
from django.db.models import Q
from collections import Counter

import nltk
from topicmodeling.lib.baseline.lda import LdaModel
from topicmodeling.output.gettopics import getTopics

latest_letters = mails.objects.all()

@csrf_exempt
def letters_process(request):
  global latest_letters
  if request.method == 'GET':
    
    """
    Return date of the first and the last letters in database.
    """
    if request.GET.get('get_date'):
      first_letter_date = mails.objects.all().aggregate(Min('date'))["date__min"]  # 2044-01-04T14:48:58
      last_letter_date = mails.objects.all().aggregate(Max('date'))["date__max"]
      
      # if first letter's year is less then 1991, change it to 1991
      if str(first_letter_date).split('-')[0] < '1991':
        fixed_first_letter_date = str(first_letter_date).split('-')
        fixed_first_letter_date[0] = '1991'
        first_letter_date = '-'.join(fixed_first_letter_date)
      
      # if last letter's year is greater then 2018, change it to 2018
      if str(last_letter_date).split('-')[0] > '2018':
        fixed_last_letter_date = str(last_letter_date).split('-')
        fixed_last_letter_date[0] = '2018'
        last_letter_date = '-'.join(fixed_last_letter_date)
      
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
        tmp_dict['users'] = [{'id' : email} for email in list(emails)[:100]]
        return_list.append(tmp_dict)

      return JsonResponse(return_list, safe=False)

    """
    Return top 5 users who have letters more than anyone else in a given period of time.
    """
    if request.GET.get('get_personal_top'):
      
      date_from,time_from = request.GET['dateFrom'].split(',')
      date_time_from = request_date_to_datetime(date_from, time_from)
      
      date_to,time_to = request.GET['dateTo'].split(',')
      date_time_to = request_date_to_datetime(date_to, time_to)
      
      all_users = []
      
      all_users += mails.objects.filter(date__range=[date_time_from,date_time_to]).values_list('addressfrom', flat=True)

      all_users += mails.objects.filter(date__range=[date_time_from,date_time_to]).values_list('addressto', flat=True)  # contains sublists with addr_to
      all_users = [item for sublist in all_users for item in sublist.replace('\n',' ').replace('\t', ' ').replace(',', ' ').split()]  # flat 2D list into 1D
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


    if request.GET.get('get_topics'):
      nltk.download('punkt')
      nltk.download('wordnet')
      texts = [letter.message for letter in latest_letters.all()]
      ids = [letter.id for letter in latest_letters.all()]
      if len(texts) > 100:
        texts = texts[:100]
        ids = ids[:100]
      ml_topics.objects.all().delete()
      print('table cleared, num of texts is %d' % len(texts))
      topics_info = getTopics(source=texts)
      topics = [words[0] + ' ' + words[1] + ' ' + words[2] for words in topics_info[0]]
      for i in range(len(topics_info[1])):
        print(i)
        curr_Id = ids[i]
        curr_probs = topics_info[1][i]
        values = [curr_Id, curr_probs, topics]
        new_val = ml_topics(id=curr_Id, probs='{' + ','.join(str(e) for e in curr_probs) + '}', topics='{' + ','.join(str(e) for e in topics) + '}')
        new_val.save()

      topics = ml_topics.objects.get(pk=ids[0]).topics
      return JsonResponse(topics, safe=False)

  """
  Return letters filtered by given data.
  TO-DO: add topics filtering
  """
  if request.method == 'POST':
    form = SearchReqForm(request.POST)
    if form.is_valid():
      date_to, time_to = form.cleaned_data['dateto'].split(',')
      date_from, time_from = form.cleaned_data['datefrom'].split(',')
      users_all = form.cleaned_data['users'].split(',')
      searchline = form.cleaned_data['search']
      date_time_from = request_date_to_datetime(date_from, time_from)
      date_time_to = request_date_to_datetime(date_to, time_to)


      filtered_letters = mails.objects.filter(date__range=[date_time_from, date_time_to]).filter(
        Q(addressto__in=users_all) | Q(addressfrom__in=users_all)).filter(
        Q(message__contains=searchline) | Q(subject__contains=searchline))

      latest_letters = filtered_letters
      return JsonResponse(get_data(filtered_letters, users))
