#!/bin/python3
import argparse, requests, re
from bs4 import BeautifulSoup
from colorama import Fore

print('-'* 84)
print(Fore.LIGHTRED_EX + """
▄▀▀▄ ▄▄   ▄▀▄▄▄▄   ▄▀▀▄▀▀▀▄  ▄▀▀█▄   ▄▀▀▄    ▄▀▀▄  ▄▀▀▀▀▄     ▄▀▀█▄▄▄▄  ▄▀▀▄▀▀▀▄ 
█  █   ▄▀ █ █    ▌ █   █   █ ▐ ▄▀ ▀▄ █   █    ▐  █ █    █     ▐  ▄▀   ▐ █   █   █ 
▐  █▄▄▄█  ▐ █      ▐  █▀▀█▀    █▄▄▄█ ▐  █        █ ▐    █       █▄▄▄▄▄  ▐  █▀▀█▀  
█   █    █       ▄▀    █   ▄▀   █   █   ▄    █      █        █    ▌   ▄▀    █  
▄▀  ▄▀   ▄▀▄▄▄▄▀ █     █   █   ▄▀     ▀▄▀ ▀▄ ▄▀    ▄▀▄▄▄▄▄▄▀ ▄▀▄▄▄▄   █     █   
█   █    █     ▐  ▐     ▐   ▐   ▐            ▀      █         █    ▐   ▐     ▐   
▐   ▐    ▐                                          ▐         ▐                  
\n""" + Fore.LIGHTGREEN_EX)

parser = argparse.ArgumentParser(description='A detector de links and emails in websites, -h for help',usage='./hcrawler.py -d domain -l False -o output.txt -e True -c False -u "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"')
parser.add_argument('-d', '--domain', action='store', dest='hosts', help='domain', required=True)
parser.add_argument('-u', '--user-agent', action='store', dest='agent', help='user-agent', default="Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0")
parser.add_argument('--cookies', action='store', dest='cookie', help='Cookies')
parser.add_argument('--data', action='store', dest='data', help='{password : 123} with asps each element', type=hash)
parser.add_argument('-o', '--output', action='store', dest='output', help='Save files of output')
parser.add_argument('-l', '--links', action='store',dest='links',default='True', help='Mode links')
parser.add_argument('-p', '--phone', dest='phones', help='Phone mode', action = 'store', default='False')
parser.add_argument('-cn', '--cnpj', dest='cnpjs', help='Cnpj mode', action = 'store', default='False')
parser.add_argument('-cp', '--cpf', dest='cpfs', help='Cpf mode', action = 'store', default='False')
parser.add_argument('-e', '--email', dest='emails', help='Mode email', action = 'store', default='False')
parser.add_argument('-c', dest='cont', help='Just crawling the website and not crawling your links', default='True', action='store')
arguments = parser.parse_args()
PHONES= []
EMAILS = []
TO_CRAWL = []
CPFS = []
CNPJS = []
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
        print('-' * 84)
        if arguments.output:
         file.close()
         arq = open(arguments.output, 'r')
         a = arq.read()
         if arguments.emails == "True":
            arqg = get_emails(a)
         if arguments.links == "True":
            arql = filter_links(a)
         if arguments.phones == "True":
            arqp = get_phone(a)
         if arguments.cpfs == "True":
            arqcp = get_cpf(a)
         if arguments.cnpjs == "True":
            arqcn = get_cnpj(a)
         arq.close()
         end = open(arguments.output, 'w')
        
         if arguments.phones == "True":
            end.write('\nPhones:\n\n')
            for phone in arqp:
                end.write(f'{phone}\n')
         if arguments.cpfs == "True":
            end.write('\nCpfs:\n\n')
            for cpf in arqcp:
                end.write(f'{cpf}\n')
         if arguments.cnpjs == "True":
            end.write('\nCnpjs:\n\n')
            for cnpj in arqcn:
                end.write(f'{cnpj}\n')
            
         if arguments.links == "True":
            end.write('\nLinks:\n\n')
            for link in arql:
                end.write(f'{link}\n')
         if arguments.emails == "True":    
            end.write('\nEmails:\n\n')
            for email in arqg:
                end.write(f'{email}\n')
        exit()
    except:
        pass

def get_cnpj(html):
     cnpjs = re.findall(r'\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$', html)
     return cnpjs
def get_cpf(html):
     cpfs = re.findall(r'\d{3}\.\d{3}\.\d{3}\-\d{2}$', html)
     return cpfs
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
    emails = re.findall(r"\w[\w\-\.]+?@\w[\w\-\.]+", html)
    return emails
def filter_links(file):
     links = re.findall(r"https?\:\//[\w\.\-\/\?\=]+", file)
     return links
def get_phone(html):
     phone = re.findall("\+\d+[ ]?\(?\d+\)?[ ]?\d+[-. ]?\d+", html)
     return phone
def crawl():
    if arguments.links == 'True':
                    print('[*] Mode link activated\n')
    if arguments.emails == 'True':
                    print('[*] Mode email activated\n')
    if arguments.cpfs == 'True':
                    print('[*] Mode cpf activated\n')
    if arguments.cnpjs == 'True':
                    print('[*] Mode cnpj activated\n') 

    if arguments.phones == 'True':
                    print('[*] Mode phone activated\n')
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
                if arguments.phones == 'True':
                     
                     phones = get_phone(html)
                     for phone in phones:
                          if phone not in PHONES:
                            print(f'[*] {phone}\n')
                            PHONES.append(phone)
                            if arguments.phones:
                                file.write(f'{phone}\n')
                if arguments.cpfs == 'True':
                     
                     cpfs = get_cpf(html)
                     for cpf in cpfs:
                          if cpf not in CPFS:
                            print(f'[*] {cpf}\n')
                            CPFS.append(cpf)
                            if arguments.cpfs:
                                file.write(f'{cpf}\n')
                if arguments.cnpjs == 'True':
                     
                     cnpjs = get_cnpj(html)
                     for cnpj in cnpjs:
                          if cnpj not in CNPJS:
                            print(f'[*] {cnpj}\n')
                            CNPJS.append(cnpj)
                            if arguments.cnpjs:
                                file.write(f'{cnpj}\n')
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
    if arguments.links == 'True':
                    print('[*] Mode link activated\n')
    if arguments.emails == 'True':
                    print('[*] Mode email activated\n')

    if arguments.phones == 'True':
                    print('[*] Mode phone activated\n')
    if arguments.cpfs == 'True':
                    print('[*] Mode cpf activated\n')
    if arguments.cnpjs == 'True':
                    print('[*] Mode cnpj activated\n')
    if TO_CRAWL:
        url = TO_CRAWL.pop()
        html = request(url)
        if html:
                
                
                if arguments.links == 'True':
                        
                        
                        links = get_links(html)
                        for link in links:
                            if link not in CRAWLED and link not in TO_CRAWL:
                                    TO_CRAWL.append(link)
                                    print(f'[*] {link}\n')
                                    if arguments.output:
                                        file.write(f'{link}\n')
                
                if arguments.emails == 'True':
                    
                    emails = get_emails(html)
                    for email in emails:
                        if email not in EMAILS:
                            print(f'[*] {email}\n')
                            EMAILS.append(email)
                            if arguments.output:
                                file.write(f'{email}\n')
                if arguments.phones == 'True':
                     
                     phones = get_phone(html)
                     for phone in phones:
                          if phone not in PHONES:
                            print(f'[*] {phone}\n')
                            PHONES.append(phone)
                            if arguments.phones:
                                file.write(f'{phone}\n')
                if arguments.cpfs == 'True':
                     
                     cpfs = get_cpf(html)
                     for cpf in cpfs:
                          if cpf not in CPFS:
                            print(f'[*] {cpf}\n')
                            CPFS.append(cpf)
                            if arguments.cpfs:
                                file.write(f'{cpf}\n')
                if arguments.cnpjs == 'True':
                     
                     cnpjs = get_cnpj(html)
                     for cnpj in cnpjs:
                          if cnpj not in CNPJS:
                            print(f'[*] {cnpj}\n')
                            CNPJS.append(cnpj)
                            if arguments.cnpjs:
                                file.write(f'{cnpj}\n')
                CRAWLED.add(url)
                if arguments.output:
                            file.write(f'{url}\n')
                            print('[*] Writing output...\n')
        else:
            CRAWLED.add(url)
            if arguments.output:
                        file.write(f'{url}\n')
                        print('[*] Writing output...\n')
    else:
        print("Done!!!")
        
        
if __name__ == "__main__":
    url = arguments.hosts
    TO_CRAWL.append(url)
    if arguments.cont == 'True':
        crawl()
    else:
        crawlb()
        print('[*] Done!!!\n')
    print(Fore.RESET + '-' * 84)
    if arguments.output:
         file.close()
         arq = open(arguments.output, 'r')
         a = arq.read()
         if arguments.emails == "True":
            arqg = get_emails(a)
         if arguments.links == "True":
            arql = filter_links(a)
         if arguments.phones == "True":
            arqp = get_phone(a)
         if arguments.cpfs == "True":
            arqcp = get_cpf(a)
         if arguments.cnpjs == "True":
            arqcn = get_cnpj(a)
         arq.close()
         end = open(arguments.output, 'w')
        
         if arguments.phones == "True":
            end.write('\nPhones:\n\n')
            for phone in arqp:
                end.write(f'{phone}\n')
         if arguments.cpfs == "True":
            end.write('\nCpfs:\n\n')
            for cpf in arqcp:
                end.write(f'{cpf}\n')
         if arguments.cnpjs == "True":
            end.write('\nCnpjs:\n\n')
            for cnpj in arqcn:
                end.write(f'{cnpj}\n')
            
         if arguments.links == "True":
            end.write('\nLinks:\n\n')
            for link in arql:
                end.write(f'{link}\n')
         if arguments.emails == "True":    
            end.write('\nEmails:\n\n')
            for email in arqg:
                end.write(f'{email}\n')
        
