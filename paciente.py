import flet as ft
import peewee as pw
import subprocess
import logging

# Definir la base de datos SQLite
base_datos = pw.SqliteDatabase("hospital_prueba.db")

# Modelo Datos
class Datos(pw.Model):
    curp_paciente = pw.CharField(primary_key=True, max_length=18)
    nombre_paciente = pw.TextField()
    apellidos_paciente = pw.TextField()
    estado_salud = pw.TextField()
    fecha = pw.TextField(null=True)
    nombre_estudio = pw.TextField(null=True)
    archivo_estudio = pw.BlobField(null=True)
    piso = pw.TextField(null=True)
    cama = pw.TextField(null=True)
    habitacion = pw.TextField(null=True)
    area = pw.TextField(null=True)
    extension = pw.IntegerField(null=True)
    
    class Meta:
        database = base_datos
        table_name = 'datos'

# Asegurar que la tabla existe
base_datos.connect()
base_datos.create_tables([Datos])

def main(page: ft.Page):
    page.title = "PACIENSYS - Sistema de Gestión Hospitalaria"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.WHITE
    page.padding = 20

    titulo = ft.Container(
        content=ft.Text("PACIENSYS", size=60, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_600),
        alignment=ft.alignment.center
    )

    subtitulo = ft.Container(
        content=ft.Text("Sistema de Gestión Hospitalaria", size=30, color=ft.colors.GREY_700),
        alignment=ft.alignment.center
    )

    curp_field = ft.TextField(
        label="Ingresa la CURP del paciente",
        width=300,
        border_color=ft.colors.BLUE_400,
        focused_border_color=ft.colors.BLUE_600,
        prefix_icon=ft.icons.PERSON
    )

    message = ft.Text(visible=False, size=16)

    def iniciar_sesion(e):
        curp = curp_field.value

        if not curp:
            show_message("Por favor, ingrese la CURP del paciente.", ft.colors.RED_600)
        else:
            try:
                paciente = Datos.get(Datos.curp_paciente == curp)
                show_message(f"Inicio de sesión exitoso. Bienvenido, {paciente.nombre_paciente} {paciente.apellidos_paciente}.", ft.colors.GREEN_600)
                # Llamar a visualizacionP.py con la CURP del paciente
                subprocess.Popen(["python", "visualizacionP.py", curp])
                page.window_destroy()  # Cerrar la ventana de inicio de sesión
            except Datos.DoesNotExist:
                show_message("CURP no encontrada. Por favor, verifique e intente nuevamente.", ft.colors.RED_600)
            except Exception as e:
                show_message(f"Error al iniciar sesión: {str(e)}", ft.colors.RED_600)

    def go_back(e):
        logging.info("Función 'Volver atrás' activada")
        subprocess.Popen(["python", "principal2.py"])

    def show_message(text, color):
        message.value = text
        message.color = color
        message.visible = True
        page.update()

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

    login_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Inicio de Sesión", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_600),
                curp_field,
                message,
                login_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        width=500,
        padding=30,
        border_radius=25,
        bgcolor=ft.colors.BLUE_50,
        border=ft.border.all(2, ft.colors.BLUE_200),
    )

    footer_info = ft.Text("© 2024 Hospital Central. Todos los derechos reservados.", size=12, color=ft.colors.GREY_600)

   
    # Botón de volver atrás
    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        on_click=go_back,
        icon_color=ft.colors.BLUE_700,
        icon_size=30,
        tooltip="Volver atrás",
    )

    main_content = ft.Column([
        titulo,
        subtitulo,
        ft.Container(height=40),
        login_container,
        ft.Container(height=20),
        footer_info
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)

    # Estructura de la página
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=back_button,
                        padding=10,
                        alignment=ft.alignment.top_left,
                    ),
                    main_content,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            expand=True,
            padding=20,
        )
    )

    page.add(main_content)
    page.update()

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)