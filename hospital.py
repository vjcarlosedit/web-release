import flet as ft
import subprocess

def main(page: ft.Page):
    page.title = "PACIENSYS - Información del Hospital"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "auto"

    def exit_app(e):
        # Llamar al subproceso principal2.py
        subprocess.Popen(["python", "principal2.py"])
        page.window_destroy()

    def button_style(color):
        return ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=color,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=10),
        )

    # Información del hospital
    info_hospital = ft.Column([
        ft.Text("Información del Hospital", size=26, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_700),
        ft.Text("CLAVE: TCSSA002003", size=18),
        ft.Text("LOCALIDAD: 0001 - CUNDUACÁN", size=18),
        ft.Text("DESCRIPCION DE LA UNIDAD: HO - UNIDAD DE HOSPITALIZACIÓN", size=18),
        ft.Text("DIRECCION: AVENIDA FIDENCIA FERNANDEZ SASTRE NO. EXT. SIN NÚMERO NO. INT., COL. C.P. (86690)", size=18),
        ft.Text("TELEFONO: 9143360689", size=18),
        ft.Container(height=20),
        ft.Text("Misión", size=26, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_700),
        ft.Text(
            "El Hospital General de Cunduacán tiene como misión brindar servicios de salud integrales, de alta calidad y accesibles, "
            "centrados en la atención y el bienestar del paciente. Nos comprometemos a promover un entorno de cuidado humano y ético, "
            "apoyado por un equipo profesional altamente capacitado, ya fomentar la prevención, el diagnóstico temprano y el tratamiento "
            "eficiente de enfermedades para mejorar la calidad de vida de la comunidad.",
            size=18,
            text_align=ft.TextAlign.JUSTIFY,
        ),
        ft.Container(height=20),
        ft.Text("Visión", size=26, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_700),
        ft.Text(
            "Ser un referente de excelencia en el ámbito de la atención hospitalaria en Cunduacán y la región, distinguiéndonos por "
            "la innovación, la tecnología avanzada y la formación continua de nuestro personal. Aspiramos a liderar programas de salud "
            "sostenibles ya ser reconocidos por nuestro compromiso con la humanización de los servicios de salud y la satisfacción del paciente.",
            size=18,
            text_align=ft.TextAlign.JUSTIFY,
        ),
    ], width=850, scroll=ft.ScrollMode.AUTO)

    # Imagen del hospital
    hospital_image = ft.Image(
        src="hospital2.jpg",
        width=400,
        height=400,
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
        info_hospital,
        ft.VerticalDivider(width=1, color=ft.colors.BLUE_200),
        ft.Column([
            hospital_image,
            ft.Container(height=20),
            exit_button,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
    ], expand=True, alignment=ft.MainAxisAlignment.CENTER)

    # Agregar contenido a la página
    page.add(main_content)
    
ft.app(target=main, view=ft.AppView.WEB_BROWSER)