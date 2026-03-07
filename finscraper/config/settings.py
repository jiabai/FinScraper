from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    request_timeout: int = 30
    max_retries: int = 3
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    data_dir: str = "data"
    
    log_level: str = "INFO"
    log_file: str = "logs/finscraper.log"

    model_config = {
        "env_prefix": "FINSCRAPER_",
    }


settings = Settings()
