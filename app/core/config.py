import os
from dotenv import load_dotenv
load_dotenv()


class Settings:
    ROUTER_IP = os.getenv("ROUTER_IP")
    ROUTER_USER = os.getenv("ROUTER_USER", "admin")
    ROUTER_PASSWORD = os.getenv("ROUTER_PASSWORD")

    @classmethod
    def validate(cls):
        if not cls.ROUTER_IP:
            raise ValueError("ROUTER_IP não definido")
        if not cls.ROUTER_PASSWORD:
            raise ValueError("ROUTER_PASSWORD não definido")
