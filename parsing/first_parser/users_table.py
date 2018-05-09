import json
import psycopg2
from psycopg2.extensions import AsIs

useless = ['attachments', 'headers', 'html', 'messageId', 'priority', 'recievedDate',
           'references', 'replyTo']


def get_data(file_name):

    file = open(file_name, 'r')
    json_file = json.load(file)
    file.close()
    file = json_file
    for key in useless:
        file[0].pop(key, 0)

    users = []
    usernames = set()

    cur_id = 0
    for i in range(len(json_file)):
        cur_user = dict.fromkeys(['Id', 'Address', 'Department'])
        cur_user['Id'] = cur_id
        cur_user['Address'] = file[i]['from'][0]['address'].lower()
        cur_user['Department'] = cur_user['Address'][cur_user['Address'].find('@')+1:]

        if cur_user['Address'] not in usernames:
            usernames.add(cur_user['Address'])
            users.append(cur_user)
            cur_id += 1

    for i in range(len(json_file)):
        cur_user = dict.fromkeys(['Id', 'Address', 'Department'])
        cur_user['Id'] = cur_id
        cur_user['Address'] = file[i]['to'][0]['address'].lower()
        cur_user['Department'] = 'NULL'

        if cur_user['Address'] not in usernames:
            usernames.add(cur_user['Address'])
            users.append(cur_user)
            cur_id += 1

    return users



def fill_table(data):

    conn = psycopg2.connect("dbname='mboxtest' user='maildiscovery' host='localhost' port='5432' password='mailpass'")
    print('Connected!')
    cur = conn.cursor()

    try:
        drop_statement = 'drop table if exists users'
        create_statement = 'create table users (Id integer, Address text, Department text)'
        cur.execute(drop_statement)
        print('Table dropped!')
        cur.execute(create_statement)
        print('Table created!')

        columns = ['Id', 'Address', 'Department']
        insert_statement = 'insert into users (%s) values %s'
        print('Filling started!')
        for i in range(len(data)):
            values = [data[i][key] for key in columns]
            cur.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
        print('Filling finished!')

    finally:
        conn.commit()
        cur.close()


def create_users_table(file_name):
    data = get_data(file_name)
    fill_table(data)
