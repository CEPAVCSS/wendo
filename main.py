import ttkbootstrap as ttk

app = ttk.App(title="Wendo", theme="bootstrap-light", size=(400, 300))
ttk.Button(app, text="Hello", bootstyle="success").pack(padx=20, pady=20)
app.mainloop()



