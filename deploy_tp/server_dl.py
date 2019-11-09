#! /usr/bin/env python3

from flask import Flask, redirect, request
import os
import urllib
import re
import threading

# ----- Fonctions --------

def download_deploy(url_to_get:str, dirname:str):
    filename = url_to_get.split('/')[-1]

    location = 'test/' + dirname + '/'

    try:
        os.mkdir(location)

        print('OK')
    except FileExistsError:
        print('not OK')

    try:
        urllib.request.urlretrieve( url_to_get, location + filename)
    except ValueError:
       return 'Ressource does not exist or isnt accessible'

def check_dir_syntax(dirname:str) -> str:
    if not re.match('^[a-z0-9\-\_]*$', dirname):
        print('Character Error')
        os.sys.exit()
    else:
        return True

def check_url(url:str) -> bool:
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

# ----- Script Serveur -------

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def get_info():
    if request.method == 'POST':
        if check_dir_syntax(request.form['tp_name']):
            dirname = request .form['tp_name']
        else:
            return 'Syntaxe de TP invalide'
        if check_url(request.form['url']):
            url = request.form['url']
        else:
            return '''Syntaxe d'URL invalide'''
        thread1 = threading.Thread(target=download_deploy, args=(url, dirname))
        thread1.start()        
        return 'Telechargement lancer'
    return '''<form method = 'POST'>
                <input type=text name=tp_name placeholder='Nom du TP'><br>
                <input type=text name=url placeholder='URL du fichier à télécharger'><br>
                <input type=submit value=Lancer>'''

#@app.route
if __name__ == '__main__':
    app.run()

