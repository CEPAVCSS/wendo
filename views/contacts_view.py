import ttkbootstrap as ttk
from tkinter import messagebox
from ttkbootstrap.widgets import Tableview

from controllers.contacts_controller import ContactsController
from models.contacts_model import DuplicateContactError

class ContactsView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)
        self.pack(fill="both", expand=True)
        self.controller = ContactsController()
        self.contacts_table = None
        self.empty_label = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        heading = ttk.Frame(self)
        heading.grid(row=0, column=0, sticky="ew", pady=(4, 2))
        heading.grid_columnconfigure(0, weight=1)
        ttk.Label(
            heading,
            text="Contactos",
            font=("Helvetica", 20, "bold"),
        ).grid(row=0, column=0, sticky="w")
        ttk.Button(
            heading,
            text="Agregar contacto",
            bootstyle="primary",
            command=self.open_contact_form,
        ).grid(row=0, column=1, sticky="e")

        ttk.Label(
            self,
            text="Directorio de clientes y personas de contacto",
            font=("Helvetica", 10),
        ).grid(row=1, column=0, sticky="w", pady=(0, 10))

        self.show_contacts()

    def show_contacts(self):
        if self.contacts_table:
            self.contacts_table.destroy()
            self.contacts_table = None
        if self.empty_label:
            self.empty_label.destroy()
            self.empty_label = None

        contacts = self.controller.get_contacts()
        if not contacts:
            self.empty_label = ttk.Label(
                self,
                text="Aún no hay contactos. Agrega el primero para comenzar.",
                anchor="center",
                bootstyle="secondary",
            )
            self.empty_label.grid(row=2, column=0, sticky="nsew", pady=24)
            return

        columns = [
            {"text": "Nombre o razón social", "width": 190, "minwidth": 130, "stretch": True},
            {"text": "Cédula / RIF", "width": 130, "minwidth": 100, "stretch": True},
            {"text": "Teléfono", "width": 125, "minwidth": 95, "stretch": True},
            {"text": "Correo electrónico", "width": 200, "minwidth": 130, "stretch": True},
            {"text": "Estado", "width": 100, "minwidth": 80, "stretch": True},
            {"text": "Segmento", "width": 120, "minwidth": 90, "stretch": True},
            {"text": "Contacto principal", "width": 175, "minwidth": 120, "stretch": True},
            {"text": "Dirección", "width": 220, "minwidth": 140, "stretch": True},
        ]
        self.contacts_table = Tableview(
            self,
            coldata=columns,
            rowdata=[tuple(contact) for contact in contacts],
            bootstyle="primary",
            autofit=False,
            autoalign=True,
            paginated=True,
            searchable=True,
            yscrollbar=True,
        )
        self.contacts_table.grid(row=2, column=0, sticky="nsew")

    def open_contact_form(self):
        dialog = ttk.Toplevel(title="Agregar contacto")
        dialog.geometry("680x560")
        dialog.minsize(540, 480)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        body = ttk.Frame(dialog, padding=18)
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)
        ttk.Label(body, text="Nuevo contacto", font=("Helvetica", 17, "bold")).grid(
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
            variable = ttk.StringVar(value="Activo" if field == "status" else "")
            self.contact_vars[field] = variable
            if field == "segment":
                ttk.Combobox(
                    field_frame,
                    textvariable=variable,
                    values=("Natural", "Corporativo", "Mayorista", "PYME", "Otro"),
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

        actions = ttk.Frame(body)
        actions.grid(row=2, column=0, columnspan=2, sticky="e", pady=(14, 0))
        ttk.Button(actions, text="Cancelar", command=dialog.destroy).pack(
            side="right", padx=(8, 0)
        )
        ttk.Button(
            actions,
            text="Guardar contacto",
            bootstyle="primary",
            command=lambda: self.save_contact(dialog, address),
        ).pack(side="right")

    def save_contact(self, dialog, address):
        contact = {
            field: variable.get().strip()
            for field, variable in self.contact_vars.items()
        }
        contact["address"] = address.get("1.0", "end-1c").strip()
        if not contact["customer_name"]:
            messagebox.showwarning(
                "Falta el nombre",
                "Ingresa el nombre o la razón social del contacto.",
                parent=dialog,
            )
            return

        try:
            self.controller.add_contact(contact)
        except DuplicateContactError as error:
            messagebox.showwarning(
                "Dato duplicado",
                str(error),
                parent=dialog,
            )
            return
        except Exception as error:
            messagebox.showerror(
                "No se pudo guardar",
                f"No fue posible guardar el contacto.\n\n{error}",
                parent=dialog,
            )
            return

        dialog.destroy()
        self.show_contacts()