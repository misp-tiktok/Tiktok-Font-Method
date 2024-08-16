from flask import Flask, request, jsonify
import hashlib
import json
import random
import time
import requests
from urllib.parse import quote
from copy import deepcopy
from hashlib import md5

app = Flask(__name__)

def hex_string(num):
    tmp_string = hex(num)[2:]
    if len(tmp_string) < 2:
        tmp_string = '0' + tmp_string
    return tmp_string

def RBIT(num):
    result = ''
    tmp_string = bin(num)[2:]
    while len(tmp_string) < 8:
        tmp_string = '0' + tmp_string
    for i in range(0, 8):
        result = result + tmp_string[7 - i]
    return int(result, 2)

def reverse(num):
    tmp_string = hex(num)[2:]
    if len(tmp_string) < 2:
        tmp_string = '0' + tmp_string
    return int(tmp_string[1:] + tmp_string[:1], 16)

class XG:
    def __init__(self, debug):
        self.length = 0x14
        self.debug = debug
        self.hex_CE0 = [0x05, 0x00, 0x50, random.choice(range(0, 0xFF)), 0x47, 0x1e, 0x00, random.choice(range(0, 0xFF)) & 0xf0]

    def addr_BA8(self):
        tmp = ''
        hex_BA8 = [i for i in range(0x100)]
        for i in range(0x100):
            if i == 0:
                A = 0
            elif tmp:
                A = tmp
            else:
                A = hex_BA8[i - 1]
            B = self.hex_CE0[i % 0x8]
            if A == 0x05:
                if i != 1:
                    if tmp != 0x05:
                        A = 0
            C = A + i + B
            while C >= 0x100:
                C -= 0x100
            if C < i:
                tmp = C
            else:
                tmp = ''
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
            while C >= 0x100:
                C -= 0x100
            tmp_add.append(C)
            D = tmp_hex[C]
            tmp_hex[i + 1] = D
            E = D + D
            while E >= 0x100:
                E -= 0x100
            F = tmp_hex[E]
            G = A ^ F
            debug[i] = G
        return debug

    def calculate(self, debug):
        for i in range(self.length):
            A = debug[i]
            B = reverse(A)
            C = debug[(i + 1) % self.length]
            D = B ^ C
            E = RBIT(D)
            F = E ^ self.length
            G = ~F
            while G < 0:
                G += 0x100000000
            H = int(hex(G)[-2:], 16)
            debug[i] = H
        return debug

    def main(self):
        result = ''.join(hex_string(item) for item in self.calculate(self.initial(self.debug, self.addr_BA8())))
        return f'8404{hex_string(self.hex_CE0[7])}{hex_string(self.hex_CE0[3])}{hex_string(self.hex_CE0[1])}{hex_string(self.hex_CE0[6])}{result}'

def X_Gorgon(param, data, cookie):
    gorgon = []
    ttime = time.time()
    Khronos = hex(int(ttime))[2:]
    url_md5 = md5(bytearray(param, 'utf-8')).hexdigest()
    gorgon.extend(int(url_md5[2 * i: 2 * i + 2], 16) for i in range(4))
    
    if data:
        data_md5 = md5(data.encode('utf-8')).hexdigest()
        gorgon.extend(int(data_md5[2 * i: 2 * i + 2], 16) for i in range(4))
    else:
        gorgon.extend([0x0] * 4)
        
    if cookie:
        cookie_md5 = md5(bytearray(cookie, 'utf-8')).hexdigest()
        gorgon.extend(int(cookie_md5[2 * i: 2 * i + 2], 16) for i in range(4))
    else:
        gorgon.extend([0x0] * 4)
    
    gorgon.extend([0x1, 0x1, 0x2, 0x4])
    gorgon.extend(int(Khronos[2 * i: 2 * i + 2], 16) for i in range(4))
    
    return {'X-Gorgon': XG(gorgon).main(), 'X-Khronos': str(int(ttime))}

def run(param="", stub="", cookie=""):
    gorgon = []
    ttime = time.time()
    Khronos = hex(int(ttime))[2:]
    url_md5 = md5(bytearray(param, 'utf-8')).hexdigest()
    gorgon.extend(int(url_md5[2 * i: 2 * i + 2], 16) for i in range(4))
    
    if stub:
        data_md5 = stub
        gorgon.extend(int(data_md5[2 * i: 2 * i + 2], 16) for i in range(4))
    else:
        gorgon.extend([0x0] * 4)
        
    if cookie:
        cookie_md5 = md5(bytearray(cookie, 'utf-8')).hexdigest()
        gorgon.extend(int(cookie_md5[2 * i: 2 * i + 2], 16) for i in range(4))
    else:
        gorgon.extend([0x0] * 4)
    
    gorgon.extend([0x1, 0x1, 0x2, 0x4])
    gorgon.extend(int(Khronos[2 * i: 2 * i + 2], 16) for i in range(4))
    
    return {'X-Gorgon': XG(gorgon).main(), 'X-Khronos': str(int(ttime))}

def get_stub(data):
    if isinstance(data, dict):
        data = json.dumps(data)
    if isinstance(data, str):
        data = data.encode('utf-8')
    if not data:
        return "00000000000000000000000000000000"
    return md5(data).hexdigest().upper()

def get_profile(session_id, device_id, iid):
    """Retrieve the current TikTok username for a given session, device, and iid."""
    try:
        url = f"https://api.tiktokv.com/passport/account/info/v2/?id=kaa&version_code=34.0.0&language=en&app_name=lite&app_version=34.0.0&carrier_region=SA&device_id={device_id}&tz_offset=10800&mcc_mnc=42001&locale=en&sys_region=SA&aid=473824&screen_width=1284&os_api=18&ac=WIFI&os_version=17.3&app_language=en&tz_name=Asia/Riyadh&carrier_region1=SA&build_number=340002&device_platform=iphone&iid={iid}&device_type=iPhone13,4"
        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": f"sessionid={session_id}",
            "sdk-version": "2",
            "user-agent": "com.zhiliaoapp.musically/432424234 (Linux; U; Android 5; en; fewfwdw; Build/PI;tt-ok/3.12.13.1)",
        }
        response = requests.get(url, headers=headers, cookies={"sessionid": session_id})
        response.raise_for_status()
        return response.json()["data"]["username"]
    except Exception as e:
        app.logger.error(f"Error retrieving profile: {e}")
        return "None"

def check_is_changed(last_username, session_id, device_id, iid):
    """Check if the username has been changed in the TikTok profile."""
    return get_profile(session_id, device_id, iid) != last_username

def change_username(session_id, device_id, iid, last_username, new_username):
    """Attempt to change a TikTok username."""
    data = f"aid=364225&unique_id={quote(new_username)}"
    parm = f"aid=364225&residence=&device_id={device_id}&version_name=1.1.0&os_version=17.4.1&iid={iid}&app_name=tiktok_snail&locale=en&ac=4G&sys_region=SA&version_code=1.1.0&channel=App%20Store&op_region=SA&os_api=18&device_brand=iPad&idfv=16045E07-1ED5-4350-9318-77A1469C0B89&device_platform=iPad&device_type=iPad13,4&carrier_region1=&tz_name=Asia/Riyadh&account_region=sa&build_number=11005&tz_offset=10800&app_language=en&carrier_region=&current_region=&aid=364225&mcc_mnc=&screen_width=1284&uoo=1&content_language=&language=en&cdid=B75649A607DA449D8FF2ADE97E0BC3F1&openudid=7b053588b18d61b89c891592139b68d918b44933&app_version=1.1.0"
    sig = run(parm, md5(data.encode("utf-8")).hexdigest(), None)
    url = f"https://api.tiktokv.com/aweme/v1/commit/user/?{parm}"
    headers = {
        "Connection": "keep-alive",
        "User-Agent": "Whee 1.1.0 rv:11005 (iPad; iOS 17.4.1; en_SA@calendar=gregorian) Cronet",
        "Cookie": f"sessionid={session_id}",
    }
    headers.update(sig)
    response = requests.post(url, data=data, headers=headers)
    result = response.text
    if "unique_id" in result:
        if check_is_changed(last_username, session_id, device_id, iid):
            return "Username change successful."
        else:
            return "Failed to change username: " + str(result)
    else:
        return "Failed to change username: " + str(result)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/change-username', methods=['POST'])
def change_username_route():
    try:
        data = request.json
        session_id = data.get('sessionId')
        new_username = data.get('newUsername')

        if not session_id or not new_username:
            return jsonify({"message": "Error: Missing sessionId or newUsername"}), 400

        device_id = "your_device_id"  # Replace with actual device_id
        iid = "your_iid"  # Replace with actual iid
        last_username = get_profile(session_id, device_id, iid)

        if not last_username or last_username == "None":
            return jsonify({"message": "Error: Unable to retrieve current username. Check session ID."}), 400
        
        result = change_username(session_id, device_id, iid, last_username, new_username)
        
        return jsonify({"message": result})
    except Exception as e:
        app.logger.error(f"Error in /change-username: {e}")
        return jsonify({"message": "An error occurred on the server."}), 500

if __name__ == '__main__':
    app.run(debug=True)
