import json
import os
from pathlib import Path
from typing import Type


class JsonRepository:
    def __init__(self, file_path: str, model_class: Type):
        self.file_path = Path(file_path)
        self.model_class = model_class

    def _ensure_file(self) -> None:
        """
        Crea la carpeta y el archivo JSON si todavía no existen.
        """
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            self._write_data([])

    def _read_data(self) -> list[dict]:
        self._ensure_file()

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError(
                    f"El archivo {self.file_path} no contiene una lista válida."
                )

            return data

        except json.JSONDecodeError as exc:
            raise ValueError(
                f"El archivo {self.file_path} contiene JSON inválido."
            ) from exc

    def _write_data(self, data: list[dict]) -> None:
        """
        Guarda primero en un archivo temporal y luego reemplaza el original.
        Esto reduce el riesgo de dejar el archivo corrupto si ocurre un error.
        """
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        temp_path = self.file_path.with_suffix(
            self.file_path.suffix + ".tmp"
        )

        try:
            with temp_path.open("w", encoding="utf-8") as file:
                json.dump(
                    data,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

            os.replace(temp_path, self.file_path)

        except Exception:
            if temp_path.exists():
                temp_path.unlink()

            raise

    def get_all(self) -> list:
        data = self._read_data()

        return [
            self.model_class.from_dict(item)
            for item in data
        ]

    def get_by_id(self, object_id: str):
        for item in self.get_all():
            if item.id == object_id:
                return item

        return None

    def add(self, item) -> None:
        items = self.get_all()

        if any(existing.id == item.id for existing in items):
            raise ValueError(
                f"Ya existe un registro con ID {item.id}."
            )

        items.append(item)
        self.save_all(items)

    def update(self, item) -> None:
        items = self.get_all()

        for index, existing in enumerate(items):
            if existing.id == item.id:
                items[index] = item
                self.save_all(items)
                return

        raise ValueError(
            f"No existe un registro con ID {item.id}."
        )

    def delete(self, object_id: str) -> None:
        items = self.get_all()

        filtered_items = [
            item for item in items
            if item.id != object_id
        ]

        if len(filtered_items) == len(items):
            raise ValueError(
                f"No existe un registro con ID {object_id}."
            )

        self.save_all(filtered_items)

    def save_all(self, items: list) -> None:
        data = [
            item.to_dict()
            for item in items
        ]

        self._write_data(data)