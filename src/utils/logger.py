import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

import sentry_sdk
from dotenv import load_dotenv


LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "app.log"

_configured = False


def configure_logging() -> None:
    global _configured

    if _configured:
        return

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    _configured = True


def init_sentry() -> bool:
    """
    Inicializa Sentry solamente si existe SENTRY_DSN.
    La aplicación puede funcionar sin Sentry configurado.
    """

    load_dotenv()

    dsn = os.getenv("SENTRY_DSN")

    if not dsn:
        logging.getLogger(__name__).warning(
            "Sentry no configurado: SENTRY_DSN no definido."
        )
        return False

    sentry_sdk.init(
        dsn=dsn,
        environment=os.getenv(
            "SENTRY_ENVIRONMENT",
            "development",
        ),
        traces_sample_rate=0.0,
        send_default_pii=False,
    )

    logging.getLogger(__name__).info(
        "Sentry inicializado correctamente."
    )

    return True


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def report_exception(error: Exception) -> None:
    sentry_sdk.capture_exception(error)