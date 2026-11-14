import ttkbootstrap as ttk
from ttkbootstrap.constants import (
    BOTH,
    CENTER,
    END,
    LEFT,
    RIGHT,
    VERTICAL,
    W,
    X,
    Y,
    YES,
)
from ttkbootstrap.dialogs import Messagebox

from controllers.contacts_controller import ContactsController
from models.contacts_model import DuplicateContactError


class ContactsView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)
        self.pack(fill=BOTH, expand=YES)
        self.controller = ContactsController()
        self.contacts = []
        self.current_segment = "Todos"
        self.search_text = ""
        self.filter_buttons = {}

        self.container = ttk.Frame(self, padding=8)
        self.container.pack(side=LEFT, fill=Y)
        self.App_title = "Contactos"
        ttk.Label(
            self.container,
            text=self.App_title,
            font=("Helvetica", 16, "bold"),
        ).pack(pady=10)
        self.count_label = ttk.Label(
            self.container,
            text="",
            font=("Helvetica", 9),
            bootstyle="secondary",
        )
        self.count_label.pack(pady=(0, 8))

        ttk.Button(
            self.container,
            text="Agregar Contacto",
            bootstyle="primary",
            command=self.open_contact_form,
        ).pack(pady=4, fill=X)
        ttk.Button(
            self.container,
            text="Ver / Editar Contacto",
            bootstyle="outline-secondary",
            command=self.ver_contacto,
        ).pack(pady=4, fill=X)
        ttk.Button(
            self.container,
            text="Eliminar Contacto",
            bootstyle="outline-danger",
            command=self._delete_contact,
        ).pack(pady=4, fill=X)

        self.main_area = ttk.Frame(self, padding=12)
        self.main_area.pack(side=RIGHT, fill=BOTH, expand=YES)

        self.setup_filters()
        self.setup_treeview()
        self.refresh()

    def setup_filters(self):
        filter_frame = ttk.Frame(self.main_area, padding=(0, 0, 0, 10))
        filter_frame.pack(fill=X)

        ttk.Label(
            filter_frame,
            text="FILTROS:",
            font=("Helvetica", 9, "bold"),
            bootstyle="secondary",
        ).pack(side=LEFT, padx=(0, 10))

        segments = (
            ("Todos", "Todos"),
            ("Natural", "Natural"),
            ("Corporativo", "Corporativo"),
            ("Mayorista", "Mayorista"),
            ("PYME", "PYME"),
            ("Otro", "Otro"),
        )
        for key, label in segments:
            button = ttk.Button(
                filter_frame,
                text=label,
                bootstyle="primary" if key == "Todos" else "secondary-outline",
                command=lambda current=key: self._set_segment(current),
            )
            button.pack(side=LEFT, padx=2)
            self.filter_buttons[key] = button

        ttk.Label(filter_frame, text="Buscar:", bootstyle="secondary").pack(
            side=RIGHT, padx=(10, 4)
        )
        self.search_var = ttk.StringVar()
        self.search_var.trace_add("write", lambda *_args: self._on_search())
        ttk.Entry(
            filter_frame,
            textvariable=self.search_var,
            bootstyle="light",
            width=24,
        ).pack(side=RIGHT)

    def setup_treeview(self):
        tree_frame = ttk.Frame(self.main_area)
        tree_frame.pack(fill=BOTH, expand=YES)

        columns = (
            "nombre",
            "cedula",
            "telefono",
            "email",
            "estado",
            "segmento",
            "contacto",
            "direccion",
        )
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            bootstyle="light",
        )

        headings = {
            "nombre": "NOMBRE O RAZÓN SOCIAL",
            "cedula": "CÉDULA / RIF",
            "telefono": "TELÉFONO",
            "email": "CORREO",
            "estado": "ESTADO",
            "segmento": "SEGMENTO",
            "contacto": "CONTACTO PRINCIPAL",
            "direccion": "DIRECCIÓN",
        }
        for column, text in headings.items():
            self.tree.heading(column, text=text)

        widths = {
            "nombre": (210, W),
            "cedula": (120, W),
            "telefono": (125, W),
            "email": (200, W),
            "estado": (95, CENTER),
            "segmento": (120, CENTER),
            "contacto": (160, W),
            "direccion": (220, W),
        }
        for column, (width, anchor) in widths.items():
            self.tree.column(column, width=width, anchor=anchor)

        self.tree.tag_configure("inactivo", background="#E2E3E5", foreground="#6C757D")
        self.tree.tag_configure("natural", background="#D1E7DD", foreground="#0F5132")
        self.tree.tag_configure("corporativo", background="#CFE2FF", foreground="#084298")
        self.tree.tag_configure("mayorista", background="#FFF3CD", foreground="#664D03")
        self.tree.tag_configure("pyme", background="#E2D9F3", foreground="#432874")
        self.tree.tag_configure("otro", background="#E2E3E5", foreground="#41464B")

        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

    def _set_segment(self, segment):
        self.current_segment = segment
        for key, button in self.filter_buttons.items():
            button.configure(
                bootstyle="primary" if key == segment else "secondary-outline"
            )
        self._populate_tree()

    def _on_search(self):
        self.search_text = self.search_var.get().strip().lower()
        self._populate_tree()

    def refresh(self):
        self.contacts = self.controller.get_contacts()
        self._update_filter_buttons()
        self._populate_tree()

    def _update_filter_buttons(self):
        counts = {"Todos": len(self.contacts)}
        for contact in self.contacts:
            segment = contact["segment"] or "Otro"
            counts[segment] = counts.get(segment, 0) + 1
        for key, button in self.filter_buttons.items():
            button.configure(text=f"{key} ({counts.get(key, 0)})")
        self.count_label.configure(
            text=f"{len(self.contacts)} contacto(s) registrado(s)"
        )

    def _populate_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for contact in self.contacts:
            segment = contact["segment"] or "Otro"
            if self.current_segment != "Todos" and segment != self.current_segment:
                continue
            searchable = " ".join(
                str(contact[field] or "")
                for field in (
                    "customer_name",
                    "cedula_rif",
                    "phone",
                    "email",
                    "status",
                    "segment",
                    "main_contact",
                    "address",
                )
            ).lower()
            if self.search_text and self.search_text not in searchable:
                continue

            values = (
                contact["customer_name"] or "",
                contact["cedula_rif"] or "",
                contact["phone"] or "",
                contact["email"] or "",
                contact["status"] or "",
                segment,
                contact["main_contact"] or "",
                contact["address"] or "",
            )
            tag = (
                "inactivo"
                if (contact["status"] or "").strip().lower() == "inactivo"
                else segment.lower()
            )
            self.tree.insert(
                "",
                END,
                iid=str(contact["id_contact"]),
                values=values,
                tags=(tag,),
            )

    def _delete_contact(self):
        selection = self.tree.selection()
        if not selection:
            Messagebox.show_warning(
                "Selecciona un contacto de la tabla.",
                title="Sin selección",
                parent=self,
            )
            return
        contact = self.controller.get_contact(int(selection[0]))
        if contact is None:
            self.refresh()
            return
        confirmed = Messagebox.okcancel(
            f"¿Eliminar el contacto «{contact['customer_name']}»?",
            title="Eliminar contacto",
            alert=True,
            parent=self,
        )
        if confirmed != "OK":
            return
        try:
            self.controller.delete_contact(contact["id_contact"])
        except Exception as error:
            Messagebox.show_error(str(error), title="No se pudo eliminar", parent=self)
            return
        self.refresh()

    def open_contact_form(self):
        self._open_contact_form()

    def ver_contacto(self):
        selection = self.tree.selection()
        if not selection:
            Messagebox.show_warning(
                "Selecciona un contacto de la tabla.",
                title="Sin selección",
                parent=self,
            )
            return
        self._open_contact_form(int(selection[0]))

    def _open_contact_form(self, contact_id=None):
        contact = (
            self.controller.get_contact(contact_id)
            if contact_id is not None
            else None
        )
        if contact_id is not None and contact is None:
            self.refresh()
            return

        editing = contact is not None
        title = "Ver / Editar contacto" if editing else "Agregar contacto"
        dialog = ttk.Toplevel(title=title)
        dialog.geometry("680x560")
        dialog.minsize(540, 480)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        body = ttk.Frame(dialog, padding=18)
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)
        ttk.Label(body, text=title, font=("Helvetica", 17, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 12)
        )

        form = ttk.Labelframe(body, text="Datos del contacto", padding=12)
        form.grid(row=1, column=0, columnspan=2, sticky="nsew")
        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=1)

        fields = (
            ("Nombre o razón social", "customer_name", 0, 0),
            ("Cédula / RIF", "cedula_rif", 1, 0),
            ("Teléfono", "phone", 1, 1),
            ("Correo electrónico", "email", 2, 0),
            ("Estado", "status", 2, 1),
            ("Segmento", "segment", 3, 0),
            ("Contacto principal", "main_contact", 3, 1),
        )
        self.contact_vars = {}
        for label, field, row, column in fields:
            field_frame = ttk.Frame(form)
            field_frame.grid(
                row=row,
                column=column,
                columnspan=2 if field == "customer_name" else 1,
                sticky="ew",
                padx=4,
                pady=5,
            )
            field_frame.grid_columnconfigure(0, weight=1)
            ttk.Label(field_frame, text=label).grid(row=0, column=0, sticky="w")
            if editing:
                initial_value = contact[field] or ""
            else:
                initial_value = "Activo" if field == "status" else ""
            variable = ttk.StringVar(value=initial_value)
            self.contact_vars[field] = variable
            if field == "segment":
                ttk.Combobox(
                    field_frame,
                    textvariable=variable,
                    values=("Natural", "Corporativo", "Mayorista", "PYME", "Otro"),
                    state="readonly",
                ).grid(row=1, column=0, sticky="ew", pady=(3, 0))
            elif field == "status":
                ttk.Combobox(
                    field_frame,
                    textvariable=variable,
                    values=("Activo", "Inactivo"),
                    state="readonly",
                ).grid(row=1, column=0, sticky="ew", pady=(3, 0))
            else:
                ttk.Entry(field_frame, textvariable=variable).grid(
                    row=1, column=0, sticky="ew", pady=(3, 0)
                )

        ttk.Label(form, text="Dirección").grid(
            row=4, column=0, columnspan=2, sticky="w", padx=4, pady=(8, 0)
        )
        address = ttk.Text(form, height=4, wrap="word")
        address.grid(row=5, column=0, columnspan=2, sticky="ew", padx=4, pady=(3, 0))
        if editing and contact["address"]:
            address.insert("1.0", contact["address"])

        actions = ttk.Frame(body)
        actions.grid(row=2, column=0, columnspan=2, sticky="e", pady=(14, 0))
        ttk.Button(actions, text="Cancelar", command=dialog.destroy).pack(
            side=RIGHT, padx=(8, 0)
        )
        ttk.Button(
            actions,
            text="Guardar cambios" if editing else "Guardar contacto",
            bootstyle="primary",
            command=lambda: self.save_contact(dialog, address, contact_id),
        ).pack(side=RIGHT)

    def save_contact(self, dialog, address, contact_id=None):
        contact = {
            field: variable.get().strip()
            for field, variable in self.contact_vars.items()
        }
        contact["address"] = address.get("1.0", "end-1c").strip()
        if not contact["customer_name"]:
            Messagebox.show_warning(
                "Ingresa el nombre o la razón social del contacto.",
                title="Falta el nombre",
                parent=dialog,
            )
            return

        try:
            if contact_id is None:
                self.controller.add_contact(contact)
            else:
                self.controller.update_contact(contact_id, contact)
        except DuplicateContactError as error:
            Messagebox.show_warning(str(error), title="Dato duplicado", parent=dialog)
            return
        except Exception as error:
            Messagebox.show_error(
                f"No fue posible guardar el contacto.\n\n{error}",
                title="No se pudo guardar",
                parent=dialog,
            )
            return

        dialog.destroy()
        self.refresh()
