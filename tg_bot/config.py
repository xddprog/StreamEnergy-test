from environs import Env


def load_bot_token() -> str:
    env = Env()
    env.read_env()
    return env.str("BOT_TOKEN")
