from environs import Env


def load_config(path: str | None = None) -> Env:
    env = Env()
    env.read_env(path)
    return env
