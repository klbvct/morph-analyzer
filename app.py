from flask import Flask, request, jsonify
from flask_cors import CORS
import pymorphy2

app = Flask(__name__)
CORS(app)

morph = pymorphy2.MorphAnalyzer()

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

        # Берем наиболее вероятный вариант
        best = parsed[0]

        # Лексема = все формы этого слова
        try:
            forms = sorted(set([form.word for form in best.lexeme]))
            results[word] = forms
        except Exception:
            results[word] = ["(не удалось разобрать)"]

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
