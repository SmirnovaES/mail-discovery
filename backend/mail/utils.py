from datetime import datetime

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
