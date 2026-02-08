import hashlib
import hmac
import os
import requests
from bs4 import BeautifulSoup
import json

BASE = "http://192.168.2.1"
INITIAL = f"{BASE}/html/index.html#/login"
USERNAME = "admin"
PASSWORD = "Televisao12c@"

session = requests.Session()

r = session.get(INITIAL)

soup = BeautifulSoup(r.text, "html.parser")

csrf_param = soup.find("meta", {"name": "csrf_param"})["content"]
csrf_token = soup.find("meta", {"name": "csrf_token"})["content"]

first_nonce = os.urandom(32).hex()

payload_nonce = {
    "data": {
        "username": USERNAME,
        "firstnonce": first_nonce
    },
    "csrf": {
        "csrf_param": csrf_param,
        "csrf_token": csrf_token
    }
}

print(json.dumps(payload_nonce, indent=2))

r = session.post(f"{BASE}/api/system/user_login_nonce", json=payload_nonce)

res = r.json()

salt = bytes.fromhex(res["salt"])
iterations = res["iterations"]
final_nonce = res["servernonce"]

auth_msg = f"{first_nonce},{final_nonce},{final_nonce}".encode()

salted_password = hashlib.pbkdf2_hmac(
    "sha256",
    PASSWORD.encode("utf-8"),
    salt,
    iterations
)

salted_password_hex = salted_password.hex()
salted_password = bytes.fromhex(salted_password_hex)

salted_password_hex = salted_password.hex()
salted_password_bytes = bytes.fromhex(salted_password_hex)

client_key = hmac.new(
    b"Client Key",
    salted_password, 
    hashlib.sha256
).digest()

stored_key = hashlib.sha256(client_key).digest()

client_signature = hmac.new(
    auth_msg,
    stored_key,
    hashlib.sha256
).digest()

client_proof = bytes(a ^ b for a, b in zip(client_key, client_signature)).hex()

payload_proof = {
    "data": {
        "clientproof": client_proof,
        "finalnonce": final_nonce
    },
    "csrf": {
        "csrf_param": res["csrf_param"],
        "csrf_token": res["csrf_token"]
    }
}

r = session.post(f"{BASE}/api/system/user_login_proof", json=payload_proof)


login_result = r.json()

FIREWALL_URL = f"{BASE}/api/ntwk/firewall"

headers = {
    "Content-Type": "application/json; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": f"{BASE}/html/index.html",
    "Origin": BASE
}

payload = {
    "data": {
        "SetLevel": "Disable",
        "SynFlooding": True,
        "IcmpFlooding": False,
        "ArpAttack": False,
        "CurrentLevel": "Low"
    },
    "csrf": {
        "csrf_param": login_result["csrf_param"],
        "csrf_token": login_result["csrf_token"]
    }
}

r = session.post(FIREWALL_URL, headers=headers, json=payload)

print("Status:", r.status_code)
print("Resposta:", r.text)
