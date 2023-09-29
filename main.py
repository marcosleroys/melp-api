from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/test', methods=['GET'])
def api():
    data = {
        data: 'test'
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)