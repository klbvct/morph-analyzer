from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pymorphy2
import os

app = Flask(__name__)
CORS(app)
morph = pymorphy2.MorphAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    words = data.get("words", [])
    results = {}

    for word in words:
        word = word.strip().lower()
        parsed = morph.parse(word)

        if not parsed:
            results[word] = ["(не найдено)"]
            continue

        best = parsed[0]

        try:
            forms = sorted(set([form.word for form in best.lexeme]))
            results[word] = forms
        except Exception:
            results[word] = ["(не удалось разобрать)"]

    return jsonify(results)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
