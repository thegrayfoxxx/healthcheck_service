from os import getenv


def get_env_var(var_name: str) -> str:
    env = getenv(var_name)
    if not env:
        raise ValueError(f"Environment variable {var_name} is not set")
    return env
