#! /usr/bin/env python3

from flask import Flask, request
import os
import urllib
import re
import threading

# ----- Stylesheet and variable -------

tp_dir = '/srv/http/deploy_tp/test/'

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
input[type=submit] {
    

</style>'''

# ----- Fonctions --------

def download_deploy(url_to_get:str, dirname:str):
# launch download and put file into TP dir
    
    global tp_dir

    filename = url_to_get.split('/')[-1]

    location = tp_dir + dirname + '/'

    try:
        os.mkdir(location)
    except FileExistsError:
        pass

    try:
        urllib.request.urlretrieve(url_to_get, location + filename)
    except ValueError:
       return 'Ressource does not exist or isnt accessible'

def check_dir_syntax(dirname:str) -> str:
# Check syntax of submitted directory using regex. second verification after html form
    if not re.match('^[A-Za-z0-9\-\_]*$', dirname):
        print('Character Error')
        os.sys.exit()
    else:
        return True

def check_url(url:str) -> bool:
# Check syntax of submitted url using urlparse. second verification after html form
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

# ----- Script Serveur -------

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def get_info():
    status =''
    if request.method == 'POST':
    # if form was submitted, then check syntax
        if check_dir_syntax(request.form['tp_name']):
            dirname = request .form['tp_name']
        else:
            status = 'Syntaxe de TP invalide'
        if check_url(request.form['url']):
            url = request.form['url']
        else:
            status = '''Syntaxe d'URL invalide'''
        # Threading for download. Enable disconnection from web server without download failling
        thread1 = threading.Thread(target=download_deploy, args=(url, dirname))
        thread1.start()        
        status = 'Téléchargement lancé'
    # return html page containing form, stylesheet and status
    return '''<!DOCTYPE html> 
                <head>
                   '''+style+''' 
                </head>
                <font face='arial'>
                <body>
                <div align=center>
                <h1>'''+status+'''</h1><br>
                    <form method = 'POST'>
                    <h3>Pré-télécharger les logiciels de TP :</h3><br>
                        Nom du TP :<br><input type=text name=tp_name placeholder='Nom du TP'><br>
                        URL : <br><input type=url name=url placeholder='URL du fichier à télécharger' required><br>
                        <input type=submit value=Lancer>
                    </form>
                    <img src='https://www.intechinfo.fr/wp-content/uploads/2019/09/logo-intechinfo-sans-baseline.png'>
                </div>
                </font>
                </body>'''

# launch app
if __name__ == '__main__':
    app.run()
