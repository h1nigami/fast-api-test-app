import os

def load_env() -> None:
    with open(".env", "r") as f:
        env_vars = {k.split("=")[0]: v for k, v in (l.split("=") for l in f)}
        for k, v in env_vars.items():
            os.environ[k] = v

