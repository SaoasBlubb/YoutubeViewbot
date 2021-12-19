import concurrent.futures.thread
import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from fake_headers import Headers

os.system("")


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


print(bcolors.OKGREEN + """
  ____                                    
 |  _ \ _ __ _____  ___   _               
 | |_) | '__/ _ \ \/ / | | |              
 |  __/| | | (_) >  <| |_| |              
 |_|   |_|_ \___/_/\_\\__, |_             
      / ___| |__   ___|___/| | _____ _ __ 
     | |   | '_ \ / _ \/ __| |/ / _ \ '__|
     | |___| | | |  __/ (__|   <  __/ |   
      \____|_| |_|\___|\___|_|\_\___|_|   
                                          
""" + bcolors.ENDC)

print(bcolors.OKCYAN + """
[ Author: Saoas ]
""" + bcolors.ENDC)

'''
Sicherung der zuvor geprueften GuteProxy
'''
try:
    os.remove('ProxyBackup.txt')
except:
    pass

try:
    shutil.copy('GuteProxy.txt', 'ProxyBackup.txt')
    print(bcolors.WARNING + 'GuteProxy gesichert in ProxyBackup' + bcolors.ENDC)
    os.remove('GuteProxy.txt')
except:
    pass

checked = {}


def load_proxy():
    proxies = []

    filename = input(bcolors.OKBLUE +
                     'Geben Sie den Namen Ihrer Proxy-Datei ein: ' + bcolors.ENDC)
    load = open(filename)
    loaded = [items.rstrip().strip() for items in load]
    load.close()

    for lines in loaded:
        if lines.count(':') == 3:
            split = lines.split(':')
            lines = f'{split[2]}:{split[-1]}@{split[0]}:{split[1]}'
        proxies.append(lines)

    return proxies


def mainChecker(proxy_type, proxy, position):

    checked[position] = None

    proxyDict = {
        "http": f"{proxy_type}://{proxy}",
        "https": f"{proxy_type}://{proxy}",
    }

    try:

        header = Headers(
            headers=False
        ).generate()
        agent = header['User-Agent']

        headers = {
            'User-Agent': f'{agent}',
        }

        response = requests.get(
            'https://www.youtube.com/', headers=headers, proxies=proxyDict, timeout=30)
        status = response.status_code

        if status != 200:
            raise Exception

        print(bcolors.OKBLUE + f"Versucht {position+1} |" + bcolors.OKGREEN +
              f' {proxy} | GUT | Typ : {proxy_type} | Reaktion : {status}' + bcolors.ENDC)

        print(proxy, file=open('GoodProxy.txt', 'a'))

    except:
        print(bcolors.OKBLUE + f"Versucht {position+1} |" + bcolors.FAIL +
              f' {proxy} | {proxy_type} |schlecht ' + bcolors.ENDC)
        checked[position] = proxy_type
        pass


def proxyCheck(position):

    proxy = proxy_list[position]

    mainChecker('http', proxy, position)
    if checked[position] == 'http':
        mainChecker('socks4', proxy, position)
    if checked[position] == 'socks4':
        mainChecker('socks5', proxy, position)


def main():
    pool_number = [i for i in range(total_proxies)]

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(proxyCheck, position)
                   for position in pool_number]

        try:
            for future in as_completed(futures):
                future.result()
        except KeyboardInterrupt:
            executor._threads.clear()
            concurrent.futures.thread._threads_queues.clear()
        except IndexError:
            print(bcolors.WARNING + 'Die Anzahl der Proxys ist geringer als die der Threads. Stellen Sie mehr Proxys oder weniger Threads bereit.' + bcolors.ENDC)
            pass


if __name__ == '__main__':
    threads = int(
        input(bcolors.OKBLUE+'Threads (empfohlen = 100): ' + bcolors.ENDC))

    proxy_list = load_proxy()
    proxy_list = list(set(proxy_list))  # removing duplicate proxies
    proxy_list = list(filter(None, proxy_list))  # removing empty proxies

    total_proxies = len(proxy_list)
    print(bcolors.OKCYAN + f'Gesamte Proxies : {total_proxies}' + bcolors.ENDC)

    main()
