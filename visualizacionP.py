import flet as ft
import peewee as pw
import sys
import os
import subprocess

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

def main(page: ft.Page):
    page.title = "PACIENSYS - Visualización de Paciente"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    curp = sys.argv[1] if len(sys.argv) > 1 else None
    if not curp:
        print("Error: No se proporcionó CURP")
        sys.exit(1)

    try:
        paciente = Datos.get(Datos.curp_paciente == curp)
    except Datos.DoesNotExist:
        print(f"Error: No se encontró paciente con CURP {curp}")
        sys.exit(1)

    def toggle_sidebar(e):
        sidebar.visible = not sidebar.visible
        page.update()

    def change_view(e):
        selected_view = e.control.text
        if selected_view == "Estado de salud":
            main_content.content = estado_salud_view
        elif selected_view == "Resultados de laboratorio":
            main_content.content = resultados_lab_view
        elif selected_view == "Ubicación":
            main_content.content = ubicacion_view
        page.update()

    def exit_app(e):
        subprocess.Popen(["python", "principal2.py"])
        page.window_destroy()

    def download_file(e):
        if paciente.archivo_estudio:
            file_name = f"{paciente.curp_paciente}_estudio.pdf"
            with open(file_name, "wb") as file:
                file.write(paciente.archivo_estudio)
            page.launch_url(file_name)
        else:
            show_snack_bar("No hay archivo disponible para descargar.")

    def show_snack_bar(message):
        snack_bar = ft.SnackBar(content=ft.Text(message))
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    # Sidebar
    sidebar = ft.Container(
        content=ft.Column([
            ft.Text("Paciente:", weight=ft.FontWeight.BOLD, size=18),
            ft.Text(f"{paciente.nombre_paciente} {paciente.apellidos_paciente}", size=16),
            ft.Text("CURP:", weight=ft.FontWeight.BOLD, size=18),
            ft.Text(paciente.curp_paciente, size=16),
            ft.Divider(),
            ft.ElevatedButton("Salir", on_click=exit_app, icon=ft.icons.EXIT_TO_APP),
        ]),
        width=250,
        padding=20,
        bgcolor=ft.colors.BLUE_50,
        visible=False
    )

    # Barra de navegación superior
    nav_bar = ft.Row(
        [
            ft.TextButton("Estado de salud", on_click=change_view, width=200, height=50),
            ft.TextButton("Resultados de laboratorio", on_click=change_view, width=200, height=50),
            ft.TextButton("Ubicación", on_click=change_view, width=200, height=50),
        ],
        alignment=ft.MainAxisAlignment.END,
    )

    # Vistas de contenido
    estado_salud_view = ft.Container(
        content=ft.Column(
            [
                ft.Text("Estado de Salud", size=25, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_600),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("                                                     Fecha                                                 ", size=22, weight=ft.FontWeight.W_500, color=ft.colors.BLUE_900)),
                        ft.DataColumn(ft.Text("                                                     Estado                                                  ", size=22, weight=ft.FontWeight.W_500, color=ft.colors.BLUE_900)),
                    ],
                    rows=[
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(paciente.fecha or "No especificado", size=20, color=ft.colors.GREY_800)),
                            ft.DataCell(ft.Text(paciente.estado_salud, size=20, color=ft.colors.GREY_800)),
                        ])
                    ],
                    border=ft.border.all(1, ft.colors.GREY_400),
                    divider_thickness=2,
                )
            ],
            spacing=30,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        ),
        expand=True,
        padding=80,
        border_radius=20,
        bgcolor=ft.colors.WHITE,
        shadow=ft.BoxShadow(
            blur_radius=15,
            spread_radius=5,
            color=ft.colors.GREY_300,
            offset=ft.Offset(5, 5)
        )
    )

    resultados_lab_view = ft.Container(
        content=ft.Column(
            [
                ft.Text("Resultados de Laboratorio", size=25, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_600),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("                              Fecha                               ", size=22, color=ft.colors.BLUE_900)),
                        ft.DataColumn(ft.Text("                              Nombre                              ", size=22, color=ft.colors.BLUE_900)),
                        ft.DataColumn(ft.Text("                              Acción                              ", size=22, color=ft.colors.BLUE_900)),
                    ],
                    rows=[
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(paciente.fecha or "No especificado", size=20)),
                            ft.DataCell(ft.Text(paciente.nombre_estudio or "No especificado", size=20)),
                            ft.DataCell(ft.ElevatedButton("Descargar", icon=ft.icons.DOWNLOAD, width=150, height=30, on_click=download_file)),
                        ])
                    ] if paciente.nombre_estudio else [],
                    border=ft.border.all(1, ft.colors.GREY_400),
                    divider_thickness=2,
                )
            ],
            spacing=30,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        ),
        expand=True,
        padding=80,
        border_radius=20,
        bgcolor=ft.colors.WHITE,
        shadow=ft.BoxShadow(
            blur_radius=15,
            spread_radius=5,
            color=ft.colors.GREY_300,
            offset=ft.Offset(5, 5)
        )
    )

    ubicacion_view = ft.Container(
        content=ft.Column(
            [
                ft.Text("Ubicación del Paciente", size=25, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_600),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("                                               Información                                                  ", size=22, color=ft.colors.BLUE_900)),
                        ft.DataColumn(ft.Text("                                               Detalle                                                  ", size=22, color=ft.colors.BLUE_900)),
                    ],
                    rows=[
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("Piso", size=20)),
                            ft.DataCell(ft.Text(paciente.piso or "No especificado")),
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("Habitación", size=20)),
                            ft.DataCell(ft.Text(paciente.habitacion or "No especificado")),
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("Cama", size=20)),
                            ft.DataCell(ft.Text(paciente.cama or "No especificado")),
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("Área", size=20)),
                            ft.DataCell(ft.Text(paciente.area or "No especificado")),
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("Extensión", size=20)),
                            ft.DataCell(ft.Text(str(paciente.extension) if paciente.extension else "No especificado")),
                        ]),
                    ],
                    border=ft.border.all(1, ft.colors.GREY_400),
                    divider_thickness=2,
                )
            ],
            spacing=30,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        ),
        expand=True,
        padding=80,
        border_radius=20,
        bgcolor=ft.colors.WHITE,
        shadow=ft.BoxShadow(
            blur_radius=15,
            spread_radius=5,
            color=ft.colors.GREY_300,
            offset=ft.Offset(5, 5)
        )
    )

    # Contenido principal
    main_content = ft.Container(
        content=estado_salud_view,
        expand=True,
        padding=20,
        alignment=ft.alignment.top_left
    )

    # Estructura principal
    content = ft.Column([
        ft.Row([
            ft.IconButton(ft.icons.MENU, on_click=toggle_sidebar),
            nav_bar,
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Row([
            sidebar,
            ft.VerticalDivider(width=1),
            main_content,
        ], expand=True),
    ], expand=True)

    # Añadir todo a la página
    page.add(content)

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)