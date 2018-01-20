import requests
import json
from datetime import datetime, timedelta



key = 'cb74c5bf3faa22a766482259495aeeb4'
token = '016c716b1b341bcc6c8582e9a08402d5a96584b720e6918b58e7f970d7e5a122'
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
calendar_list_id = "5a62abada67a82fe63fcae9a"
backlog_list_id = "59170914545505a2f247ce6c"
base = 'https://trello.com/1/'

boards_url = base + 'members/me/boards'

def get_list_of_cards_from_list(list_id, params = None):
    params_key_and_token = {'key': key, 'token': token}

    if params != None:
        params_key_and_token.update(params)

    list_url = base + "lists/" + list_id + "/cards"
    response = requests.get(list_url, params=params_key_and_token)
    return response.json()


def get_list_of_boards(board_id, params = None):
    params_key_and_token = {'key': key, 'token': token}

    if params != None:
        params_key_and_token.update(params)

    now_url = base + "boards/" + board_id + "/lists"
    response = requests.get(now_url, params=params_key_and_token)

    return response.json()

params_for_cards = {'fields' : ['name', 'closed', 'dateLastActivity', 'desc', 'idLabels', 'url']}

class Card():
    def __init__(self, dict_of_attrs):
        self.id = dict_of_attrs['id']
        self.desc = dict_of_attrs['desc']
        self.board = dict_of_attrs['idBoard']
        self.list = dict_of_attrs['idList']
        self.labels = dict_of_attrs['labels']
        self.name = dict_of_attrs['name']
        self.scheduled = False

    def time_for_completion(self):
        if self.desc == '':
            return timedelta(hours=1)
        elif 'h' in self.desc:
            hours = int(''.join([i for i in self.desc if i.isalpha()]))
            return timedelta(hours=hours)
        elif 'm' in self.desc:
            minutes = int(''.join([i for i in self.desc if i.isalpha()]))
            return timedelta(minutes=minutes)

class List():
    def __init__(self, dict_of_cards):
        self.dict_of_cards = dict_of_cards
        self.cards = []
        for card_dict in dict_of_cards:
            self.cards.append(Card(card_dict))


# l = get_list_of_cards_from_list(backlog_list_id, params_for_cards)
# # l = get_list_of_boards(now_board_id)
# print(l)
# for i in l:
#     print(i)