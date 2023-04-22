from typing import Any, Dict, List

from pydantic import (
    AnyHttpUrl,
    BaseSettings,
    PostgresDsn,
    validator,
)


class Settings(BaseSettings):
    API: str = '/api'
    DOCS: str = '/docs'
    STARTUP: str = 'startup'
    SHUTDOWN: str = 'shutdown'
    SECRET_KEY: str
    NAME: str = 'Cyberzone booking service'
    VERSION: str = '1.0'
    DESCRIPTION: str = 'Service for booking PCs in cyberzone.'

    SWAGGER_UI_PARAMETERS: Dict[str, Any] = {
        'displayRequestDuration': True,
        'filter': True,
    }

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator('BACKEND_CORS_ORIGINS', pre=True)
    def assemble_cors_origins(
            cls, value: str | List[str],
    ) -> str | List[str]:
        if isinstance(value, str) and not value.startswith('['):
            return [i.strip() for i in value.split(',')]
        elif isinstance(value, (list, str)):
            return value

        raise ValueError(value)

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str = ''
    DB_NAME: str
    DATABASE_URI: PostgresDsn | None = None

    @validator('DATABASE_URI', pre=True)
    def assemble_db_connection(
            cls, value: str | None, values: Dict[str, Any],
    ) -> str:
        if isinstance(value, str):
            return value

        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('DB_USER'),
            password=values.get('DB_PASSWORD'),
            host=values.get('DB_HOST'),
            port=values.get('DB_PORT'),
            path='/{0}'.format(values.get('DB_NAME')),
        )

    class Config(object):
        case_sensitive = True


settings = Settings()
