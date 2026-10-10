"""
This is the main module for the Wendo application.
It initializes the application and creates the main window.
Author: Curso CEPAV
"""
import ttkbootstrap as ttk
import views.sidebar as S

class WendoApp():
    def __init__(self, master=None):
        self.title = "Wendo"
        # self.master = master
        # self.pack()
        self.app = ttk.App(title=self.title, size=(800, 600)) 

    def configure(self):
        # Configuración de la ventana principal
        S.Sidebar(master=self.app)

    def apply_theme(self):
        # Configuración de colores y tipografías

        # self.style = app.style
        self.COLOR_PRINCIPAL = "#1E3A8A"  # Color principal del tema
        self.COLOR_SECUNDARIO = "#2563EB"  # Color secundario
        self.COLOR_TERCIARIO = "#10B981"  # Color terciario
        self.COLOR_TEXTO = "#64748B"  # Color del texto
        self.COLOR_TITULO = "#1E3A8A"  # Color del título
        self.COLOR_FONDO = "#D3E4FE"  # Color de fondo
        self.COLOR_CARD = "#FFFFFF"  # Color de los botones

        # Tipografías
        self.TIPOGRAFIA_TITULO = "Helvetica, sans-serif"  # Tipografía para títulos
        self.TIPOGRAFIA_TEXTO = "Verdana, sans-serif"

        self.app.style.configure(
            "TLabel",
            background="#D3E4FE",
            foreground="#17141f",
            font=("Verdana", 12),
        )
        self.app.style.configure(
            "TButton",
            background="#85878B00",
            foreground="white",
            font=("Helvetica", 10, "bold"),
        )
        self.app.style.configure(
            "TFrame",
            background="#D3E4FE",
        )
        ttk.Theme(
            name="wendo",
            primary="#1E3A8A", 
            success="#10B981", 
            info="#2563EB",
            warning="#efa31d", 
            danger="#fc3939",
            neutral="#FFFFFF",
            light=dict(background="#E3ECF9", foreground="#17141f"),
            dark=dict(background="#17141f", foreground="#e9ecef"),
        ).register()

        self.app.style.theme_use("wendo-light")

    def start(self):
        self.configure()
        self.apply_theme()
        self.app.mainloop()

if __name__ == "__main__":
    app = WendoApp()
    app.start()