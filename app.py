# app.py

from flask import Flask, render_template, request, jsonify
from minha_lista import lista_sem_acentos
from collections import defaultdict

app = Flask(__name__)

alfabeto = list("abcdefghijklmnopqrstuvwxyz")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_words', methods=['POST'])
def get_words():
    data = request.get_json()
    letras_input = data.get('letters', '').lower()
    obr = data.get('required', '').lower()

    if len(letras_input) != 7 or len(obr) != 1:
        return jsonify({"error": "You must enter exactly 7 letters and 1 required letter."}), 400

    letras = list(letras_input)
    letras_prb = alfabeto.copy()

    for letra in letras:
        if letra in letras_prb:
            letras_prb.remove(letra)

    lista2 = [p for p in lista_sem_acentos if len(p) >= 4 and obr in p]

    def sem_letra(palavra):
        for letra in letras_prb:
            if letra in palavra:
                return False
        return True

    nova_lista = list(filter(sem_letra, lista2))

    # Group by word length
    grouped = defaultdict(list)
    for word in nova_lista:
        grouped[len(word)].append(word)

    # Sort the output: convert to dict with sorted keys and sorted words
    sorted_grouped = {
        str(length): sorted(words)
        for length, words in sorted(grouped.items())
    }

    return jsonify({"grouped_words": sorted_grouped})

if __name__ == '__main__':
    app.run(debug=True)
