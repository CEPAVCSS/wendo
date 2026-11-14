import ttkbootstrap as ttk
from ttkbootstrap.constants import (
    BOTH,
    CENTER,
    E,
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

from controllers.providers_controller import ProvidersController
from models.providers_model import DuplicateProviderError
from utils.utils import Utils


class ProvidersView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)
        self.pack(fill=BOTH, expand=YES)
        self.master = master
        self.controller = ProvidersController(master)
        self.providers = []
        self.current_type = "Todos"
        self.search_text = ""
        self.filter_buttons = {}

        self.container = ttk.Frame(self, padding=8)
        self.container.pack(side=LEFT, fill=Y)
        self.App_title = "Proveedores"
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
            text="Agregar Proveedor",
            bootstyle="primary",
            command=self.agregar_proveedor,
        ).pack(pady=4, fill=X)
        ttk.Button(
            self.container,
            text="Ver / Editar Proveedor",
            bootstyle="outline-secondary",
            command=self.ver_proveedor,
        ).pack(pady=4, fill=X)
        ttk.Button(
            self.container,
            text="Eliminar Proveedor",
            bootstyle="outline-danger",
            command=self._delete_provider,
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

        provider_types = (
            ("Todos", "Todos"),
            ("Ordinario", "Ordinario"),
            ("Especial", "Especial"),
            ("Formal", "Formal"),
            ("No Sujeto", "No Sujeto"),
        )
        for key, label in provider_types:
            button = ttk.Button(
                filter_frame,
                text=label,
                bootstyle="primary" if key == "Todos" else "secondary-outline",
                command=lambda current=key: self._set_type(current),
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

        columns = ("rif", "razon", "tipo", "contacto", "telefono", "email", "estado", "ciudad")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            bootstyle="light",
        )

        headings = {
            "rif": "RIF",
            "razon": "RAZÓN SOCIAL",
            "tipo": "TIPO",
            "contacto": "CONTACTO",
            "telefono": "TELÉFONO",
            "email": "CORREO",
            "estado": "ESTADO",
            "ciudad": "CIUDAD",
        }
        for column, text in headings.items():
            self.tree.heading(column, text=text)

        widths = {
            "rif": (120, W),
            "razon": (220, W),
            "tipo": (110, CENTER),
            "contacto": (160, W),
            "telefono": (130, W),
            "email": (200, W),
            "estado": (120, CENTER),
            "ciudad": (130, W),
        }
        for column, (width, anchor) in widths.items():
            self.tree.column(column, width=width, anchor=anchor)

        self.tree.tag_configure("ordinario", background="#D1E7DD", foreground="#0F5132")
        self.tree.tag_configure("especial", background="#CFE2FF", foreground="#084298")
        self.tree.tag_configure("formal", background="#FFF3CD", foreground="#664D03")
        self.tree.tag_configure("no sujeto", background="#E2E3E5", foreground="#41464B")

        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

    def _set_type(self, provider_type):
        self.current_type = provider_type
        for key, button in self.filter_buttons.items():
            button.configure(
                bootstyle="primary" if key == provider_type else "secondary-outline"
            )
        self._populate_tree()

    def _on_search(self):
        self.search_text = self.search_var.get().strip().lower()
        self._populate_tree()

    def refresh(self):
        self.providers = self.controller.get_providers()
        self._update_filter_buttons()
        self._populate_tree()

    def _update_filter_buttons(self):
        counts = {"Todos": len(self.providers)}
        for provider in self.providers:
            provider_type = provider["provider_type"] or "No Sujeto"
            counts[provider_type] = counts.get(provider_type, 0) + 1
        for key, button in self.filter_buttons.items():
            button.configure(text=f"{key} ({counts.get(key, 0)})")
        self.count_label.configure(
            text=f"{len(self.providers)} proveedor(es) registrado(s)"
        )

    def _populate_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for provider in self.providers:
            provider_type = provider["provider_type"] or "No Sujeto"
            if self.current_type != "Todos" and provider_type != self.current_type:
                continue
            searchable = " ".join(
                str(provider[field] or "")
                for field in (
                    "reason",
                    "rif_prefix",
                    "rif_number",
                    "conatct_name",
                    "contact_email",
                    "state",
                    "city",
                )
            ).lower()
            if self.search_text and self.search_text not in searchable:
                continue

            rif = "".join(
                part for part in (provider["rif_prefix"], provider["rif_number"]) if part
            )
            values = (
                rif,
                provider["reason"] or "",
                provider_type,
                provider["conatct_name"] or "",
                provider["contact_phone"] or "",
                provider["contact_email"] or "",
                provider["state"] or "",
                provider["city"] or "",
            )
            self.tree.insert(
                "",
                END,
                iid=str(provider["id_provider"]),
                values=values,
                tags=(provider_type.lower(),),
            )

    def _delete_provider(self):
        selection = self.tree.selection()
        if not selection:
            Messagebox.show_warning(
                "Selecciona un proveedor de la tabla.",
                title="Sin selección",
                parent=self,
            )
            return
        provider = self.controller.get_provider(int(selection[0]))
        if provider is None:
            self.refresh()
            return
        confirmed = Messagebox.okcancel(
            f"¿Eliminar el proveedor «{provider['reason']}»?",
            title="Eliminar proveedor",
            alert=True,
            parent=self,
        )
        if confirmed != "OK":
            return
        try:
            self.controller.delete_provider(provider["id_provider"])
        except Exception as error:
            Messagebox.show_error(str(error), title="No se pudo eliminar", parent=self)
            return
        self.refresh()

    def agregar_proveedor(self, master=None):
        self._open_provider_form()

    def ver_proveedor(self):
        selection = self.tree.selection()
        if not selection:
            Messagebox.show_warning(
                "Selecciona un proveedor de la tabla.",
                title="Sin selección",
                parent=self,
            )
            return
        self._open_provider_form(int(selection[0]))

    def _open_provider_form(self, provider_id=None):
        provider = (
            self.controller.get_provider(provider_id)
            if provider_id is not None
            else None
        )
        if provider_id is not None and provider is None:
            self.refresh()
            return

        editing = provider is not None
        title = "Ver / Editar Proveedor" if editing else "Agregar Proveedor"
        dialog = ttk.Toplevel(title=title)
        dialog.geometry("760x600")
        dialog.minsize(680, 540)
        Utils.center_window(dialog)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ttk.Label(
            dialog,
            text=title,
            font=("Helvetica", 16, "bold"),
        ).pack(pady=(14, 8))

        form = ttk.Labelframe(dialog, text="Información del Proveedor", padding=15)
        form.pack(fill="both", expand=True, padx=15, pady=(0, 12))
        form.columnconfigure((0, 1), weight=1, uniform="col")

        self.rif_prefix = ttk.StringVar(
            value=provider["rif_prefix"] if editing else "J"
        )
        self.rif_number = ttk.StringVar(
            value=provider["rif_number"] if editing else ""
        )
        self.reason = ttk.StringVar(value=provider["reason"] if editing else "")
        self.provider_type = ttk.StringVar(
            value=provider["provider_type"] if editing else "Ordinario"
        )
        self.contact_name = ttk.StringVar(
            value=provider["conatct_name"] if editing else ""
        )
        self.contact_phone = ttk.StringVar(
            value=provider["contact_phone"] if editing else ""
        )
        self.contact_email = ttk.StringVar(
            value=provider["contact_email"] if editing else ""
        )
        self.state = ttk.StringVar(value=provider["state"] if editing else "")
        self.city = ttk.StringVar(value=provider["city"] if editing else "")

        rif_frame = ttk.Frame(form)
        rif_frame.grid(row=0, column=0, sticky="ew", padx=(0, 8), pady=5)
        ttk.Label(
            rif_frame,
            text="RIF (Registro de Información Fiscal)",
            font=("Helvetica", 9, "bold"),
        ).pack(anchor="w")
        rif_row = ttk.Frame(rif_frame)
        rif_row.pack(fill=X, pady=(3, 0))
        ttk.Combobox(
            rif_row,
            textvariable=self.rif_prefix,
            values=("V", "J", "E", "G", "C"),
            width=3,
            state="readonly",
        ).pack(side=LEFT, padx=(0, 5))
        ttk.Entry(rif_row, textvariable=self.rif_number).pack(
            side=LEFT, fill=X, expand=True
        )

        reason_frame = ttk.Frame(form)
        reason_frame.grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=5)
        ttk.Label(
            reason_frame,
            text="Razón Social / Nombre Completo",
            font=("Helvetica", 9, "bold"),
        ).pack(anchor="w")
        ttk.Entry(reason_frame, textvariable=self.reason).pack(
            fill=X, pady=(3, 0)
        )

        type_frame = ttk.Frame(form)
        type_frame.grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=5)
        ttk.Label(
            type_frame,
            text="Tipo de Contribuyente (SENIAT)",
            font=("Helvetica", 9, "bold"),
        ).pack(anchor="w")
        ttk.Combobox(
            type_frame,
            textvariable=self.provider_type,
            values=("Ordinario", "Especial", "Formal", "No Sujeto"),
            state="readonly",
        ).pack(fill=X, pady=(3, 0))

        contact_frame = ttk.Frame(form)
        contact_frame.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=5)
        ttk.Label(
            contact_frame,
            text="Persona de Contacto",
            font=("Helvetica", 9, "bold"),
        ).pack(anchor="w")
        ttk.Entry(contact_frame, textvariable=self.contact_name).pack(
            fill=X, pady=(3, 0)
        )

        phone_frame = ttk.Frame(form)
        phone_frame.grid(row=2, column=0, sticky="ew", padx=(0, 8), pady=5)
        ttk.Label(
            phone_frame,
            text="Teléfono",
            font=("Helvetica", 9, "bold"),
        ).pack(anchor="w")
        validator = dialog.register(
           lambda texto: len(texto) <= 20
            and all(c.isdigit() or c in "-+# " for c in texto)
        )
        ttk.Entry(
            phone_frame,
            textvariable=self.contact_phone,
            validate="key",
            validatecommand=(validator, "%P")
            
        ).pack(fill=X, pady=(3, 0))

        email_frame = ttk.Frame(form)
        email_frame.grid(row=2, column=1, sticky="ew", padx=(8, 0), pady=5)
        ttk.Label(
            email_frame,
            text="Correo Electrónico",
            font=("Helvetica", 9, "bold"),
        ).pack(anchor="w")
        ttk.Entry(email_frame, textvariable=self.contact_email).pack(
            fill=X, pady=(3, 0)
        )

        states = (
            "Distrito Capital", "Miranda", "Zulia", "Aragua", "Carabobo", "Lara",
            "Anzoátegui", "Yaracuy", "Bolívar", "Trujillo", "Táchira",
            "Nueva Esparta", "Sucre", "Portuguesa", "Mérida", "Amazonas",
            "Apure", "Barinas", "Cojedes", "Delta Amacuro", "Falcón",
            "Guárico", "Monagas", "La Guaira", "Otros",
        )
        state_frame = ttk.Frame(form)
        state_frame.grid(row=3, column=0, sticky="ew", padx=(0, 8), pady=5)
        ttk.Label(
            state_frame,
            text="Estado / Región",
            font=("Helvetica", 9, "bold"),
        ).pack(anchor="w")
        ttk.Combobox(
            state_frame,
            textvariable=self.state,
            values=states,
            state="readonly",
        ).pack(fill=X, pady=(3, 0))

        city_frame = ttk.Frame(form)
        city_frame.grid(row=3, column=1, sticky="ew", padx=(8, 0), pady=5)
        ttk.Label(
            city_frame,
            text="Ciudad",
            font=("Helvetica", 9, "bold"),
        ).pack(anchor="w")
        ttk.Entry(city_frame, textvariable=self.city).pack(fill=X, pady=(3, 0))

        ttk.Label(
            form,
            text="Dirección Fiscal",
            font=("Helvetica", 9, "bold"),
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(8, 0))
        address = ttk.Text(form, height=3, wrap="word")
        address.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(3, 0))
        if editing and provider["address"]:
            address.insert("1.0", provider["address"])

        actions = ttk.Frame(dialog)
        actions.pack(fill=X, padx=15, pady=(0, 15))
        ttk.Button(
            actions,
            text="Guardar cambios" if editing else "Guardar Proveedor",
            bootstyle="success",
            command=lambda: self._save_provider(dialog, address, provider_id),
        ).pack(side=RIGHT)
        ttk.Button(
            actions,
            text="Cancelar",
            bootstyle="danger-outline",
            command=dialog.destroy,
        ).pack(side=RIGHT, padx=(0, 8))


    def _save_provider(self, dialog, address, provider_id=None):
        provider = {
            "rif_prefix": self.rif_prefix.get().strip(),
            "rif_number": self.rif_number.get().strip(),
            "reason": self.reason.get().strip(),
            "provider_type": self.provider_type.get().strip(),
            "contact_name": self.contact_name.get().strip(),
            "contact_phone": self.contact_phone.get().strip(),
            "contact_email": self.contact_email.get().strip(),
            "state": self.state.get().strip(),
            "city": self.city.get().strip(),
            "address": address.get("1.0", "end-1c").strip(),
        }
        try:
            if provider_id is None:
                self.controller.add_provider(provider)
            else:
                self.controller.update_provider(provider_id, provider)
        except (ValueError, DuplicateProviderError) as error:
            Messagebox.show_warning(str(error), title="Revisa los datos", parent=dialog)
            return
        except Exception as error:
            Messagebox.show_error(
                f"No fue posible guardar el proveedor.\n\n{error}",
                title="No se pudo guardar",
                parent=dialog,
            )
            return

        dialog.destroy()
        self.refresh()

