import flet as ft

def main(page: ft.Page):
    page.title = "PACIENSYS - Números de Emergencia"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "auto"

    def exit_app(e):
        page.window_destroy()

    def button_style(color):
        return ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=color,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=10),
        )

    # Números de emergencia
    numeros_emergencia = ft.Column([
        ft.Text("Números de Emergencia", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_700),
        ft.Container(height=20),
        ft.Text("EMERGENCIAS:      911", size=18),
        ft.Text("                   ", size=18),
        ft.Text("CRUZ ROJA:      911", size=18),
        ft.Text("                   ", size=18),
        ft.Text("AMBULANCIAS GEISER:      914 121 72 43", size=18),
        ft.Text("                   ", size=18),
        ft.Text("HOSPITAL GENERAL DE CUNDUACAN:      914 336 06 89", size=18),
        ft.Text("                   ", size=18),
        ft.Text("DIRECCION DE SEGURIDAD PUBLICA MUNICIPAL:      914 33 60288", size=18),
        ft.Text("                   ", size=18),
        ft.Text("INSTITUTO DE PROTECCION CIVIL DEL ESTADO DE TABASCO (IPCET):      3 58 11 25", size=18),
        ft.Text("                   ", size=18),
        ft.Text("BOMBEROS: 3 58 11 25", size=18),
        ft.Text("                   ", size=18),
        ft.Text("SISTEMA ESTATAL DE URGENCIAS DE TABASCO (SEUT):      357 11 11", size=18),
        ft.Text("                   ", size=18),
        ft.Text("COORDINACION DE PROTECCION CIVIL DEL MUNICIPIO DEL CUNDUACAN:      91433 61363", size=18),
    ], width=850, scroll=ft.ScrollMode.AUTO)

    # Imagen de emergencia (asumiendo que tienes una imagen llamada "emergencia.jpg")
    emergencia_image = ft.Image(
        src="emergencia.png",
        width=250,
        height=250,
        fit=ft.ImageFit.CONTAIN,
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

    # Contenido principal
    main_content = ft.Row([
        numeros_emergencia,
        ft.VerticalDivider(width=1, color=ft.colors.BLUE_200),
        ft.Column([
            emergencia_image,
            ft.Container(height=20),
            exit_button,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
    ], expand=True, alignment=ft.MainAxisAlignment.CENTER)

    # Agregar contenido a la página
    page.add(main_content)

ft.app(target=main, view=ft.AppView.WEB_BROWSER)