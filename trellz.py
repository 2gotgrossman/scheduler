import requests
import json
from datetime import timedelta
from functools import cmp_to_key



key = 'cb74c5bf3faa22a766482259495aeeb4'
token = '858a84edbb439884febcc612ef8b35ac74b755122c1e11000217d9df3dc77532'
#   https://trello.com/1/authorize?response_type=token&key=[[  YOUR KEY HERE ]]&scope=read,write&expiration=never&name=Trello+API+Demo
#
#   Note that you can change the scope, expiration, and name (the name is used to identify who you gave access to at trello.com/your/account )
#   You'll get a token back in your browser when you click allow. Paste that below or in a separate file.

# if you're storing your token in this file, you don't need the following three lines
# if not token:
#   from settings import trello_token
#   token = trello_token

# For example, if I want to get a list of my boards, documented at https://trello.com/docs/api/member/index.html#get-1-members-idmember-or-username-boards,
# I would make a GET request to the following URL

# The base url for every request is the same

now_board_id = "58ba055c236d1b24f3ecdd3a"
tasks_on_the_docket_id = "59b5dc0a16842c9942166841"
current_tasks_list_id = "5a62abada67a82fe63fcae9a"

base = 'https://trello.com/1/'


def get_list_of_cards_from_list(list_id, params = None):
    params_key_and_token = {'key': key, 'token': token}

    if params != None:
        params_key_and_token.update(params)

    list_url = base + "lists/" + list_id + "/cards"
    response = requests.get(list_url, params=params_key_and_token)
    return response.json()

def get_boards():
    params_key_and_token = {'key': key, 'token': token}

    url = base + "members/me/boards"
    response = requests.get(url, params=params_key_and_token)

    return response.json()

def get_list_of_boards(board_id, params = None):
    params_key_and_token = {'key': key, 'token': token}

    if params != None:
        params_key_and_token.update(params)

    board_url = base + "boards/" + board_id + "/lists"
    response = requests.get(board_url, params=params_key_and_token)

    return response.json()

def create_card(list_id, name, labels=None, desc=None):
    card_url = base + "card"
    params_key_and_token = {'key': key, 'token': token}
    params_key_and_token['name'] = name
    params_key_and_token['idList'] = list_id
    if desc:
        params_key_and_token['desc'] = desc

    response = requests.post(card_url, params=params_key_and_token)

    card = Card(response.json()['id'])
    if labels:
        for label in labels:
            response = card.add_label(label)

    return response.json()



class Card():
    def __init__(self, dict_of_attrs):
        self.id = dict_of_attrs['id']
        self.desc = dict_of_attrs['desc']
        self.board = dict_of_attrs['idBoard']
        self.list = dict_of_attrs['idList']
        self.labels = set()
        for label in dict_of_attrs['labels']:
            self.labels.add(label['color'])

        self.name = dict_of_attrs['name']
        self.url = dict_of_attrs['url']
        self.scheduled = False

    # TODO: Rewrite time for completion. Need better way to store / standard
    def time_for_completion(self):
        if self.desc == '':
            return timedelta(hours=.5)
        elif 'h' in self.desc:
            hours = int(''.join([i for i in self.desc if not i.isalpha()]))
            return timedelta(hours=hours)
        elif 'm' in self.desc:
            minutes = int(''.join([i for i in self.desc if not i.isalpha()]))
            return timedelta(minutes=minutes)

    def move_to_list(self, new_board_id):
        move_url = base + "cards/" + self.id + "/idList"
        params_key_and_token = {'key': key, 'token': token, 'value': new_board_id}
        response = requests.put(move_url, params=params_key_and_token)
        return response.json()

    def add_label(self, color):
        label_url = base + "cards/" + self.id + "/labels"
        params_key_and_token = {'key': key, 'token': token, 'value': color}

        response = requests.post(label_url, params=params_key_and_token)
        return response.json()

    def archive_me(self):
        label_url = base + "cards/" + self.id + "/closed"
        params_key_and_token = {'key': key, 'token': token, 'value' : 'true'}

        response = requests.put(label_url, params=params_key_and_token)
        return response.json()

# TODO: Rethink how labels are stored. Right now, labels are used for priority and repeated tasks. Could be extended
# TODO:         to categories
label_map = {
    'green' : 1,
    'yellow' : 2,
    'orange' : 3,
    'red' : 4
}

priority_map = {
    1 : 'green',
    2: 'yellow',
    3: 'orange',
    4: 'red'
}

def get_label_priority(labels):
    max_priority = 0
    for label in labels:
        if label in label_map and label_map[label] > max_priority:
            max_priority = label_map[label]
    return max_priority


def priority_function(a, b):
    a_label_priority = get_label_priority(a.labels)
    b_label_priority = get_label_priority(b.labels)

    return b_label_priority - a_label_priority


# TODO: When adding cards, make sure card is not already in the List
class List():
    def __init__(self, dict_of_cards):
        self.cards = []
        self.dict_of_cards = []
        self.add_cards(dict_of_cards)

    def add_cards(self, dict_of_cards):
        self.dict_of_cards.extend(dict_of_cards)
        for card in dict_of_cards:
            self.cards.append(Card(card))

    def prioritize(self):
        self.cards.sort(key=cmp_to_key(priority_function))
        return self.cards

def get_list_from_id(list_id):
    cards_json = get_list_of_cards_from_list(list_id)
    return List(cards_json)

def json_print(js):
    print(json.dumps(js, sort_keys=True, indent=4, separators=(',', ': ')))
