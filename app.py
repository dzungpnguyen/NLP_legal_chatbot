from flask import Flask, render_template, jsonify, request
from ml_based_chatbot.MLChatBot import get_response


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    try:
        input = request.json.get("text")
        if input is None:
            return jsonify({"error": "No text in request"}), 400
        response = get_response(input)
        return jsonify({'response': response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
