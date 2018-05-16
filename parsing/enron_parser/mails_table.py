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
        maxInt = int(maxInt/10)
        decrement = True


def convert_key(key):

    converter = {
        'Date': 'Date',
        'AddressFrom': 'From',
        'AddressTo': 'To',
        'Subject': 'Subject'
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

    else:
        index = cur_string.find('\n' + convert_key(key) + ': ')
        if index == -1:
            return ''
        value_with_trash = cur_string[index + 1 + len(convert_key(key) + ': '):]
        cur_piece = value_with_trash[:value_with_trash.find('\n') + 1]
        value_with_trash = value_with_trash[value_with_trash.find('\n') + 1:]
        while value_with_trash[0] == ' ' or value_with_trash[0] == '\t' or value_with_trash[0] == '\n':
            cur_piece += value_with_trash[:value_with_trash.find('\n') + 1]
            value_with_trash = value_with_trash[value_with_trash.find('\n') + 1:]

        if key == 'Date':
            pdt_index = cur_piece.find('(')
            cur_piece = cur_piece[:pdt_index].strip()

        if key == 'AddressFrom':
            index = cur_piece.find('<')
            if index >= 0:
                if cur_piece[index + 1] == '.':
                    cur_piece = cur_piece[:index - 1] + cur_piece[index + 1:-2]

        if key == 'AddressTo':
            users_to = cur_piece.strip().replace('\n', ' ').replace('\t', ' ').split(',')
            cur_piece = ''
            for user in users_to:
                user = user.strip()
                index = user.find('<')
                if index >= 0:
                    if user[index + 1] == '.':
                        user = user[:index - 1] + user[index + 1:-2]
                cur_piece += user
                cur_piece += ','
            cur_piece = cur_piece[:-1]

        return cur_piece.strip()


def get_string(line):

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


def is_valid_letter(cur_string):
    if (get_info(cur_string, 'AddressTo') == '' or get_info(cur_string, 'AddressFrom') == ''
            or get_info(cur_string, 'Message') == '' or get_info(cur_string, 'AddressFrom').find('@') == -1 or
               get_info(cur_string, 'AddressFrom').find('<') >= 0 or get_info(cur_string, 'AddressFrom').find(' ') >= 0):
        return False

    users_to = get_info(cur_string, 'AddressTo').replace('\n', ' ').replace('\t', ' ').split(',')
    for user in users_to:
        if user.find('@') == -1 or user.find('<') > -1 or user.find(' ') > -1:
            return False
    return True


def create_mails_table(file_name, limit=0):

    useful = ['Id', 'Date', 'AddressFrom', 'AddressTo', 'Subject', 'Message']
    conn = psycopg2.connect("dbname='maildata' user='maildiscovery' host='localhost' port='5432' password='mailpass'")
    print('Connected!')
    cur = conn.cursor()
    drop_statement = 'drop table if exists mails'
    create_statement = 'create table mails (Id integer, Date timestamp, AddressFrom text, AddressTo text, Subject text, Message text)'

    try:
        cur.execute(drop_statement)
        print('Table dropped!')
        cur.execute(create_statement)
        print('Table created!')

        print('Filling started!')
        factor = get_factor(limit)
        file_obj = open(file_name, 'r')
        reader = csv.DictReader(file_obj, delimiter=',')
        num_of_iteration = 0

        cur_max_id = 0
        for line in reader:
            num_of_iteration += 1
            if num_of_iteration * factor > limit:
                break

            # line is an ordered dictionary
            cur_string = get_string(line)
            letter = dict.fromkeys(useful)

            if not is_valid_letter(cur_string):
                continue

            for key in useful:
                if key == 'Id':
                    letter['Id'] = cur_max_id

                else:
                    letter[key] = get_info(cur_string, key)

            columns = letter.keys()
            values = [letter[column] for column in columns]
            insert_statement = 'insert into mails (%s) values %s'
            cur.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
            cur_max_id += 1

        print('Filling finished!')
        file_obj.close()

    finally:
        conn.commit()
        cur.close()
