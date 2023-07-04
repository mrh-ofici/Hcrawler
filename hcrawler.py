#!/bin/python3
import argparse, requests, re
from bs4 import BeautifulSoup
from colorama import Fore

print('-'* 65)
print(Fore.LIGHTRED_EX + """
        ▄▀▀▄ ▄▄   ▄▀▄▄▄▄   ▄▀▀▄▀▀▀▄  ▄▀▀█▄   ▄▀▀▄    ▄▀▀▄  ▄▀▀▀▀▄     ▄▀▀█▄▄▄▄  ▄▀▀▄▀▀▀▄ 
        █  █   ▄▀ █ █    ▌ █   █   █ ▐ ▄▀ ▀▄ █   █    ▐  █ █    █     ▐  ▄▀   ▐ █   █   █ 
        ▐  █▄▄▄█  ▐ █      ▐  █▀▀█▀    █▄▄▄█ ▐  █        █ ▐    █       █▄▄▄▄▄  ▐  █▀▀█▀  
        █   █    █       ▄▀    █   ▄▀   █   █   ▄    █      █        █    ▌   ▄▀    █  
        ▄▀  ▄▀   ▄▀▄▄▄▄▀ █     █   █   ▄▀     ▀▄▀ ▀▄ ▄▀    ▄▀▄▄▄▄▄▄▀ ▄▀▄▄▄▄   █     █   
        █   █    █     ▐  ▐     ▐   ▐   ▐            ▀      █         █    ▐   ▐     ▐   
        ▐   ▐    ▐                                          ▐         ▐                  
\n""" + Fore.LIGHTGREEN_EX)

parser = argparse.ArgumentParser(description='A detector de links and emails in websites', usage='./hcrawler.py -d domain -l False -o output.txt -e True -c False -u "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"')
parser.add_argument('-d', '--domain', action='store', dest='hosts', help='domain', required=True)
parser.add_argument('-u', '--user-agent', action='store', dest='agent', help='user-agent', default="Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0")
parser.add_argument('--cookies', action='store', dest='cookie', help='Cookies')
parser.add_argument('--data', action='store', dest='data', help='{password : 123} with asps each element', type=hash)
parser.add_argument('-o', '--output', action='store', dest='output', help='Save files of output')
parser.add_argument('-l', '--links', action='store',dest='links',default='True', help='Mode links')
parser.add_argument('-e', '--email', dest='emails', help='Mode email', action = 'store', default='False')
parser.add_argument('-c', dest='cont', help='Just crawling the website and not crawling your links', default='True', action='store')
arguments = parser.parse_args()

EMAILS = []
TO_CRAWL = []
CRAWLED = set()
if arguments.output:
    print('[*] Mode output activated\n')
    file = open(arguments.output, 'w')

def request(url):
    header = {"User-Agent": arguments.agent}
    try:
        if arguments.cookie:
                header['Cookie'] = arguments.cookie
        if arguments.data:
            data = arguments.data
            response = requests.get(url, headers=header, data=data)
        
        else:
            response = requests.get(url, headers=header)
        return response.text
    except KeyboardInterrupt:
        print('-' * 65)
        exit()
    except:
        pass


def get_links(html):
    links = []
    try:
        soup = BeautifulSoup(html, "html.parser")
        tags_a = soup.find_all("a", href=True)
        for tag in tags_a:
            link = tag["href"]
            if link.startswith("http"):
                links.append(link)

        return links
    except:
        pass

def get_emails(html):
    emails = re.findall(r"\w[\w\.]+@\w[\w\.]+\w", html)
    return emails
def filter_links(file):
     links = re.findall(r"\w+://\w+[\w\./]+", file)
     return links
def crawl():
    if arguments.links == 'True':
                    print('[*] Mode link activated\n')
    if arguments.emails == 'True':
                    print('[*] Mode email activated\n')
    while 1:
        if TO_CRAWL:
            url = TO_CRAWL.pop()

            html = request(url)
            if html:
                if arguments.links == 'True':
                    links = get_links(html)
                    if links:
                        for link in links:
                            if link not in CRAWLED and link not in TO_CRAWL:
                                TO_CRAWL.append(link)

                    print(f"[*] Crawling {url}\n")
                
                if arguments.emails == 'True':
                    emails = get_emails(html)
                    for email in emails:
                        if email not in EMAILS:
                            print(f'[*] {email}')
                            EMAILS.append(email)
                CRAWLED.add(url)
                if arguments.output:
                    file.write(f'{url}\n')
            else:
                CRAWLED.add(url)
                if arguments.output:
                    file.write(f'{url}\n')
        else:
            print("Done!!!\n")
            break

def crawlb():
    html = request(url)
    if html:
        if arguments.links == 'True':
                print('[*] Mode link activated\n')
                links = get_links(html)
                for link in links:
                     print(f'[*] {link}\n')
                     if arguments.output:
                        file.write(f'{link}\n')
        
        if arguments.emails == 'True':
            print('[*] Mode email activated\n')
            emails = get_emails(html)
            for email in emails:
                if email not in EMAILS:
                    print(f'[*] {email}\n')
                    if arguments.output:
                        file.write(f'{email}\n')
        if arguments.output:
                    file.write(f'{url}\n')
                    print('[*] Writing output...\n')
    else:
        if arguments.output:
                    file.write(f'{url}\n')
                    print('[*] Writing output...\n')
if __name__ == "__main__":
    url = arguments.hosts
    TO_CRAWL.append(url)
    if arguments.cont == 'True':
        crawl()
    else:
        crawlb()
        print('[*] Done!!!\n')
    print(Fore.RESET + '-' * 65)
    if arguments.output:
         file.close()
         arq = open(arguments.output, 'r')
         a = arq.read()
         
         arqg = get_emails(a)
         arql = filter_links(a)
         
         arq.close()
         end = open(arguments.output, 'w')
        
         
         end.write('Links:\n\n')
         for link in arql:
            end.write(f'{link}\n')
         end.write('\nEmails:\n\n')
         for email in arqg:
            end.write(f'{email}\n')
        
