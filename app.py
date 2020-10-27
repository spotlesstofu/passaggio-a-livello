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

def get_reaction(wait_time):
    if wait_time == 0:
        return "🙂"
    if 0 < wait_time <= 5:
        return "🙁"
    #if wait_time > 5:
    return "☹️"


@app.route("/")
def get_orari_passaggio():
    orari_passaggio = []
    status = f"{get_reaction(0)} Aperto"
    for stazione_partenza, stazione_arrivo, time_delta in [(terni, marmore, 4), (marmore, terni, 9)]:
        soluzioniViaggio = requests.get(f'{viaggiatreno}/soluzioniViaggioNew/{stazione_partenza}/{stazione_arrivo}/{get_datetime()}').json()
        for s in soluzioniViaggio["soluzioni"]:
            if s["vehicles"][0]["categoriaDescrizione"] == "Regionale":
                orarioPartenza = datetime.datetime.fromisoformat(s["vehicles"][0]["orarioPartenza"])
                # if orarioPartenza - datetime.datetime.now() < datetime.timedelta(minutes=60):
                orarioArrivo = datetime.datetime.fromisoformat(s["vehicles"][0]["orarioArrivo"])
                orario_chiude = orarioPartenza
                orario_apre = orarioArrivo - datetime.timedelta(minutes=time_delta)
                if orario_chiude <= datetime.datetime.now() < orario_apre:
                    eta = int((orario_apre - datetime.datetime.now()).seconds/60)
                    status = f"{get_reaction(eta)} Chiuso - apre tra {eta} minuti"
                orari_passaggio.append((orario_chiude, orario_apre))
    orari_passaggio.sort()
    return render_template("orari.html", items=orari_passaggio, status=status)


if __name__ == "__main__":
    app.run(debug=True)
