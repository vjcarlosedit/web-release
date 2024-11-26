import flet as ft
import subprocess
import logging

def main(page: ft.Page):
    # Hardcoded admin credentials
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "paciensys2024"

    # Configuración global de la página
    page.title = "PACIENSYS - Sistema de Gestión Hospitalaria"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.WHITE
    page.padding = 20

    # Título principal del sistema
    titulo = ft.Container(
        content=ft.Text("PACIENSYS", size=60, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_600),
        alignment=ft.alignment.center  # Centra el texto horizontalmente
    )

    subtitulo = ft.Container(
        content=ft.Text("Sistema de Gestión Hospitalaria", size=30, color=ft.colors.GREY_700),
        alignment=ft.alignment.center  # Centra el texto horizontalmente
    )

    # Campos de texto para el inicio de sesión
    username_field = ft.TextField(
        label="Usuario",
        width=300,
        prefix_icon=ft.icons.PERSON,
        border_color=ft.colors.BLUE_400,
        focused_border_color=ft.colors.BLUE_600,
    )
    password_field = ft.TextField(
        label="Contraseña",
        width=300,
        password=True,
        prefix_icon=ft.icons.LOCK,
        border_color=ft.colors.BLUE_400,
        focused_border_color=ft.colors.BLUE_600,
    )

    # Mensaje de error o éxito (inicialmente oculto)
    message = ft.Text(visible=False, size=16)

    def iniciar_sesion(e):
        username = username_field.value
        password = password_field.value

        if not username or not password:
            message.value = "Por favor, complete todos los campos."
            message.color = ft.colors.RED_600
        elif username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            message.value = "Inicio de sesión con éxito"
            message.color = ft.colors.GREEN_600
            # Abrir el submódulo registroOaltas.py
            subprocess.Popen(["python", "registroOaltas.py"])
            page.window_destroy()  # Cerrar la ventana de inicio de sesión
        else:
            message.value = "Credenciales incorrectas. Inténtelo de nuevo."
            message.color = ft.colors.RED_600

        message.visible = True
        page.update()

    def go_back(e):
        logging.info("Función 'Volver atrás' activada")
        subprocess.Popen(["python", "principal2.py"])

    # Botón de inicio de sesión
    login_button = ft.ElevatedButton(
        text="Iniciar Sesión",
        icon=ft.icons.LOGIN,
        width=300,
        on_click=iniciar_sesion,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE_600,
            shape=ft.RoundedRectangleBorder(radius=10),
        )
    )
    # Botón de volver atrás
    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        on_click=go_back,
        icon_color=ft.colors.BLUE_700,
        icon_size=30,
        tooltip="Volver atrás",
    )

    # Cuadro de inicio de sesión
    cuadro_login = ft.Container(
        content=ft.Column(
            [
                ft.Text("Inicio de Sesión", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_600),
                username_field,
                password_field,
                message,
                login_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Centra los elementos horizontalmente
        ),
        width=500,
        padding=30,
        border_radius=25,
        bgcolor=ft.colors.BLUE_50,
        border=ft.border.all(2, ft.colors.BLUE_200),
    )

    # Pie de página
    footer_info = ft.Text("© 2024 Hospital Central. Todos los derechos reservados.", size=12, color=ft.colors.GREY_600)

    # Contenedor principal
    content = ft.Container(
        content=ft.Column(
            [
                titulo,
                subtitulo,
                cuadro_login,
                footer_info
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=40,
            expand=True  # Expande la columna para usar el espacio disponible
        ),
        alignment=ft.alignment.center,
        expand=True  # Expande el contenedor principal para ocupar toda la página
    )

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=back_button,
                        padding=10,
                        alignment=ft.alignment.top_left,
                    ),
                    content,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            expand=True,
            padding=20,
        )
    )

    # Agregar el contenedor a la página
    page.add(content)
    page.update()

ft.app(target=main, view=ft.AppView.WEB_BROWSER)