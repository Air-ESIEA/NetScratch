#! /usr/bin/env python3

from flask import Flask, redirect, request
import os
import urllib
import re
import threading

# ----- Stylesheet -------

style = '''
<style type="text/css">
body {
    background-color: DimGrey;
}
input {
	max-width: 500px;
	padding: 10px 20px;
	background: #f4f7f8;
	margin: 10px auto;
	padding: 20px;
	background: #f4f7f8;
	border-radius: 8px;
	font-family: 'Arial';
}

</style>'''

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
    return '''<!DOCTYPE html>
                <head>
                   '''+style+''' 
                </head>
                <font face='arial'>
                <body>
                <div align=center>
                    <form method = 'POST'>
                    <h1>Pré-télécharger les logiciels de TP :</h1><br>
                        Nom du TP :<br><input type=text name=tp_name placeholder='Nom du TP'><br>
                        URL : <br><input type=url name=url placeholder='URL du fichier à télécharger' required><br>
                        <input type=submit value=Lancer>
                    </form>
                    <img src='https://www.intechinfo.fr/wp-content/uploads/2019/09/logo-intechinfo-sans-baseline.png'>
                </div>
                </font>
                </body>'''

#@app.route
if __name__ == '__main__':
    app.run()

