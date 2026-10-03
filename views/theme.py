"""
Archivo de tema para la aplicación WENDO
Aqui se establecen los colores y tipografias

"""

# Importar modulos necesarios

COLOR_PRINCIPAL = "#1E3A8A"  # Color principal del tema
COLOR_SECUNDARIO = "#2563EB"  # Color secundario
COLOR_TERCIARIO = "#10B981"  # Color terciario
COLOR_TEXTO = "#64748B"  # Color del texto
COLOR_TITULO = "#1E3A8A"  # Color del título
COLOR_FONDO = "#D3E4FE"  # Color de fondo
CORLOR_CARD = "#FFFFFF"  # Color de los botones

# Tipografías
TIPOGRAFIA_TITULO = "Helvetica, sans-serif"  # Tipografía para títulos
TIPOGRAFIA_TEXTO = "Verdana, sans-serif"  # Tipografía para el texto

import ttkbootstrap as ttk

ttk.Theme(
    name="wendo",
    primary="#1E3A8A", 
    success="#10B981", 
    info="#2563EB",
    warning="#efa31d", 
    danger="#fc3939",
    neutral="#FFFFFF",
    light=dict(background="#D3E4FE", foreground="#17141f"),
    dark=dict(background="#17141f", foreground="#e9ecef"),
).register()