import flet as ft
import subprocess

def main(page: ft.Page):
    page.title = "PACIENSYS"
    page.padding = 0
    page.bgcolor = ft.colors.WHITE
    page.theme_mode = ft.ThemeMode.LIGHT

    def open_module(module_name):
        subprocess.Popen(["python", f"{module_name}.py"])

    def nav_item(text, module_name):
        return ft.Container(
            content=ft.Text(
                text,
                color=ft.colors.BLACK,
                weight=ft.FontWeight.W_500,
                size=14,
            ),
            padding=ft.padding.symmetric(horizontal=15, vertical=10),
            border_radius=ft.border_radius.all(5),
            on_click=lambda _: open_module(module_name),
        )

    nav_items = ft.Row(
        [
            nav_item("Hospital", "hospital"),
            ft.VerticalDivider(width=1, color=ft.colors.BLUE_200),
            nav_item("Paciente", "paciente"),
            ft.VerticalDivider(width=1, color=ft.colors.BLUE_200),
            nav_item("Administración", "administrador"),
            ft.VerticalDivider(width=1, color=ft.colors.BLUE_200),
            nav_item("Números de emergencia", "emergencias"),
        ],
        alignment=ft.MainAxisAlignment.END,
    )

    app_bar = ft.AppBar(
        leading=ft.Icon(ft.icons.HEALTH_AND_SAFETY),
        leading_width=40,
        title=ft.Text("PACIENSYS"),
        center_title=False,
        bgcolor=ft.colors.BLUE_50,
        actions=[nav_items],
    )

    main_content = ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "PACIENSYS",
                                size=60,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.BLUE_700,
                            ),
                            ft.Text(
                                "Un sistema integral que ayuda a la gestión de datos de los pacientes",
                                size=20,
                                color=ft.colors.GREY_700,
                                width=400,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    padding=50,
                    alignment=ft.alignment.center_left,
                ),
                ft.VerticalDivider(width=1, color=ft.colors.BLUE_200),
                ft.Container(
                    content=ft.Image(
                        src="hospital_logo.png",
                        width=600,
                        height=600,
                        fit=ft.ImageFit.CONTAIN
                    ),
                    expand=True,
                    alignment=ft.alignment.center,
                ),
            ],
            expand=True,
        ),
        expand=True,
    )

    def resize(e):
        if page.window_width <= 600:
            app_bar.actions = None
            app_bar.title = None
            main_content.content.controls[0].visible = False
            main_content.content.controls[1].visible = False
        else:
            app_bar.actions = [nav_items]
            app_bar.title = ft.Text("PACIENSYS")
            main_content.content.controls[0].visible = True
            main_content.content.controls[1].visible = True
        page.update()

    page.on_resize = resize

    page.add(app_bar, main_content)

ft.app(target=main, view=ft.AppView.WEB_BROWSER)