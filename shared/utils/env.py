import os

from dotenv import load_dotenv
load_dotenv()

def get_env(env_name: str, default=None) -> str:
    env = os.getenv(env_name, default)
    if env is None:
        raise Exception(f"Environment variable {env_name} not found")

    if default is not None and type(default) != type(env):
        raise Exception(f"Environment variable {env_name} type mismatch")

    return env
