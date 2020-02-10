# -*- encode utf-8 -*-

import os
import sys
import requests
# from bs4 import BeautifulSoup as BS
import random 
from time import sleep

# @see: https://developers.whatismybrowser.com/useragents/explore
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "Opera/9.80 (Linux armv7l) Presto/2.12.407 Version/12.51 , D50u-D1-UHD/V1.5.16-UHD (Vizio, D50u-D1, Wireless)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36 OPR/52.0.2871.99",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/74.0.3729.157 Safari/537.36",
    "Wget/1.12 (linux-gnu)"    
]

def get_books_by_bruteforce(i):
    # @see https://www.gutenberg.org/files/
    url = "https://www.gutenberg.org/files/{}{}"
    headers = {'User-agent': random.choice(user_agents)}

    try:
        # @see: https://www.gutenberg.org/files/
        file_ascii = url.format(i, "/{}.txt".format(i))
        file_iso = url.format(i, "/{}-0.txt".format(i))
        file_utf8 = url.format(i, "/{}-8.txt".format(i))

        # espera algo entre 10~50 ms
        ms = random.uniform(0.01, 0.05)
        print(headers['User-agent'])
        print("Esperando {}ms".format(round(ms, 3)*1000))
        sleep(ms)
        response = requests.get(file_ascii, headers=headers)
        if response.status_code == 404:
            print("{} - {}".format(response.status_code, file_ascii))
        elif response.status_code == 200:
            print("{} - {} ({} bytes)".format(response.status_code, file_ascii, response.headers['Content-length']))
            return {'content': response.text, 'file_name': file_ascii}

        # espera algo entre 10~50 ms
        ms = random.uniform(0.01, 0.05)
        print(headers['User-agent'])
        print("Esperando {}ms".format(round(ms, 3)*1000))
        sleep(ms)
        response = requests.get(file_iso, headers=headers)
        if response.status_code == 404:
            print("{} - {}".format(response.status_code, file_iso))
        elif response.status_code == 200:
            print("{} - {} ({} bytes)".format(response.status_code, file_iso, response.headers['Content-length']))
            return {'content': response.text, 'file_name': file_iso}
        
        # espera algo entre 5~25 ms
        ms = random.uniform(0.005, 0.025)
        print(headers['User-agent'])
        print("Esperando {}ms".format(round(ms, 3) * 1000))
        sleep(ms)
        response = requests.get(file_utf8, headers=headers)
        if response.status_code == 404:
            print("{} - {}".format(response.status_code, file_utf8))
        elif response.status_code == 200:
            print("{} - {} ({} bytes)".format(response.status_code, file_utf8, response.headers['Content-length']))
            return {'content': response.text, 'file_name': file_utf8}

    except requests.exceptions.RequestException as e:
        print("ERRO! - {}".format(e))
        sys.exit(1)
    
    print("** Nada encontrado **")
    print("   [{}]".format(file_ascii))
    return None
    # raise Exception("Nada encontrado")


# def get_links_from_robot(pages=1):
#     # @see https://www.gutenberg.org/wiki/Gutenberg:Information_About_Robot_Access_to_our_Pages
#     url = "https://gutenberg.org/robot/harvest?filetypes[]=txt"

#     try:
#         # print("Buscando {}".format(url))
#         response = requests.get(url)
#         html = response.text
#         # print("Interpretando HTML")
#         soup = BS(html, features="html.parser")
#         zip_list = open("zip_list.txt", "w")
#         for link in soup.find_all("a", href=True):
#             # print(link['href'])
#             zip_list.write("{}\n".format(link['href']))
#     except requests.exceptions.RequestException as e:
#         print("ERRO! - {}".format(e))
#         sys.exit(1)

repo = os.path.dirname(os.path.realpath(__file__))
repo = os.path.join(repo, 'downloads')

book_content = None
for i in range(3999, 5000):
    book = get_books_by_bruteforce(i)
    if book == None:
        continue

    book_file = os.path.join(repo, os.path.basename(book['file_name']))

    print("Escrevendo o arquivo em disco {}".format(book_file))
    filew = open(book_file, "w")
    filew.write(book['content'])
    filew.close()
    print("-" * 10)
