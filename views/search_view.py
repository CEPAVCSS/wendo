





import ttkbootstrap as ttk


class WendoApp(ttk.Window):

    def __init__(self):
        super().__init__(
            title="Wendo", themename="gruvbox-dark", size=(800, 600)
        )
        self.create_widgets()

    def create_widgets(self):
        main_container = ttk.Frame(self, padding=20)
        main_container.pack(fill="both", expand=True)

        
        search_frame = ttk.Frame(main_container)
        search_frame.pack(fill="x", pady=(0, 15))

        
        lupa_label = ttk.Label(search_frame, text="🔍", font=("Segoe UI", 12))
        lupa_label.pack(side="left", padx=(0, 5))

        
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.search_entry.insert(0, "Escribe para buscar reportes...")
        self.search_entry.bind("<FocusIn>", self.limpiar_placeholder)

        
        search_btn = ttk.Button(
            search_frame,
            text="Buscar",
            bootstyle="outline-neutral",
            command=self.ejecutar_busqueda,
        )
        search_btn.pack(side="left")


    def limpiar_placeholder(self, event):
        if self.search_entry.get() == "Escribe para buscar...":
            self.search_entry.delete(0, "end")

    def ejecutar_busqueda(self):
        texto = self.search_entry.get()
        print(f"Buscando: {texto}")

    def abrir_reportes(self):
        print("Abriendo sección de reportes...")


if __name__ == "__main__":
    app = WendoApp()
    app.mainloop()































