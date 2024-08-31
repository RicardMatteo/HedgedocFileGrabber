#!/usr/bin/env python3


import json
import os
import pprint
import sqlite3 as db
import sys
from pathlib import Path

import requests

FIREFOX_DIR = Path(os.path.expanduser('~'), '.mozilla', 'firefox')
SESSION_COOKIES_TXT = 'cookies.txt'
COOKIE_NAME = "connect.sid="
CONTENTS = "value"

HOST : str = "sanik.inpt.fr"

def get_cookie_db_path(firefox_dir):
    for e in os.listdir(firefox_dir):
        if e.endswith('.default-release'):
            p = Path(firefox_dir, e, 'cookies.sqlite')
            if not p.is_file():
                print("Error: the file '{0}' doesn't exist".format(str(p)), file=sys.stderr)
                sys.exit(1)
            else:
                return str(p)
    # else
    print("Error: the user dir. was not found in '{0}'".format(firefox_dir), file=sys.stderr)
    sys.exit(1)


def extract_cookies(host):
    """
    Extract cookies from cookies.sqlite.
    """
    cookie_db = get_cookie_db_path(str(FIREFOX_DIR))
    print("# working with", cookie_db)

    conn = db.connect(cookie_db)
    cursor = conn.cursor()

    sql = "SELECT {c} FROM moz_cookies WHERE host LIKE '%{h}%' AND name = 'connect.sid'".format(c=CONTENTS, h=host)
    cursor.execute(sql)

    cnt = 0
    for row in cursor.fetchall():
        s = row[0];
        cnt += 1

    print("Search term: {0}".format(host))
    print("Exported: {0}".format(cnt))

    conn.close()

    print(s);
    return s;

def download_document(hedge_doc_base_url, document_id, cookie, destination_directory, filename):
    url = f"{hedge_doc_base_url}/{document_id}/download"
    try:
        headers = {'Cookie': cookie}
        response = requests.get(url, headers=headers)
        # response = requests.get(hedge_doc_base_url + "/me", headers=headers)
        if response.status_code == 200:
            os.makedirs(destination_directory, exist_ok=True)  # Assurez-vous que le répertoire de destination existe
    
            with open(os.path.join(destination_directory, f"{filename}.md"), "w", encoding="utf-8") as file:
                file.write(response.text)
        else:
            raise Exception("Échec de la récupération du document Markdown.")
    except Exception as e:
        print(e)


def extract_path_and_filename(filepath):
    # Séparation du chemin et du nom de fichier
    path, filename = os.path.split(filepath)
    # Si le chemin est vide, cela signifie qu'il n'y a pas de répertoire parent
    if not path:
        return "", filename
    # Si le chemin n'est pas vide, nous retirons le dernier séparateur de chemin
    path = path.rstrip(os.path.sep)
    return path, filename


#############################################################################

if __name__ == "__main__":
    try:
        # Récupération du cookie de session
        # On commence par lire le fichier cookies.txt
        with open(SESSION_COOKIES_TXT, "r") as cookies_file:
            cookie = "connect.sid=" + cookies_file.read()   
            # cookie = COOKIE_NAME +extract_cookies(HOST)
             
    except Exception as e:
        # Si le fichier n'existe pas, on tente de récupérer le cookie depuis le navigateur
        try: 
            # cookie = "connect.sid=" + cookies_file.read()   
            cookie = COOKIE_NAME +extract_cookies(HOST)
        except Exception as e:
            print(e)
            # Si le cookie n'a pas pu être récupéré, on utilise un cookie par défaut (hardcodé)
            print("Impossible de récupérer le cookie de session. Utilisation d'un cookie par défaut.")
            exit(1)
    hedge_doc_base_url = f"https://{HOST}"
    
    with open("config.txt", "r") as file:
        for line in file:
            document_id, filepath = line.strip().split(", ")  # Séparation de l'ID du document et du chemin
            path, filename = extract_path_and_filename(filepath)
            os.makedirs(path, exist_ok=True)  # Assurez-vous que le répertoire de destination existe
            # Téléchargement du contenu de la note
            result = download_document(hedge_doc_base_url, document_id, cookie, path, filename)  

