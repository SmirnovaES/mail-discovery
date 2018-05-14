import sys
import csv
import psycopg2
from psycopg2.extensions import AsIs

maxInt = sys.maxsize
decrement = True

while decrement:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt / 10)
        decrement = True


def convert_key(key):
    converter = {
        'Address': 'From',
        'Date': 'Date',
        'AddressTo': 'To',
    }
    return converter[key]


def get_info(cur_string, key):
    if key == 'Message':
        cur_string_copy = (cur_string + '.')[:-1]
        cur_field = cur_string[:cur_string.find('\n')]
        while cur_field != '':
            index = cur_string_copy.find('\n')
            cur_field = cur_string_copy[:index]
            cur_string_copy = cur_string_copy[index + 1:]
        return cur_string_copy.strip()

    index = cur_string.find('\n' + convert_key(key) + ': ')
    if index == -1:
        return ''

    value_with_trash = cur_string[index + 1 + len(convert_key(key) + ': '):]
    cur_piece = value_with_trash[:value_with_trash.find('\n') + 1]
    value_with_trash = value_with_trash[value_with_trash.find('\n') + 1:]
    while value_with_trash[0] == ' ' or value_with_trash[0] == '\t' or value_with_trash[0] == '\n':
        cur_piece += value_with_trash[:value_with_trash.find('\n') + 1]
        value_with_trash = value_with_trash[value_with_trash.find('\n') + 1:]

    return cur_piece.strip()


def get_string(line):

    # line is an ordered dictionary
    norm_dict = dict(line)
    cur_string = norm_dict['message']
    if cur_string.find('-----Original Message-----') > -1:
        cur_string = cur_string[:cur_string.find('-----Original Message-----')]
    if cur_string.find('---------------------- Forwarded') > -1:
        cur_string = cur_string[:cur_string.find('---------------------- Forwarded')]
    return cur_string


def get_factor(limit):
    if limit == 0:
        return 0
    else:
        return 1


def first_stage(file_name, users, limit):
    factor = get_factor(limit)
    file_obj = open(file_name, 'r')
    reader = csv.DictReader(file_obj, delimiter=',')
    num_of_iteration = 0

    for line in reader:
        num_of_iteration += 1
        if num_of_iteration * factor > limit:
            break
        cur_string = get_string(line)

        if (get_info(cur_string, 'AddressTo') == '' or get_info(cur_string, 'Address') == ''
                or get_info(cur_string, 'Message') == ''):
            continue

        address = get_info(cur_string, 'Address')
        if address in users.keys():
            continue
        users.setdefault(address)
        id_ = len(users) - 1
        department = address[address.find('@') + 1:]
        users[address] = (id_, department)

    file_obj.close()


def second_stage(file_name, users, limit):
    factor = get_factor(limit)
    file_obj = open(file_name, 'r')
    reader = csv.DictReader(file_obj, delimiter=',')
    num_of_iteration = 0

    for line in reader:
        num_of_iteration += 1
        if num_of_iteration * factor > limit:
            break
        cur_string = get_string(line)

        if (get_info(cur_string, 'AddressTo') == '' or get_info(cur_string, 'Address') == ''
                or get_info(cur_string, 'Message') == ''):
            continue

        addresses = get_info(cur_string, 'AddressTo')
        addresses = addresses.replace('\n', ' ').replace('\t', ' ').split(',')

        for address in addresses:
            address = address.strip()
            if address not in users.keys():
                users.setdefault(address)
                id_ = len(users) - 1
                department = address[address.find('@') + 1:]
                users[address] = (id_, department)

    file_obj.close()


def create_users_table(file_name, limit=0):
    conn = psycopg2.connect("dbname='maildata' user='maildiscovery' host='localhost' port='5432' password='mailpass'")
    print('Connected!')
    print('Preprocessing started!')
    cur = conn.cursor()
    drop_statement = 'drop table if exists users'
    create_statement = 'create table users (Id integer, Address text, Department text)'

    try:
        cur.execute(drop_statement)
        print('Table dropped!')
        cur.execute(create_statement)
        print('Table created!')
        print('Preprocessing finished!')

        print('First stage started!')
        users = dict()
        first_stage(file_name, users, limit)
        print('First stage finished!')

        print('Second stage started!')
        second_stage(file_name, users, limit)
        print('Second stage finished!')

        print('Filling started!')
        columns = ['Id', 'Address', 'Department']
        insert_statement = 'insert into users (%s) values %s'
        for address in users.keys():
            values = [users[address][0], address, users[address][1]]
            cur.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
        print('Filling finished!')

    finally:
        conn.commit()
        cur.close()
