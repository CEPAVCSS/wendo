from models.conector.SQLiteConector import SQLiteConnector


class SearchModel:
    def __init__(self, db=None):
        self.db = db or SQLiteConnector()

    def get_dashboard_stats(self):
        def scalar(query, params=()):
            rows = self.db.fetch_all(query, params)
            return rows[0][0] if rows else 0

        return {
            "contacts": scalar("SELECT COUNT(*) FROM contacts"),
            "active_contacts": scalar(
                "SELECT COUNT(*) FROM contacts WHERE LOWER(TRIM(COALESCE(status, ''))) = 'activo'"
            ),
            "providers": scalar("SELECT COUNT(*) FROM providers"),
            "orders": scalar("SELECT COUNT(*) FROM orders"),
            "pending_orders": scalar(
                "SELECT COUNT(*) FROM orders WHERE LOWER(TRIM(COALESCE(order_status, ''))) = 'pendiente'"
            ),
            "paid_orders": scalar(
                "SELECT COUNT(*) FROM orders WHERE LOWER(TRIM(COALESCE(order_status, ''))) "
                "IN ('pagado', 'entregado')"
            ),
            "orders_amount": scalar(
                "SELECT COALESCE(SUM(order_amount), 0) FROM orders"
            ),
            "tasks": scalar("SELECT COUNT(*) FROM tasks"),
            "pending_tasks": scalar(
                "SELECT COUNT(*) FROM tasks WHERE LOWER(TRIM(COALESCE(status, ''))) "
                "IN ('pendiente', 'en progreso')"
            ),
            "completed_tasks": scalar(
                "SELECT COUNT(*) FROM tasks WHERE LOWER(TRIM(COALESCE(status, ''))) = 'completada'"
            ),
        }

    def search(self, text="", category="Todo"):
        term = f"%{text.strip().lower()}%"
        results = []

        if category in ("Todo", "Contactos"):
            rows = self.db.fetch_all(
                """SELECT id_contact, customer_name, cedula_rif, phone, email, status, segment,
                          main_contact, address
                   FROM contacts
                   WHERE LOWER(COALESCE(customer_name, '')) LIKE ?
                      OR LOWER(COALESCE(cedula_rif, '')) LIKE ?
                      OR LOWER(COALESCE(phone, '')) LIKE ?
                      OR LOWER(COALESCE(email, '')) LIKE ?
                      OR LOWER(COALESCE(status, '')) LIKE ?
                      OR LOWER(COALESCE(segment, '')) LIKE ?
                      OR LOWER(COALESCE(main_contact, '')) LIKE ?
                      OR LOWER(COALESCE(address, '')) LIKE ?
                   ORDER BY customer_name COLLATE NOCASE""",
                (term,) * 8,
            )
            for row in rows:
                detail = " · ".join(
                    part
                    for part in (
                        f"Cédula/RIF: {row['cedula_rif']}" if row["cedula_rif"] else "",
                        f"Tel: {row['phone']}" if row["phone"] else "",
                        row["email"] or "",
                        row["segment"] or "",
                    )
                    if part
                )
                results.append(
                    {
                        "type": "Contacto",
                        "title": row["customer_name"] or "(sin nombre)",
                        "detail": detail or "Sin datos de contacto",
                        "status": row["status"] or "",
                    }
                )

        if category in ("Todo", "Proveedores"):
            rows = self.db.fetch_all(
                """SELECT id_provider, rif_prefix, rif_number, reason, provider_type,
                          conatct_name, contact_phone, contact_email, state, city, address
                   FROM providers
                   WHERE LOWER(COALESCE(reason, '')) LIKE ?
                      OR LOWER(COALESCE(rif_prefix, '')) LIKE ?
                      OR LOWER(COALESCE(rif_number, '')) LIKE ?
                      OR LOWER(COALESCE(provider_type, '')) LIKE ?
                      OR LOWER(COALESCE(conatct_name, '')) LIKE ?
                      OR LOWER(COALESCE(contact_phone, '')) LIKE ?
                      OR LOWER(COALESCE(contact_email, '')) LIKE ?
                      OR LOWER(COALESCE(state, '')) LIKE ?
                      OR LOWER(COALESCE(city, '')) LIKE ?
                      OR LOWER(COALESCE(address, '')) LIKE ?
                   ORDER BY reason COLLATE NOCASE""",
                (term,) * 10,
            )
            for row in rows:
                rif = "".join(
                    part for part in (row["rif_prefix"], row["rif_number"]) if part
                )
                detail = " · ".join(
                    part
                    for part in (
                        f"RIF: {rif}" if rif else "",
                        f"Tel: {row['contact_phone']}" if row["contact_phone"] else "",
                        row["contact_email"] or "",
                        row["conatct_name"] or "",
                        row["city"] or "",
                        row["state"] or "",
                    )
                    if part
                )
                results.append(
                    {
                        "type": "Proveedor",
                        "title": row["reason"] or "(sin razón social)",
                        "detail": detail or "Sin datos de contacto",
                        "status": row["provider_type"] or "",
                    }
                )

        if category in ("Todo", "Pedidos"):
            rows = self.db.fetch_all(
                """SELECT id_order, order_number, order_date, order_type, customer_name,
                          order_status, order_amount
                   FROM orders
                   WHERE LOWER(COALESCE(order_number, '')) LIKE ?
                      OR LOWER(COALESCE(order_date, '')) LIKE ?
                      OR LOWER(COALESCE(order_type, '')) LIKE ?
                      OR LOWER(COALESCE(customer_name, '')) LIKE ?
                      OR LOWER(COALESCE(order_status, '')) LIKE ?
                      OR CAST(COALESCE(order_amount, 0) AS TEXT) LIKE ?
                   ORDER BY order_date DESC, id_order DESC""",
                (term,) * 6,
            )
            for row in rows:
                try:
                    amount = f"${float(row['order_amount'] or 0):,.2f}"
                except (TypeError, ValueError):
                    amount = "$0.00"
                detail = " · ".join(
                    part
                    for part in (
                        row["order_type"] or "",
                        row["customer_name"] or "",
                        amount,
                        row["order_date"] or "",
                    )
                    if part
                )
                results.append(
                    {
                        "type": "Pedido",
                        "title": row["order_number"] or "(sin número)",
                        "detail": detail,
                        "status": row["order_status"] or "",
                    }
                )

        if category in ("Todo", "Tareas"):
            rows = self.db.fetch_all(
                """SELECT id_task, tarea, fecha, prioridad, descripcion, status
                   FROM tasks
                   WHERE LOWER(COALESCE(tarea, '')) LIKE ?
                      OR LOWER(COALESCE(fecha, '')) LIKE ?
                      OR LOWER(COALESCE(prioridad, '')) LIKE ?
                      OR LOWER(COALESCE(descripcion, '')) LIKE ?
                      OR LOWER(COALESCE(status, '')) LIKE ?
                   ORDER BY id_task DESC""",
                (term,) * 5,
            )
            for row in rows:
                detail = " · ".join(
                    part
                    for part in (
                        f"Prioridad: {row['prioridad']}" if row["prioridad"] else "",
                        f"Vence: {row['fecha']}" if row["fecha"] else "",
                        row["descripcion"] or "",
                    )
                    if part
                )
                results.append(
                    {
                        "type": "Tarea",
                        "title": row["tarea"] or "(sin título)",
                        "detail": detail or "Sin descripción",
                        "status": row["status"] or "",
                    }
                )

        return results
