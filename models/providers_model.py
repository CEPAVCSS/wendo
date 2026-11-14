import sqlite3

from models.conector.SQLiteConector import SQLiteConnector


class DuplicateProviderError(ValueError):
    pass


class ProvidersModel:
    fields = (
        "rif_prefix",
        "rif_number",
        "reason",
        "provider_type",
        "conatct_name",
        "contact_phone",
        "contact_email",
        "state",
        "city",
        "address",
    )

    def __init__(self, db=None):
        self.db = db or SQLiteConnector()

    def get_providers(self):
        columns = ", ".join(("id_provider",) + self.fields)
        return self.db.fetch_all(
            f"SELECT {columns} FROM providers ORDER BY reason COLLATE NOCASE"
        )

    def get_provider(self, provider_id):
        columns = ", ".join(("id_provider",) + self.fields)
        rows = self.db.fetch_all(
            f"SELECT {columns} FROM providers WHERE id_provider = ?",
            (provider_id,),
        )
        return rows[0] if rows else None

    def add_provider(self, provider):
        values = [str(provider.get(field) or "").strip() for field in self.fields]
        reason = values[2]
        contact_phone = values[5]

        if not reason:
            raise ValueError("La razón social o nombre es obligatorio.")
        if not contact_phone:
            raise ValueError("El teléfono de contacto es obligatorio.")

        if self.db.fetch_all(
            "SELECT 1 FROM providers WHERE LOWER(TRIM(reason)) = LOWER(TRIM(?)) LIMIT 1",
            (reason,),
        ):
            raise DuplicateProviderError(
                "Ya existe un proveedor con esa razón social."
            )

        columns = ", ".join(self.fields)
        placeholders = ", ".join("?" for _ in self.fields)
        try:
            self.db.execute(
                f"INSERT INTO providers ({columns}) VALUES ({placeholders})",
                tuple(values),
            )
        except sqlite3.IntegrityError as error:
            raise DuplicateProviderError(
                "El proveedor ya está registrado."
            ) from error

    def delete_provider(self, provider_id):
        self.db.execute(
            "DELETE FROM providers WHERE id_provider = ?", (provider_id,)
        )
