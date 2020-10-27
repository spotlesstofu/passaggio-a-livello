#!/usr/bin/env python3

import datetime

import requests
from flask import Flask, render_template

app = Flask(__name__)

terni = 7226
marmore = 7401
viaggiatreno = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno"

def get_datetime():
    return (datetime.datetime.now() - datetime.timedelta(minutes=20)).isoformat().split(".")[0]

def get_orari_passaggio():
    orari_passaggio = []
    for stazione_partenza, stazione_arrivo in [(terni, marmore), (marmore, terni)]:
        soluzioniViaggio = requests.get(f'{viaggiatreno}/soluzioniViaggioNew/{stazione_partenza}/{stazione_arrivo}/{get_datetime()}').json()
        for s in soluzioniViaggio["soluzioni"]:
            if s["vehicles"][0]["categoriaDescrizione"] == "Regionale":
                orarioPartenza = datetime.datetime.fromisoformat(s["vehicles"][0]["orarioPartenza"])
                # if orarioPartenza - datetime.datetime.now() < datetime.timedelta(minutes=60):
                orarioArrivo = datetime.datetime.fromisoformat(s["vehicles"][0]["orarioArrivo"])
                orario_chiude = orarioPartenza
                orario_apre = orarioArrivo
                orari_passaggio.append((orario_chiude, orario_apre))
    orari_passaggio.sort()
    return orari_passaggio


@app.route("/")
def index():
    return render_template("orari.html", items=get_orari_passaggio())


if __name__ == "__main__":
    app.run()
