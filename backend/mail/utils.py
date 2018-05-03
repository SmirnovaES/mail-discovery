from datetime import datetime
import psycopg2
from psycopg2.extensions import AsIs
from topicmodeling.lib.baseline.lda import LdaModel
from topicmodeling.output.gettopics import getTopics
from django.db import connection
def request_date_to_datetime(date, time):
    yyyy, mm, dd = date.split('-')
    hours, minutes = time.split(':')
    return datetime(int(yyyy), int(mm), int(dd), int(hours), int(minutes))


def get_data(letters, users):
    nodes = []
    links = []

    num_of_letters = dict()
    curr_users = set()
    for letter in letters:
        addresses_to = letter.addressto.replace('\n', ' ').replace('\t', ' ').replace(',', ' ').split()
        for address in addresses_to:
            send_rec = (letter.addressfrom, address)
            curr_users.add(letter.addressfrom)
            curr_users.add(address)
            if num_of_letters.get(send_rec) is None:
                num_of_letters[send_rec] = [1, False]  # [num of occurrencies, flag if this send_rec is already in links array]
            else:
                num_of_letters[send_rec][0] += 1

    for user in curr_users:
        group = users.objects.filter(address=user)[0].department
        data = {"id": user, "group": group}
        nodes.append(data)

    for letter in letters:
        addresses_to = letter.addressto.replace('\n', ' ').replace('\t', ' ').replace(',', ' ').split()
        for address in addresses_to:
            data = {}

            send_rec = (letter.addressfrom, address)
            if num_of_letters[send_rec][1]:
                continue
            data["source"] = letter.addressfrom
            data["target"] = address
            data["value"] = num_of_letters[send_rec][0]
            links.append(data)
            num_of_letters[send_rec][1] = True

    data = {"nodes": nodes, "links": links}
    return data


def lst2pgarr(alist):
    return '{' + ','.join(str(e) for e in alist) + '}'


def create_topics_table(texts, ids):
    with connection.cursor() as cur:
        cur.execute('drop table if exists topics')
        cur.execute('create table ml_topics (Id integer, Probs decimal[], Topics text[])')
        row = cur.fetchone()
        topics_info = getTopics(source=texts)
        insert_statement = 'insert into ml_topics (%s) values %s'
        topics = [words[0] + ' ' + words[1] + ' ' + words[2] for words in topics_info[0]]
        columns = ['Id', 'Probs', 'Topics']
        for i in range(len(topics_info[1])):
            cur_Id = ids[i]
            cur_probs = topics_info[1][i]
            values = [cur_Id, lst2pgarr(cur_probs), lst2pgarr(topics)]
            cur.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
