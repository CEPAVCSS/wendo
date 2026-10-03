"""
This is the main module for the Wendo application.
It initializes the application and creates the main window.
Author: Curso CEPAV
"""
import ttkbootstrap as ttk
import views.theme as T
import views.sidebar as sidebar

class WendoApp(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master, padding=10, bootstyle="@card")
        # self.master = master
        # self.pack()


app = ttk.App(
        title="Wendo", 
        theme="wendo-light", 
        size=(600, 400)
    )
WendoApp(master=app).pack(fill="both", expand=True)

sidebar = sidebar.Sidebar(master=app)
sidebar.pack(side="left", fill="y")

app.mainloop()