import flet as ft
import peewee as pw
from datetime import datetime
import io
import subprocess

# Database connection
base_datos = pw.SqliteDatabase("hospital_prueba.db")

# Model
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

# Ensure table exists
base_datos.connect()
base_datos.create_tables([Datos])

def main(page: ft.Page):
    page.title = "PACIENSYS - Gestión de Pacientes"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "auto"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def go_back(e):
        print("Volver atrás")
        subprocess.Popen(["python", "registroOaltas.py"])

    def clear_fields(e):
        paciente_dropdown.value = None
        fecha_input.value = ""
        estado_salud_input.value = ""
        nombre_estudio_input.value = ""
        archivo_input.value = None
        archivo_name.value = "Ningún archivo seleccionado"
        piso_input.value = ""
        habitacion_input.value = ""
        cama_input.value = ""
        area_input.value = ""
        extension_input.value = ""
        page.update()

    def load_patient_data(e):
        selected_curp = paciente_dropdown.value
        if not selected_curp:
            show_snack_bar("Por favor, seleccione un paciente.")
            return

        try:
            patient = Datos.get(Datos.curp_paciente == selected_curp)
            fecha_input.value = patient.fecha or ""
            estado_salud_input.value = patient.estado_salud
            nombre_estudio_input.value = patient.nombre_estudio or ""
            archivo_name.value = "Archivo existente" if patient.archivo_estudio else "Ningún archivo seleccionado"
            piso_input.value = patient.piso or ""
            habitacion_input.value = patient.habitacion or ""
            cama_input.value = patient.cama or ""
            area_input.value = patient.area or ""
            extension_input.value = str(patient.extension) if patient.extension else ""
            page.update()
            show_snack_bar("Datos del paciente cargados.")
        except Datos.DoesNotExist:
            show_snack_bar("Error al cargar los datos del paciente.")

    def submit_data(e):
        selected_curp = paciente_dropdown.value
        if not selected_curp:
            show_snack_bar("Por favor, seleccione un paciente.")
            return

        if not all([estado_salud_input.value, fecha_input.value]):
            show_snack_bar("Por favor, complete todos los campos obligatorios.")
            return

        try:
            with base_datos.atomic():
                patient = Datos.get(Datos.curp_paciente == selected_curp)
                patient.estado_salud = estado_salud_input.value
                patient.fecha = fecha_input.value
                patient.nombre_estudio = nombre_estudio_input.value
                if archivo_input.value:
                    patient.archivo_estudio = archivo_input.value
                patient.piso = piso_input.value
                patient.cama = cama_input.value
                patient.habitacion = habitacion_input.value
                patient.area = area_input.value
                patient.extension = int(extension_input.value) if extension_input.value else None
                patient.save()

            show_snack_bar("Datos del paciente actualizados con éxito.")
            clear_fields(None)
        except Exception as e:
            show_snack_bar(f"Error al procesar los datos del paciente: {str(e)}")

        page.update()

    def show_snack_bar(message):
        snack_bar = ft.SnackBar(content=ft.Text(message))
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]
            with open(file.path, "rb") as f:
                archivo_input.value = f.read()
            archivo_name.value = file.name
        else:
            archivo_input.value = None
            archivo_name.value = "Ningún archivo seleccionado"
        page.update()

    def update_patient_dropdown():
        patients = list(Datos.select())
        paciente_dropdown.options = [
            ft.dropdown.Option(p.curp_paciente, f"{p.nombre_paciente} {p.apellidos_paciente} - {p.curp_paciente}")
            for p in patients
        ]
        page.update()

    # Botón de volver atrás
    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        on_click=go_back,
        icon_color=ft.colors.BLUE_700,
        icon_size=30,
        tooltip="Volver atrás",
    )

    # Dropdown para seleccionar paciente
    paciente_dropdown = ft.Dropdown(
        label="Seleccionar Paciente",
        width=600,
        on_change=load_patient_data
    )

    # Campos de entrada
    fecha_input = ft.TextField(label="Fecha (DD/MM/YYYY)", width=300)
    estado_salud_input = ft.TextField(
        label="Estado de Salud",
        multiline=True,
        min_lines=3,
        max_lines=5,
        width=600,
    )
    nombre_estudio_input = ft.TextField(
        label="Nombre del estudio",
        width=450,
    )

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)

    archivo_input = ft.TextField(visible=False)
    archivo_name = ft.Text("Ningún archivo seleccionado")
    archivo_button = ft.ElevatedButton(
        "Seleccionar archivo",
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=False),
        width=300,
    )

    piso_input = ft.TextField(label="Piso", width=340)
    habitacion_input = ft.TextField(label="Habitación", width=340)
    cama_input = ft.TextField(label="Cama", width=340)
    area_input = ft.TextField(label="Área", width=340)
    extension_input = ft.TextField(label="Extensión", width=340)

    # Botones
    clear_button = ft.ElevatedButton(
        "Borrar",
        on_click=clear_fields,
        style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.RED_400),
        width=300,
        height=50,
    )
    submit_button = ft.ElevatedButton(
        "Guardar",
        on_click=submit_data,
        style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.GREEN),
        width=300,
        height=50,
    )

    # Contenido principal
    main_content = ft.Column([
        ft.Text("Actualizaciones del Paciente", size=60, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_700),
        ft.Container(height=30),
        ft.Card(
            content=ft.Container(
                content=ft.Column([
                    paciente_dropdown,
                    ft.Row([fecha_input], alignment=ft.MainAxisAlignment.START),
                    estado_salud_input,
                ], spacing=20),
                padding=30,
                width=900,
            ),
        ),
        ft.Container(height=20),
        ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Estudio", size=20, weight=ft.FontWeight.BOLD),
                    nombre_estudio_input,
                    ft.Row([archivo_name, archivo_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ], spacing=20),
                padding=30,
                width=900,
            ),
        ),
        ft.Container(height=20),
        ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Ubicación", size=20, weight=ft.FontWeight.BOLD),
                    ft.Row([piso_input, habitacion_input], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([cama_input, area_input], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    extension_input,
                ], spacing=20),
                padding=30,
                width=900,
            ),
        ),
        ft.Container(height=30),
        ft.Row([clear_button, submit_button], alignment=ft.MainAxisAlignment.CENTER, spacing=40),
    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Estructura de la página
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Row([back_button], alignment=ft.MainAxisAlignment.START),
                main_content,
            ]),
            expand=True,
            alignment=ft.alignment.center,
        )
    )

    # Inicializar el dropdown de pacientes
    update_patient_dropdown()

ft.app(target=main, view=ft.AppView.WEB_BROWSER)