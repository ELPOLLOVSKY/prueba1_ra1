import os
import re

# Carpeta donde se guardan los archivos
CARPETA_DATOS = "datos"

# Crear la carpeta si no existe
if not os.path.exists(CARPETA_DATOS):
    os.makedirs(CARPETA_DATOS)

def validar_ip(ip):
    patron = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
                        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    return patron.match(ip)

def mostrar_menu():
    print("\nMenú:")
    print("1. Ver dispositivos")
    print("2. Ver campus")
    print("3. Añadir dispositivo")
    print("4. Añadir campus")
    print("5. Salir")

def cargar_campus():
    archivos = os.listdir(CARPETA_DATOS)
    campus = [archivo[:-4] for archivo in archivos if archivo.endswith(".txt")]
    return campus

def ver_dispositivos(campus):
    if not campus:
        print("No hay campus registrados.")
        return
    for i, c in enumerate(campus):
        print(f"{i+1}. {c}")
    try:
        opcion = int(input("Seleccione un campus: ")) - 1
        if 0 <= opcion < len(campus):
            archivo = os.path.join(CARPETA_DATOS, f"{campus[opcion]}.txt")
            if os.path.exists(archivo):
                with open(archivo, "r") as f:
                    contenido = f.read().strip()
                    if contenido:
                        print("\nDispositivos registrados:")
                        print(contenido)
                    else:
                        print("No hay dispositivos registrados aún.")
            else:
                print("Archivo del campus no encontrado.")
        else:
            print("Opción fuera de rango.")
    except ValueError:
        print("Entrada inválida.")

def ver_campus(campus):
    if not campus:
        print("No hay campus registrados.")
        return
    print("\nCampus registrados:")
    for i, c in enumerate(campus):
        print(f"{i+1}. {c}")

def añadir_dispositivo(campus):
    if not campus:
        print("No hay campus disponibles. Cree uno primero.")
        return
    for i, c in enumerate(campus):
        print(f"{i+1}. {c}")
    try:
        opcion = int(input("Seleccione un campus: ")) - 1
        if 0 <= opcion < len(campus):
            dispositivo = input("Tipo de dispositivo (Router/Switch/Switch Multicapa): ").strip()
            nombre = input("Nombre del dispositivo: ").strip()

            while True:
                direccion_ip = input("Dirección IP (formato xxx.xxx.xxx.xxx): ").strip()
                if validar_ip(direccion_ip):
                    break
                else:
                    print("IP no válida. Intente nuevamente.")

            vlans = input("VLAN(s) (separadas por coma): ").strip()
            servicios = input("Servicios (Datos, VLAN, Trunking, Enrutamiento): ").strip()
            capa = input("Capa (Núcleo, Distribución, Acceso): ").strip()

            archivo = os.path.join(CARPETA_DATOS, f"{campus[opcion]}.txt")
            with open(archivo, "a") as f:
                f.write("\n-----------------------------\n")
                f.write(f"Dispositivo: {dispositivo}\n")
                f.write(f"Nombre: {nombre}\n")
                f.write(f"IP: {direccion_ip}\n")
                f.write(f"VLAN(s): {vlans}\n")
                f.write(f"Servicios: {servicios}\n")
                f.write(f"Capa: {capa}\n")
                f.write("-----------------------------\n")
            print("Dispositivo agregado correctamente.")
        else:
            print("Selección fuera de rango.")
    except ValueError:
        print("Entrada inválida.")

def añadir_campus(campus):
    nuevo = input("Nombre del nuevo campus: ").strip().replace(" ", "_")
    if nuevo in campus:
        print("El campus ya existe.")
        return
    archivo = os.path.join(CARPETA_DATOS, f"{nuevo}.txt")
    try:
        with open(archivo, "w") as f:
            f.write(f"# Archivo de campus: {nuevo}\n")
        print(f"Campus '{nuevo}' creado correctamente.")
    except Exception as e:
        print(f"Ocurrió un error al crear el archivo: {e}")

def main():
    while True:
        campus = cargar_campus()
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            ver_dispositivos(campus)
        elif opcion == "2":
            ver_campus(campus)
        elif opcion == "3":
            añadir_dispositivo(campus)
        elif opcion == "4":
            añadir_campus(campus)
        elif opcion == "5":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
