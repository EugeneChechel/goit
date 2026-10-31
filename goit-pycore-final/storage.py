"""Збереження та завантаження даних у домашній каталог користувача."""

from __future__ import annotations

import pickle
from pathlib import Path

from models import PersonalAssistant

DATA_DIR = Path.home() / ".personal_assistant"
DATA_FILE = DATA_DIR / "assistant.pkl"


def ensure_data_dir() -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR


def save_data(assistant: PersonalAssistant, filepath: Path | None = None) -> None:
    """Зберігає контакти й нотатки через pickle."""
    ensure_data_dir()
    path = filepath or DATA_FILE
    with open(path, "wb") as file:
        pickle.dump(assistant, file)


def load_data(filepath: Path | None = None) -> PersonalAssistant:
    """Завантажує дані. Якщо файлу немає — повертає порожнього помічника."""
    path = filepath or DATA_FILE
    try:
        with open(path, "rb") as file:
            data = pickle.load(file)
    except FileNotFoundError:
        return PersonalAssistant()
    except (pickle.UnpicklingError, EOFError, AttributeError):
        return PersonalAssistant()

    if isinstance(data, PersonalAssistant):
        return data

    return PersonalAssistant()
