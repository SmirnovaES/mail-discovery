import json
import re
import psycopg2
from psycopg2.extensions import AsIs
import dateutil

useful = ['id', 'from', 'to', 'date', 'subject', 'message']
useless = ['attachments', 'headers', 'html', 'messageId', 'priority', 'recievedDate',
           'references', 'replyTo']


def get_data(file_name):

    file = open(file_name, 'r')
    json_file = json.load(file)
    file.close()
    file = json_file
    for key in useless:
        file[0].pop(key, 0)

    letters = list()
    for i in range(len(json_file)):
        cur_letter = dict.fromkeys(useful)
        cur_letter['id'] = i
        cur_letter['from'] = file[i]['from'][0]['address']
        cur_letter['to'] = file[i]['to'][0]['address']
        cur_letter['date'] = file[i]['date']
        cur_letter['subject'] = file[i]['subject']

        if 'text' in file[i].keys():
            cur_letter['message'] = file[i]['text']
        else:
            # delete html tags
            cleanr = re.compile('<.*?>')
            cur_letter['message'] = re.sub(cleanr, '', file[i]['html'])

        letters.append(cur_letter)

    return letters


def convert_key(key):
    converter = {
        'id': 'Id',
        'from': 'AddressFrom',
        'to': 'AddressTo',
        'date': 'Date',
        'subject': 'Subject',
        'message': 'Message'
    }
    return converter[key]



def fill_table(data):

    conn = psycopg2.connect("dbname='mboxtest' user='maildiscovery' host='localhost' port='5432' password='mailpass'")
    print('Connected!')
    cur = conn.cursor()

    try:
        drop_statement = 'drop table if exists mails'
        create_statement = 'create table mails (Id integer, Date timestamp, AddressFrom text, AddressTo text, Subject text, Message text)'
        cur.execute(drop_statement)
        print('Table dropped!')
        cur.execute(create_statement)
        print('Table created!')

        columns = ['Id', 'AddressFrom', 'AddressTo', 'Date', 'Subject', 'Message']
        insert_statement = 'insert into mails (%s) values %s'
        print('Filling started!')
        for i in range(len(data)):
            #data[i]['Date'] = dateutil.parser.parse(data[i]['Date'])
            values = [data[i][key] for key in data[0].keys()]
            cur.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
        print('Filling finished!')

    finally:
        conn.commit()
        cur.close()



def create_mails_table(file_name):
    data = get_data(file_name)
    fill_table(data)

