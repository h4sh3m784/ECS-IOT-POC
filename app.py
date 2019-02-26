from flask import Flask, request
from flask import jsonify

app = Flask(__name__)


#Route
@app.route('/handle', methods=['GET', 'POST'])
def login():

    data = {"status":"null"}

    if request.method == 'POST':
         data = {"status": "POST"}
    else:
         data = {"status": "GET"}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
