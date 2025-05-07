from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__, static_folder='templates')


def carica_parole_csv(file_path):
    df = pd.read_csv(file_path)
    parole = dict(zip(df['parola'].str.lower(), df['punteggio']))  
    return parole

def calcola_punteggio(titolo, parole):
    punteggio_totale = 0
    parole_titolo = titolo.lower().split() #divide e minuscolo

    for parola in parole_titolo:
        if parola in parole:
            punteggio_totale += parole[parola]

    return punteggio_totale

def calcola_punteggio_percentuale(titolo, parole):
    punteggio_totale = 0
    parole_titolo = titolo.lower().split()
    totale_parole = len(parole_titolo)

    for parola in parole_titolo:
        if parola in parole:
            punteggio_totale += parole[parola]

    if totale_parole > 0:
        return (punteggio_totale / totale_parole) * 100
    return 0

def classificazione(punteggio):
    if punteggio > 0:
        return "Fonte attendibile"
    elif punteggio < 0:
        return "Fake news"
    else:
        return "Indeterminato"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        titolo = request.form['titolo']  
        parole = carica_parole_csv("parole.csv")  
        punteggio_percentuale = calcola_punteggio_percentuale(titolo, parole)
        classe = classificazione(punteggio_percentuale)
        return render_template('index.html', titolo=titolo, punteggio=round(punteggio_percentuale, 2), classe=classe)
    return render_template('index.html', titolo=None, punteggio=None, classe=None)

if __name__ == '__main__':
    app.run(debug=True)
