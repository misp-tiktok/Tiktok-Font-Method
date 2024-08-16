from flask import Flask, request, jsonify
from run import change_username  # Assuming your logic for changing username is in run.py

app = Flask(__name__)

@app.route('/change_username', methods=['POST'])
def change_username_route():
    data = request.json
    session_id = data.get('session_id')
    device_id = data.get('device_id')
    iid = data.get('iid')
    last_username = data.get('last_username')
    new_username = data.get('new_username')

    if not all([session_id, device_id, iid, last_username, new_username]):
        return jsonify({'error': 'Missing parameters'}), 400

    result = change_username(session_id, device_id, iid, last_username, new_username)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
