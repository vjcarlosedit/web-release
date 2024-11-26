import flet as ft
import subprocess

def main(page: ft.Page):
    page.title = "PACIENSYS - Menú Principal"
    page.padding = 50
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def button_style(color):
        return ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=color,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=10),
        )

    def handle_registro_click(e):
        subprocess.Popen(["python", "registroP.py"])

    def handle_altas_click(e):
        subprocess.Popen(["python", "altas.py"])

    def exit_app(e):
        subprocess.Popen(["python", "principal2.py"])
        page.window_destroy()

    # Título PACIENSYS
    title = ft.Text("PACIENSYS", size=60, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_700)
    title2 = ft.Text("                        ", size=40)

    # Botones principales
    registro_button = ft.ElevatedButton(
        text="Registro",
        on_click=handle_registro_click,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.GREEN,
            text_style=ft.TextStyle(
                size=35  # Tamaño de la fuente ajustado
            ),
            shape=ft.RoundedRectangleBorder(radius=10)  # Forma cuadrada sin bordes redondeados
        ),
        width=400,
        height=200,
    )

    altas_button = ft.ElevatedButton(
        text="Altas",
        on_click=handle_altas_click,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.BLUE,
            text_style=ft.TextStyle(
                size=35  # Tamaño de la fuente ajustado
            ),
            shape=ft.RoundedRectangleBorder(radius=10)  # Forma cuadrada sin bordes redondeados
        ),
        width=400,
        height=200,
    )

    # Botón de salir
    exit_button = ft.ElevatedButton(
        "Salir",
        on_click=exit_app,
        icon=ft.icons.EXIT_TO_APP,
        style=button_style(ft.colors.RED_400),
        width=150,
        height=50,
    )

    # Contenedor principal
    main_content = ft.Column(
        [
            title,
            title2,
            ft.Row(
                [registro_button, altas_button],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=40,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=50,
    )

    # Estructura de la página
    page.add(
        ft.Column(
            [
                main_content,
                exit_button,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=50,
            expand=True,
        )
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER)