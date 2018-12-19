import requests
import misc
import json
import time
import bs4
from bs4 import BeautifulSoup
import telegram

token = misc.token
# https://api.telegram.org/bot638177707:AAFES2oGTeMc1h_9B8mn1Qw3kVB3xoByx1c/getUpdates

baseUrl = "https://api.telegram.org/bot"+token+"/"
messages = 4


def get_updates():
    url = baseUrl + 'getUpdates'
    r = requests.get(url)
    return r.json()


def get_messages():
    data = get_updates()

    chat_id = data['result'][-1]['message']['chat']['id']
    messages_text = data['result'][-1]['message']['text']

    message_info = {
        'chat_id': chat_id,
        'text': messages_text
    }
    return message_info


def send_message(chat_id, text = 'Wait a second'):
    url = baseUrl + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.post(url)


def write_updates():
    updates_getter = get_updates
    with open('updates.json', 'w') as file:
        json.dump(updates_getter, file, indent=2, ensure_ascii=False)


def updates_checker():
    data = get_updates()
    length = len(data['result'])
    global messages

    if length != messages:
        messages = length
        return True
    return False


# ----------------------------------------BeautifulSoup----------------------------------------------------------------


def get_html(name):
    if " " in name:
        name = name.replace(" ", "+")

    base_url = "http://flibusta.is/booksearch?ask="
    request = base_url + name
    r = requests.get(request)
    return r.text


# def get_book(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     links = list()
#
#     try:
#         ul = soup.find('div', id="main").findAll("ul")[-1]
#
#         for li in ul:
#             for a in li:
#                 # links.append(a['href'])
#                 if type(a) is bs4.element.Tag:
#                     links.append(a['href'])
#
#     except IndexError:
#         try:
#             ul = soup.find('div', id="main").findAll("ul")[-2]
#             print(ul)
#             for li in ul:
#                 for a in li:
#                     # links.append(a['href'])
#                     if type(a) is bs4.element.Tag:
#                         links.append(a['href'])
#         except IndexError:
#             links = list()
#
#     print(links)
#
#     return links


def get_book(html):
    soup = BeautifulSoup(html, 'html.parser')
    






def separate(one_book):
    booksLinks = list()

    for i in one_book:
        if "b" in i:
            booksLinks.append(i)

    return booksLinks


def get_concrete_book(chat_message):
    URL = "http://flibusta.is"

    list_of = list()
    books = separate(get_book(get_html(chat_message)))
    counter = 0

    for i in books:

        url = URL + i
        r = requests.get(url)
        text = r.text
        soup = BeautifulSoup(text, 'html.parser')

        book_name = soup.find('h1', class_="title").findAll(text=True)

        author_block = soup.find("div", id="main").findAll("a")[34].findAll(text=True)

        links = "\n" + url+"/epub\n"+url+"/mobi\n"+url+"/fb2\n"

        if len(list_of) == 5:
            break
        new_str = str(book_name[0]) + " " + str(author_block[0]) + links
        list_of.append(new_str)
    return list_of


def main():
    get_book(get_html("хроники"))
    # while True:
    #     print("whiling")
    #     if updates_checker():
    #         chat_message = get_messages()['text']
    #         print('entered the state' + chat_message)
    #         chat_id = get_messages()['chat_id']
    #         concrete = get_concrete_book(chat_message)
    #
    #         result_string = "Вот что мне удалось разыскать по вашему запросу \"{}\":\n".format(chat_message)
    #
    #         if len(concrete) != 0:
    #             for i in concrete:
    #                 result_string += i + "\n"
    #                 print(i + " this is ш")
    #         else:
    #             result_string = " ничего не удалось найти :( "
    #
    #         send_message(chat_id, result_string)
    #
    #     time.sleep(0.5)


if __name__ == '__main__':
    main()
