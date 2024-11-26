import flet as ft
import peewee as pw
import logging
from datetime import date
import subprocess

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Definir la base de datos SQLite
base_datos = pw.SqliteDatabase("hospital_prueba.db")

# Modelo Datos
class Datos(pw.Model):
    curp_paciente = pw.CharField(primary_key=True, max_length=18)
    nombre_paciente = pw.TextField()
    apellidos_paciente = pw.TextField()
    estado_salud = pw.TextField()
    
    class Meta:
        database = base_datos
        table_name = 'datos'

# Conectar a la base de datos y crear tablas
try:
    base_datos.connect()
    base_datos.create_tables([Datos])
    logging.info("Conexión a la base de datos hospital_prueba.db establecida y tabla creada con éxito.")
except Exception as e:
    logging.error(f"Error al conectar a la base de datos o crear tabla: {e}")

def main(page: ft.Page):
    page.title = "PACIENSYS - Registro de Paciente"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER


    def go_back(e):
        logging.info("Función 'Volver atrás' activada")
        subprocess.Popen(["python", "registroOaltas.py"])


    def clear_fields(e):
        nombre_input.value = ""
        apellidos_input.value = ""
        curp_input.value = ""
        page.update()

    def register_patient(e):
        nombre = nombre_input.value
        apellidos = apellidos_input.value
        curp = curp_input.value

        if not nombre or not apellidos or not curp:
            show_snack_bar("Por favor, complete todos los campos.")
            return

        try:
            with base_datos.atomic():
                Datos.create(
                    curp_paciente=curp,
                    nombre_paciente=nombre,
                    apellidos_paciente=apellidos,
                    estado_salud="No especificado"  # Valor por defecto
                )
            
            # Verificar si el paciente se guardó correctamente
            paciente = Datos.get_or_none(Datos.curp_paciente == curp)
            if paciente:
                logging.info(f"Paciente guardado: {paciente.nombre_paciente} {paciente.apellidos_paciente}")
                show_snack_bar("Paciente registrado con éxito.")
                clear_fields(None)
            else:
                logging.error("El paciente no se guardó correctamente.")
                show_snack_bar("Error: No se pudo guardar el paciente.")

        except pw.IntegrityError:
            logging.error(f"Error de integridad: La CURP {curp} ya existe en la base de datos.")
            show_snack_bar("Error: La CURP ya existe en la base de datos.")
        except Exception as e:
            logging.error(f"Error al registrar el paciente: {str(e)}")
            show_snack_bar(f"Error al registrar el paciente: {str(e)}")

    def show_snack_bar(message):
        snack_bar = ft.SnackBar(content=ft.Text(message))
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    # Título
    title = ft.Text("Registro de Paciente", size=60, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_700)

    # Campos de entrada
    nombre_input = ft.TextField(
        label="Nombre del Paciente",
        width=500,
        height=90,
        text_size=28,
        border_color=ft.colors.BLUE_400,
        focused_border_color=ft.colors.BLUE_700,
    )
    apellidos_input = ft.TextField(
        label="Apellidos del Paciente",
        width=500,
        height=90,
        text_size=28,
        border_color=ft.colors.BLUE_400,
        focused_border_color=ft.colors.BLUE_700,
    )
    curp_input = ft.TextField(
        label="CURP",
        width=500,
        height=90,
        text_size=28,
        border_color=ft.colors.BLUE_400,
        focused_border_color=ft.colors.BLUE_700,
    )

    # Botones
    clear_button = ft.ElevatedButton(
        "Borrar",
        on_click=clear_fields,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.RED_400,
            padding=ft.padding.all(20),
        ),
        width=180,
        height=50,
    )
    register_button = ft.ElevatedButton(
        "Registrar",
        on_click=register_patient,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.GREEN,
            padding=ft.padding.all(20),
        ),
        width=180,
        height=50,
    )

    # Botón de volver atrás
    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        on_click=go_back,
        icon_color=ft.colors.BLUE_700,
        icon_size=30,
        tooltip="Volver atrás",
    )

    # Contenido principal
    main_content = ft.Column(
        [
            title,
            ft.Container(height=30),
            nombre_input,
            ft.Container(height=20),
            apellidos_input,
            ft.Container(height=20),
            curp_input,
            ft.Container(height=30),
            ft.Row(
                [clear_button, register_button],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=40,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

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

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
    base_datos.close()