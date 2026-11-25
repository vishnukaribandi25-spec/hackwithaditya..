import json
from pathlib import Path

from pydantic import ValidationError

from app.models.scheme import Scheme

SCHEMES_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "schemes.json"


class SchemeDataError(Exception):
    """Raised when the scheme catalog cannot be loaded or validated."""


def load_schemes() -> list[Scheme]:
    try:
        with SCHEMES_DATA_PATH.open("r", encoding="utf-8") as file:
            records = json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        raise SchemeDataError("The scheme catalog could not be read") from exc

    if not isinstance(records, list):
        raise SchemeDataError("The scheme catalog must contain a JSON array")

    try:
        return [Scheme.model_validate(record) for record in records]
    except ValidationError as exc:
        raise SchemeDataError("The scheme catalog contains invalid scheme data") from exc
