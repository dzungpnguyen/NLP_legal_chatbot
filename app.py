from flask import Flask, render_template, jsonify,request
from ml_based_chatbot.MLChatBot import get_response


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['GET'])
def chat():
    input = request.json.get("text")
    if input is None:
        return jsonify({"No text in request"}), 400
    response = get_response(input)
    return jsonify({'response': response}), 200


if __name__ == '__main__':
    app.run(debug=True)
