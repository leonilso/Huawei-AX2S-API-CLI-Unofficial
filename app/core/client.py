import requests
from app.core.config import Settings
import hashlib
import hmac
import os
import requests
from bs4 import BeautifulSoup
import json

class RouterClient:

    def __init__(self):
        Settings.validate()
        self.base = f"http://{Settings.ROUTER_IP}"
        self.password = Settings.ROUTER_PASSWORD
        self.session = requests.Session()
        self.csrf_param = None
        self.csrf_token = None

    def login(self):
        INITIAL = f"{self.base}/html/index.html#/login"
        USERNAME = "admin"
        r = self.session.get(INITIAL)

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

        r = self.session.post(f"{self.base}/api/system/user_login_nonce", json=payload_nonce)

        res = r.json()

        salt = bytes.fromhex(res["salt"])
        iterations = res["iterations"]
        final_nonce = res["servernonce"]

        auth_msg = f"{first_nonce},{final_nonce},{final_nonce}".encode()

        salted_password = hashlib.pbkdf2_hmac(
            "sha256",
            self.password.encode("utf-8"),
            salt,
            iterations
        )

        salted_password_hex = salted_password.hex()
        salted_password = bytes.fromhex(salted_password_hex)

        salted_password_hex = salted_password.hex()

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

        r = self.session.post(f"{self.base}/api/system/user_login_proof", json=payload_proof)

        login_result = r.json()

        self.csrf_param = login_result["csrf_param"]
        self.csrf_token = login_result["csrf_token"]
        pass

    def _update_csrf(self, response_json):
        self.csrf_param = response_json.get("csrf_param")
        self.csrf_token = response_json.get("csrf_token")

    def post(self, endpoint, data):
        payload = {
            "data": data,
            "csrf": {
                "csrf_param": self.csrf_param,
                "csrf_token": self.csrf_token
            }
        }

        r = self.session.post(
            f"{self.base}{endpoint}",
            json=payload,
            headers={
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"{self.base}/html/index.html",
                "Origin": self.base
            }
        )

        result = r.json()
        self._update_csrf(result)
        return result

    def get(self, endpoint):
        r = self.session.get(
            f"{self.base}{endpoint}",
            headers={"X-Requested-With": "XMLHttpRequest"}
        )
        return r.json()
