import sys
import json
import os

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


def create_config():
    print(bcolors.WARNING + 'Ihre Einstellungen werden gespeichert, so dass Sie diese Fragen nicht erneut beantworten muessen.' + bcolors.ENDC)
    print(bcolors.WARNING + 'Druecken Sie einfach die Eingabetaste, um die Standard- oder empfohlenen Werte zu akzeptieren, ohne etwas einzugeben.' + bcolors.ENDC)

    config = {}
    port = 5000
    auth_required = False
    proxy_api = False

    http_api = str(input(
        bcolors.OKBLUE + '\nMoechten Sie eine HTTP-API auf dem lokalen Server aktivieren? (Standard=Ja) [Yes/no] : ' + bcolors.ENDC)).lower()

    if http_api == 'y' or http_api == 'yes' or http_api == '':
        enabled = True
        port = input(bcolors.OKCYAN +
                     '\nGeben Sie einen freien Port ein (Standard=5000) : ' + bcolors.ENDC)
        if port == '':
            port = 5000
        else:
            port = int(port)

    else:
        enabled = False

    config["http_api"] = {
        "enabled": enabled,
        "host": "0.0.0.0",
        "port": port
    }

    database = str(input(
        bcolors.OKBLUE + '\nMoechten Sie Ihre taeglich generierten Ansichten in einer Datenbank speichern? (Standard=Ja) [Yes/no] : ' + bcolors.ENDC)).lower()

    if database == 'y' or database == 'yes' or database == "":
        database = True
    else:
        database = False
    config["database"] = database

    views = int(input(bcolors.WARNING + '\nAnzahl der Views : ' + bcolors.ENDC))
    config["views"] = views

    print(bcolors.WARNING + '\nDie Prozentsaetze fuer die minimale und maximale Betrachtungsdauer haben keinen Einfluss auf Live-Streams.' + bcolors.ENDC)
    print(bcolors.WARNING + 'Beim Live-Streaming spielt das Skript das Video ab, bis der Stream beendet ist.' + bcolors.ENDC)
    
    minimum = input(
        bcolors.WARNING + '\nMinimale ueberwachungsdauer in Prozent (Standard = 85) : ' + bcolors.ENDC)
    if minimum == '':
        minimum = 85.0
    else:
        minimum = float(minimum)
    config["minimum"] = minimum

    maximum = input(
        bcolors.WARNING + '\nMaximale ueberwachungsdauer in Prozent (Standard = 95) : ' + bcolors.ENDC)
    if maximum == '':
        maximum = 95.0
    else:
        maximum = float(maximum)
    config["maximum"] = maximum

    category = input(bcolors.OKCYAN + "\nIn welche Kategorie faellt Ihr Proxy? " +
                     "[F = Kostenlos (ohne user:pass), P = Premium (mit user:pass), R = Rotating Proxy] : " + bcolors.ENDC).lower()

    if category == 'f':
        handle_proxy = str(input(
            bcolors.OKBLUE + '\nYouTube Viewer mit Proxys umgehen lassen? (empfohlen=Nein) [No/yes] : ' + bcolors.ENDC)).lower()

        if handle_proxy == 'y' or handle_proxy == 'yes':
            filename = False
            proxy_type = False

        else:
            filename = input(bcolors.OKCYAN +
                             '\nGeben Sie Ihren Proxy-Dateinamen oder Proxy-API-Link ein : ' + bcolors.ENDC)

            if 'http://' in filename or 'https://' in filename:
                proxy_api = True

            handle_proxy = str(input(
                bcolors.OKBLUE + "\nProxy-Typ auswaehlen [1 = HTTP , 2 = SOCKS4, 3 = SOCKS5, 4 = ALLE] : " + bcolors.ENDC)).lower()

            if handle_proxy == '1':
                proxy_type = 'http'
            elif handle_proxy == '2':
                proxy_type = 'socks4'
            elif handle_proxy == '3':
                proxy_type = 'socks5'
            elif handle_proxy == '4':
                proxy_type = False
            else:
                input(
                    '\nBitte geben Sie 1 fuer HTTP, 2 fuer SOCKS4, 3 fuer SOCKS5 und 4 fuer ALLE Proxy-Typen ein. ')
                sys.exit()

    elif category == 'p' or category == 'r':
        if category == 'r':
            print(bcolors.WARNING + '\nWenn Sie den Proxy-API-Link verwenden, wird das Skript die Proxy-Liste bei jedem Thread-Start abrufen.' + bcolors.ENDC)
            print(bcolors.WARNING + 'Und wird einen Proxy zufaellig aus dieser Liste verwenden, um die Sitzungsverwaltung sicherzustellen.' + bcolors.ENDC)
            filename = input(bcolors.OKCYAN +
                             '\nGeben Sie den Haupt-Gateway oder den Proxy-API-Link Ihres Rotating-Proxy-Dienstes ein : ' + bcolors.ENDC)

            if 'http://' in filename or 'https://' in filename:
                proxy_api = True
                auth_required = input(bcolors.OKCYAN +
                                      '\nBenoetigen Proxys eine Authentifizierung? (Standard=Nein) [No/yes] : ' + bcolors.ENDC).lower()
                if auth_required == 'y' or auth_required == 'yes' or auth_required == "":
                    auth_required = True
                    proxy_type = 'http'
                else:
                    auth_required = False

            else:
                if '@' in filename:
                    auth_required = True
                    proxy_type = 'http'
                elif filename.count(':') == 3:
                    split = filename.split(':')
                    filename = f'{split[2]}:{split[-1]}@{split[0]}:{split[1]}'
                    auth_required = True
                    proxy_type = 'http'
            
            if not auth_required:
                handle_proxy = str(input(
                    bcolors.OKBLUE + "\nProxy-Typ auswaehlen [1 = HTTP , 2 = SOCKS4, 3 = SOCKS5] : " + bcolors.ENDC)).lower()

                if handle_proxy == '1':
                    proxy_type = 'http'
                elif handle_proxy == '2':
                    proxy_type = 'socks4'
                elif handle_proxy == '3':
                    proxy_type = 'socks5'
                else:
                    input(
                        '\nBitte geben Sie 1 fuer HTTP, 2 fuer SOCKS4 und 3 fuer SOCKS5 Proxy-Typ ein ')
                    sys.exit()

        else:
            filename = input(bcolors.OKCYAN +
                             '\nGeben Sie Ihren Proxy-Dateinamen oder Proxy-API-Link ein : ' + bcolors.ENDC)
            auth_required = True
            proxy_type = 'http'
            if 'http://' in filename or 'https://' in filename:
                proxy_api = True
    else:
        input('\nBitte geben Sie F fuer Free, P fuer Premium und R fuer Rotating Proxy ein ')
        sys.exit()

    refresh = 0.0
    if category != 'r':
        print(bcolors.WARNING + '\nAktualisierungsintervall bedeutet, dass das Programm alle X Minuten Proxys aus Ihrer Datei oder API neu laedt.' + bcolors.ENDC)
        print(bcolors.WARNING + 'Sie sollten dies nur dann verwenden, wenn alle X Minuten neue Proxies hinzukommen.' + bcolors.ENDC)
        print(bcolors.WARNING + 'Andernfalls geben Sie einfach 0 als Intervall ein.' + bcolors.ENDC)
        refresh = float(input(
            bcolors.OKCYAN+'\nGeben Sie ein Intervall fuer das Nachladen von Proxys aus der Datei oder API ein (in Minuten). : ' + bcolors.ENDC))

    config["proxy"] = {
        "category": category,
        "proxy_type": proxy_type,
        "filename": filename,
        "authentication": auth_required,
        "proxy_api": proxy_api,
        "refresh": refresh
    }

    gui = str(input(
        bcolors.OKCYAN + '\nMoechten Sie im Headless-Modus (im Hintergrund) arbeiten? (empfohlen=Nein) [No/yes] : ' + bcolors.ENDC)).lower()

    if gui == 'y' or gui == 'yes':
        background = True
    else:
        background = False

    bandwidth = str(input(
        bcolors.OKBLUE + '\nDie Videoqualitaet reduzieren, um Bandbreite zu sparen? (empfohlen=Nein) [No/yes] : ' + bcolors.ENDC)).lower()

    if bandwidth == 'y' or bandwidth == 'yes':
        bandwidth = True
    else:
        bandwidth = False

    playback_speed = input(
        bcolors.OKBLUE + '\nWaehlen Sie die Wiedergabegeschwindigkeit [1 = Normal(1x), 2 = Langsam(zufaellig .25x, .5x, .75x), 3 = Schnell(zufaellig 1.25x, 1.5x, 1.75x)] (Voreinstellung = 1) : ' + bcolors.ENDC)
    if playback_speed == "":
        playback_speed = 1
    else:
        playback_speed = int(playback_speed)

    print(bcolors.WARNING +
          '\nDas Skript aktualisiert die Anzahl der Threads dynamisch, wenn der Proxy neu geladen wird.' + bcolors.ENDC)
    print(bcolors.WARNING + 'Wenn Sie immer die gleiche Anzahl von Threads verwenden moechten, geben Sie bei Maximum und Minimum Threads die gleiche Anzahl ein.' + bcolors.ENDC)
    max_threads = input(
        bcolors.OKCYAN + '\nMaximum Threads [Anzahl der zu verwendenden Chrome-Treiber] (empfohlen = 5): ' + bcolors.ENDC)
    if max_threads == '':
        max_threads = 5
    else:
        max_threads = int(max_threads)

    min_threads = input(
        bcolors.OKCYAN + '\nMinimum Threads [Anzahl der zu verwendenden Chrome-Treiber] (empfohlen = 2): ' + bcolors.ENDC)
    if min_threads == '':
        min_threads = 2
    else:
        min_threads = int(min_threads)

    config["background"] = background
    config["bandwidth"] = bandwidth
    config["playback_speed"] = playback_speed
    config["max_threads"] = max_threads
    config["min_threads"] = min_threads

    json_object = json.dumps(config, indent=4)

    with open("config.json", "w") as outfile:
        outfile.write(json_object)

    print(bcolors.OKGREEN + '\nIhre Einstellungen werden in config.json gespeichert. Sie koennen jederzeit eine neue Konfigurationsdatei aus youtube_viewer.py erstellen' + bcolors.ENDC)
    print(bcolors.OKGREEN + 'Oder durch Ausfuehren von `python config.py` ' + bcolors.ENDC)


if __name__ == '__main__':
    create_config()
