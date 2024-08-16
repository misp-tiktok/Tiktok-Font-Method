from flask import Flask, request, jsonify, render_template
from hashlib import md5
import random
import time
import requests
from copy import deepcopy

app = Flask(__name__)

class XG:
    def __init__(self, debug):
        self.length = 0x14
        self.debug = debug
        self.hex_CE0 = [0x05, 0x00, 0x50, random.choice(range(0, 0xFF)), 0x47, 0x1e, 0x00, random.choice(range(0, 0xFF)) & 0xf0]

    def addr_BA8(self):
        tmp = None
        hex_BA8 = list(range(0x100))
        for i in range(0x100):
            A = tmp if tmp else hex_BA8[i - 1] if i > 0 else 0
            B = self.hex_CE0[i % 0x8]
            if A == 0x05 and i != 1 and tmp != 0x05:
                A = 0
            C = A + i + B
            C %= 0x100
            tmp = C if C < i else None
            D = hex_BA8[C]
            hex_BA8[i] = D
        return hex_BA8

    def initial(self, debug, hex_BA8):
        tmp_add = []
        tmp_hex = deepcopy(hex_BA8)
        for i in range(self.length):
            A = debug[i]
            B = tmp_add[-1] if tmp_add else 0
            C = hex_BA8[i + 1] + B
            C %= 0x100
            tmp_add.append(C)
            D = tmp_hex[C]
            tmp_hex[i + 1] = D
            E = D + D
            E %= 0x100
            F = tmp_hex[E]
            debug[i] = A ^ F
        return debug

    def calculate(self, debug):
        for i in range(self.length):
            A = debug[i]
            B = reverse(A)
            C = debug[(i + 1) % self.length]
            D = B ^ C
            E = RBIT(D)
            F = E ^ self.length
            G = ~F & 0xFF
            debug[i] = G
        return debug

    def main(self):
        result = ''.join(hex_string(item) for item in self.calculate(self.initial(self.debug, self.addr_BA8())))
        return f'8404{hex_string(self.hex_CE0[7])}{hex_string(self.hex_CE0[3])}{hex_string(self.hex_CE0[1])}{hex_string(self.hex_CE0[6])}{result}'

def hex_string(num):
    return f'{num:02x}'

def RBIT(num):
    return int(f'{num:08b}'[::-1], 2)

def reverse(num):
    tmp_string = f'{num:02x}'
    return int(tmp_string[1] + tmp_string[0], 16)

def run(param="", stub="", cookie=""):
    gorgon = []
    ttime = time.time()
    Khronos = hex(int(ttime))[2:]
    url_md5 = md5(param.encode('utf-8')).hexdigest()
    gorgon.extend(int(url_md5[i:i+2], 16) for i in range(0, 8, 2))
    
    if stub:
        data_md5 = stub
        gorgon.extend(int(data_md5[i:i+2], 16) for i in range(0, 8, 2))
    else:
        gorgon.extend([0x0] * 4)

    if cookie:
        cookie_md5 = md5(cookie.encode('utf-8')).hexdigest()
        gorgon.extend(int(cookie_md5[i:i+2], 16) for i in range(0, 8, 2))
    else:
        gorgon.extend([0x0] * 4)

    gorgon += [0x1, 0x1, 0x2, 0x4]
    gorgon.extend(int(Khronos[i:i+2], 16) for i in range(0, 8, 2))
    
    return {'X-Gorgon': XG(gorgon).main(), 'X-Khronos': str(int(ttime))}

def get_stub(data):
    if isinstance(data, dict):
        data = json.dumps(data)
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    if not data:
        return "00000000000000000000000000000000"

    m = md5()
    m.update(data)
    return m.hexdigest().upper()

def get_profile(session_id, device_id, iid):
    url = f"https://api.tiktokv.com/passport/account/info/v2/?id=kaa&version_code=34.0.0&language=en&app_name=lite&app_version=34.0.0&carrier_region=SA&device_id={device_id}&tz_offset=10800&mcc_mnc=42001&locale=en&sys_region=SA&aid=473824&screen_width=1284&os_api=18&ac=WIFI&os_version=17.3&app_language=en&tz_name=Asia/Riyadh&carrier_region1=SA&build_number=340002&device_platform=iphone&iid={iid}&device_type=iPhone13,4"
    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": f"sessionid={session_id}",
        "sdk-version": "2",
        "user-agent": "com.zhiliaoapp.musically/432424234 (Linux; U; Android 5; en; Build/PI;tt-ok/3.12.13.1)",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("data", {}).get("username", "None")
    except requests.RequestException as e:
        return f"Error: {str(e)}"

def check_is_changed(last_username, session_id, device_id, iid):
    return get_profile(session_id, device_id, iid) != last_username

def change_username(session_id, device_id, iid, last_username, new_username):
    data = f"aid=364225&unique_id={new_username}"
    param = f"aid=364225&device_id={device_id}&iid={iid}&app_name=tiktok_snail"
    
    sig = run(param, get_stub(data), None)
    url = f"https://api.tiktokv.com/aweme/v1/commit/user/?{param}"

    headers = {
        "cookie": f"sessionid={session_id}",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-khronos": sig["X-Khronos"],
        "x-gorgon": sig["X-Gorgon"],
        "user-agent": "com.zhiliaoapp.musically/2026902040 (Linux; U; Android 8.1.0; en; iPhone13,4; Build/OPM2.171019.012;tt-ok/3.10.1.2)",
    }
    response = requests.post(url, data=data, headers=headers)
    
    if response.status_code == 200:
        if check_is_changed(last_username, session_id, device_id, iid):
            return f"Success! Your username has been changed to {new_username}."
        else:
            return "Failed to change the username."
    else:
        return f"Error: {response.status_code}, {response.text}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/change-username', methods=['POST'])
def change_username_route():
    data = request.json
    session_id = data.get('sessionId')
    new_username = data.get('newUsername')

    device_id = "your_device_id"
    iid = "your_iid"
    last_username = get_profile(session_id, device_id, iid)
    
    if not last_username or last_username == "None":
        return jsonify({"message": "Error: Unable to retrieve current username. Check session ID."})
    
    result = change_username(session_id, device_id, iid, last_username, new_username)
    
    return jsonify({"message": result})

if __name__ == '__main__':
    app.run(debug=True)
