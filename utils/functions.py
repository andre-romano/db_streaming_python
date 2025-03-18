from dotenv import load_dotenv
import os

load_dotenv()


def get_env(key, default=None):
    env = os.getenv(key)
    if env:
        return env
    return default