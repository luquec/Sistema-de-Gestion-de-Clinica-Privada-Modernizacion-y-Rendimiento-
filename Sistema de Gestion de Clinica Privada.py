from collections import deque
from datetime import datetime
import random
import time
import tracemalloc
import matplotlib.pyplot as plt


#===============================================================================================================================

#                                  Carga de Archivos con Base de Datos

#===============================================================================================================================
#Se utiliza una lista de diccionarios para la carga inicial

def cargarPacientes(archivo = "pacientes_500.txt"):
    lista_pacientes = []
    with open(archivo, "r", encoding="utf-8") as archivo_abierto:
        next(archivo_abierto) #Omitir el txt

        for linea in archivo_abierto:
            linea = linea.strip().split("|")

            edadNum = int(linea[2])
            prioridadNum = int(linea[4])

            paciente = {
                "cedula" : linea[0],
                "nombre": linea[1],
                "edad" : edadNum,
                "fecha" : linea[3],
                "prioridad" : prioridadNum,
                "tipoSangre" : linea[5],
                }
            lista_pacientes.append(paciente)

        return lista_pacientes


def cargarDiagnosticos():
    lista_diagnosticos = []
    with open("diagnosticos_base.txt", "r") as archivo_abierto:
        next(archivo_abierto)

        for linea in archivo_abierto:
            linea = linea.strip().split("|")

            diagnostico = {
                "codigo": linea[0],
                "area_medica": linea[1],
                "especialidad": linea[2],
                "diagnostico_especifico": linea[3],
            }
            lista_diagnosticos.append(diagnostico)

        return lista_diagnosticos

def cargarConsultas(archivo = "consultas_500.txt"):
    lista_consultas = []
    with open(archivo, "r") as archivo_abierto:
        next(archivo_abierto)

        for linea in archivo_abierto:
            linea = linea.strip().split("|")

            IDNum = int(linea[0])
            gravedadNum = int(linea[4])

            consulta= {
                "ID" : IDNum,
                "cedula": linea[1],
                "fecha" : linea[2],
                "diagnostico" : linea[3],
                "gravedad" : gravedadNum
                }
            lista_consultas.append(consulta)

        return lista_consultas

#Carga inicial de datos desordenados en memoria RAM
base_pacientes = cargarPacientes()
base_consultas = cargarConsultas()
base_diagnosticos = cargarDiagnosticos()



#===============================================================================================================================

#                                  Modulo 1 - Estructura de Atencion (cola con prioridad)

#===============================================================================================================================

def colaPrioridad(lista_pacientes):
    sala_de_espera = []

    while True:
        print("\n", "=" * 45)
        print("        Sala de Espera en Tiempo Real        ")
        print("="*45)

        if sala_de_espera:
            siguiente = sala_de_espera[0]
            print("Siguiente paciente en ser atendido:\n[",siguiente["prioridad"],"] ",siguiente["nombre"],"(Cédula: ", siguiente["cedula"],") - Registro:",siguiente["fecha"])
        else:
            print("Siguiente paciente en ser atendido:\nNo hay pacientes en la sala de espera.\n")

        print("-"*45)
        print("Pacientes actualmente en espera:")
        if len(sala_de_espera) <= 1:
            print("No hay nadie en la fila.\n")
        else:
            for indice,paciente in enumerate(sala_de_espera[1:]):
                print((indice+1),".[",paciente["prioridad"],"]",paciente["nombre"],"- Registro:",paciente["fecha"])

        print("-"*45)
        print("Seleccione una opción:")
        print("1. Simular llegada de paciente aleatorio (Insertar en la cola)")
        print("2. Registrar atención del siguiente paciente (Sacar de de cola)")
        print("3. Salir al menú principal")


        opcion = input("Opción (1-3): ")

        if opcion == "1":

            #Cronometros de tiempo y memoria RAM
            tracemalloc.start() #Medir memoria RAM
            tiempo_inicio = time.perf_counter() #Medir precision del tiempo

            #Escoje un paciente random, agrega a la sala y ordena por prioridad/fecha
            pacienteRandom = random.choice(lista_pacientes)
            sala_de_espera.append(pacienteRandom)
            sala_de_espera.sort(key=lambda p: (p["prioridad"], p["fecha"]))

            #Detener cronometros
            memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            tiempo_fin = time.perf_counter()

            #Calcular
            duracion = tiempo_fin - tiempo_inicio
            memoria_kb = memoria_pico / 1024 #bytes a kilobytes

            print("\nPaciente",pacienteRandom["nombre"],"ingresó a la sala.")
            print("\nDuración de la actividad: ", duracion, " segundos.")
            print("Consumo de memoria: ", memoria_kb, " KB.")


        elif opcion == "2":

            if not sala_de_espera:
                print("No hay pacientes en la sala de espera.")
                continue

            tracemalloc.start()
            tiempo_inicio = time.perf_counter()

            paciente_atendido = sala_de_espera.pop(0)

            memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            tiempo_fin = time.perf_counter()

            duracion = tiempo_fin - tiempo_inicio
            memoria_kb = memoria_pico / 1024 #bytes a kilobytes

            print("\nAtendiendo a paciente",paciente_atendido["nombre"],"...")
            print("\nDuración de la actividad: ",duracion, "segundos.")
            print("Consumo de memoria: ",memoria_kb, "KB.")

        elif opcion == "3":
            print("\nRegresando al menú principal...")
            break

        else:
            print("\nOpcion no es válida.")




#===============================================================================================================================

#                                  Módulo 2 — Expedientes y búsquedas

#===============================================================================================================================
#Comparativa entre la Busqueda Lineal y Binaria (necesita que los datos esten ordenados)

def BusquedaCedulaLineal(cedula):
    consultas = []

    for consulta in base_consultas:
        if cedula == consulta["cedula"]:
            consultas.append(consulta)

    if consultas == []:
        return []
    return consultas


def BusquedaCedulaBinaria(cedula):

    base_consultas_ordenadas = sorted(
        base_consultas,
        key=lambda x: int(x["cedula"].replace("-", "")))

    cedula_numerica = int(cedula.replace("-", ""))
    consultas = []

    izquierda = 0
    derecha = len(base_consultas_ordenadas) - 1  # Última posición de la lista

    #Division de mitades
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2  # Posición del medio
        medio_num = int(base_consultas_ordenadas[medio]["cedula"].replace("-", ""))  # Cédula del medio

        if medio_num == cedula_numerica:
            consultas.append(base_consultas_ordenadas[medio])
            del base_consultas_ordenadas[medio]
            derecha -= 1

        elif medio_num < cedula_numerica:
            # La cédula buscada es MÁS GRANDE, busca en la mitad derecha
            izquierda = medio + 1
        else:
            # La cédula buscada es MÁS PEQUEÑA, busca en la mitad izquierda
            derecha = medio - 1

    if consultas == []:
        return []
    return consultas


def BusquedaFechaLineal(fecha_inicio, fecha_fin):
    consultas = []

    for consulta in base_consultas:
        if fecha_inicio <= consulta["fecha"] <= fecha_fin:
            consultas.append(consulta)

    if consultas == []:
        return []
    return consultas


def BusquedaFechaBinaria(fecha_inicio, fecha_fin):
    base_consultas_ordenadas = sorted(base_consultas, key=lambda x: x["fecha"])
    total = len(base_consultas_ordenadas)

    # Búsqueda binaria del límite izquierdo (primera fecha >= fecha_inicio)
    izquierda = 0
    derecha = total - 1
    primer_indice = total  # si no se encuentra nada, queda fuera de rango

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2

        if base_consultas_ordenadas[medio]["fecha"] >= fecha_inicio:
            primer_indice = medio
            derecha = medio - 1
        else:
            izquierda = medio + 1

    # Búsqueda binaria del límite derecho (última fecha <= fecha_fin)
    izquierda = 0
    derecha = total - 1
    ultimo_indice = -1  # si no se encuentra nada, queda fuera de rango

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2

        if base_consultas_ordenadas[medio]["fecha"] <= fecha_fin:
            ultimo_indice = medio
            izquierda = medio + 1
        else:
            derecha = medio - 1

    if primer_indice > ultimo_indice:
        return []

    return base_consultas_ordenadas[primer_indice:ultimo_indice + 1]


def BusquedaGravedadLineal(gravedad):
    consultas = []

    for consulta in base_consultas:

        if gravedad == consulta["gravedad"]:
            consultas.append(consulta)

    if consultas == []:
        return []

    return consultas


def BusquedaGravedadBinaria(gravedad):
    consultas = []

    base_consultas_ordenadas = sorted(base_consultas, key=lambda x: x["gravedad"])

    izquierda = 0
    derecha = len(base_consultas_ordenadas) - 1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        medio_grav = base_consultas_ordenadas[medio]["gravedad"]

        if medio_grav == gravedad:

            consultas.append(base_consultas_ordenadas[medio])
            del base_consultas_ordenadas[medio]

            derecha -= 1

        elif medio_grav < gravedad:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    if consultas == []:
        return []

    return consultas

#--------------------------------------------------------------------------
#                      SubMenu Consultas - Modulo 2
#--------------------------------------------------------------------------


def ExpedientesBusqueda():

    while True:

        print("\n", "=" * 45)
        print("        Busqueda de Expedientes       ")
        print("="*45)
        print("Seleccione una opción:")
        print("1. Buscar consultas por cédula exacta de paciente (lineal)")
        print("2. Buscar consultas por cédula exacta de paciente (binaria)")
        print("3. Buscar consultas por nombre de paciente (lineal)")
        print("4. Buscar consultas por nombre de paciente (binaria)")
        print("5. Buscar consultas por rango de fechas (lineal)")
        print("6. Buscar consultas por rango de fechas (binaria)")
        print("7. Buscar consultas por nivel de gravedad (lineal)")
        print("8. Buscar consultas por nivel de gravedad (binaria)")
        print("9. Salir al menú principal")

        try:
            opcion = int(input("Opcion: "))
        except:
            print("Error: Opcion invalida.")
            continue

        match opcion:

            case 1:
                    #Cronometros de tiempo y memoria RAM
                tracemalloc.start()
                tiempo_inicio = time.perf_counter()

                cedula = str(input(("\nDigite la cedula completa del paciente con guiones:")))
                consultas = BusquedaCedulaLineal(cedula)

                if consultas == []:
                    print(f"No se encontraron consultas con la cedula {cedula}.\n")
                    break
                print(f"\nConsultas de la cedula: {cedula}\n")

                for consulta in consultas:
                    print(consulta)

                    #Detener cronometros
                    memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    tiempo_fin = time.perf_counter()

                    #Calcular
                    duracion = tiempo_fin - tiempo_inicio
                    memoria_kb = memoria_pico / 1024 #bytes a kilobytes

                    print("\nDuración de la actividad: ", duracion, " segundos.")
                    print("Consumo de memoria: ", memoria_kb, " KB.")


            case 2:

                #Cronometros de tiempo y memoria RAM
                tracemalloc.start()
                tiempo_inicio = time.perf_counter()

                consultas = []

                cedula = str(input(("Digite la cedula completa con guiones:")))

                consultas = BusquedaCedulaBinaria(cedula)

                if consultas == []:
                    print(f"No se encontraron consultas con la cedula {cedula}.\n")
                    break

                print(f"\nConsultas de la cedula: {cedula}\n")
                for consulta in consultas:
            
                    print(consulta)

                #Detener cronometros
                memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                tiempo_fin = time.perf_counter()

                #Calcular
                duracion = tiempo_fin - tiempo_inicio
                memoria_kb = memoria_pico / 1024 #bytes a kilobytes

                print("\nDuración de la actividad: ", duracion, " segundos.")
                print("Consumo de memoria: ", memoria_kb, " KB.")

                break


            case 3:

                    #Cronometros de tiempo y memoria RAM
                tracemalloc.start()
                tiempo_inicio = time.perf_counter()

                pacientes = []

                nombre = str(input("\nEscriba el nombre del paciente: "))

                for paciente in base_pacientes:

                    if nombre.lower() in paciente["nombre"].lower():

                        pacientes.append(paciente)

                if pacientes == []:

                    print(f"No se encontro un paciente con un nombre semejante a {nombre}.\n")
                    break

                consultas = []

                for paciente in pacientes:

                    coincidencias = BusquedaCedulaLineal(paciente["cedula"])
                    consultas += coincidencias

                if consultas == []:

                    print(f"No se encontraron consultas de {nombre}.\n")
                    break

                for consulta in consultas:
                    print(consulta)

                    #Detener cronometros
                memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                tiempo_fin = time.perf_counter()

                #Calcular
                duracion = tiempo_fin - tiempo_inicio
                memoria_kb = memoria_pico / 1024 #bytes a kilobytes

                print("\nDuración de la actividad: ", duracion, " segundos.")
                print("Consumo de memoria: ", memoria_kb, " KB.")



            case 4:

                #Cronometros de tiempo y memoria RAM
                tracemalloc.start()
                tiempo_inicio = time.perf_counter()

                pacientes = []
                pacientes_ordenados = sorted(
                base_pacientes, 
                key=lambda x: x["nombre"])
                

                nombre = str(input("\nEscriba el nombre del paciente: ")).lower()

                izquierda = 0
                derecha = len(pacientes_ordenados) - 1  
                
                while izquierda <= derecha:
                    medio = (izquierda + derecha) // 2  
                    medio_nom = pacientes_ordenados[medio]["nombre"].lower()  
                    
                    if medio_nom == nombre:
            
                        pacientes.append(pacientes_ordenados[medio])
                        del pacientes_ordenados[medio]
            
                        derecha -= 1
            
                    elif medio_nom < nombre:
                        izquierda = medio + 1
                    else:
                        derecha = medio - 1
            
            
                if pacientes == []:

                    print(f"No se encontro un paciente con un nombre semejante a {nombre}.\n")
                    break

                consultas = []

                for paciente in pacientes:

                    coincidencias = BusquedaCedulaBinaria(paciente["cedula"])
                    consultas += coincidencias

                if consultas == []:

                    print(f"No se encontraron consultas de {nombre}.\n")
                    break

                for consulta in consultas:
                    print(consulta)

                    #Detener cronometros
                memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                tiempo_fin = time.perf_counter()

                #Calcular
                duracion = tiempo_fin - tiempo_inicio
                memoria_kb = memoria_pico / 1024 #bytes a kilobytes

                print("\nDuración de la actividad: ", duracion, " segundos.")
                print("Consumo de memoria: ", memoria_kb, " KB.")

            case 5:
 
                #Cronometros de tiempo y memoria RAM
                tracemalloc.start()
                tiempo_inicio = time.perf_counter()

                while True:

                    fecha_inicio = str(input("\nDigite la fecha inicial (YYYY-MM-DD): ")).strip()
                    fecha_fin = str(input("Digite la fecha final (YYYY-MM-DD): ")).strip()

                    try:
                        datetime.strptime(fecha_inicio, "%Y-%m-%d")
                        datetime.strptime(fecha_fin, "%Y-%m-%d")
                        break

                    except ValueError as e:
                        print("Fecha invalida. Use el formato YYYY-MM-DD (ej: 2024-06-28).\n")
        
                
 
                consultas = BusquedaFechaLineal(fecha_inicio, fecha_fin)
 
                if consultas == []:
                    print(f"No se encontraron consultas entre {fecha_inicio} y {fecha_fin}.\n")
                    break
 
                print(f"\nConsultas entre {fecha_inicio} y {fecha_fin}:\n")
 
                for consulta in consultas:
                    print(consulta)
 
                #Detener cronometros
                memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                tiempo_fin = time.perf_counter()
 
                #Calcular
                duracion = tiempo_fin - tiempo_inicio
                memoria_kb = memoria_pico / 1024 #bytes a kilobytes
 
                print("\nDuración de la actividad: ", duracion, " segundos.")
                print("Consumo de memoria: ", memoria_kb, " KB.")
 
                
 
 
            case 6:
 
                #Cronometros de tiempo y memoria RAM
                tracemalloc.start()
                tiempo_inicio = time.perf_counter()
 
                while True:
                
                    fecha_inicio = str(input("\nDigite la fecha inicial (YYYY-MM-DD): ")).strip()
                    fecha_fin = str(input("Digite la fecha final (YYYY-MM-DD): ")).strip()

                    try:
                        datetime.strptime(fecha_inicio, "%Y-%m-%d")
                        datetime.strptime(fecha_fin, "%Y-%m-%d")
                        break

                    except ValueError as e:
                        print("Fecha invalida. Use el formato YYYY-MM-DD (ej: 2024-06-28).\n")
 
                consultas = BusquedaFechaBinaria(fecha_inicio, fecha_fin)
 
                if consultas == []:
                    print(f"No se encontraron consultas entre {fecha_inicio} y {fecha_fin}.\n")
                    break
 
                print(f"\nConsultas entre {fecha_inicio} y {fecha_fin}:\n")
 
                for consulta in consultas:
                    print(consulta)
 
                #Detener cronometros
                memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                tiempo_fin = time.perf_counter()
 
                #Calcular
                duracion = tiempo_fin - tiempo_inicio
                memoria_kb = memoria_pico / 1024 #bytes a kilobytes
 
                print("\nDuración de la actividad: ", duracion, " segundos.")
                print("Consumo de memoria: ", memoria_kb, " KB.")
 
                
 
 
            case 7:
 
                #Cronometros de tiempo y memoria RAM
                tracemalloc.start()
                tiempo_inicio = time.perf_counter()
 
                try:
                    gravedad = int(input("\nDigite el nivel de gravedad (1-3): "))
                except:
                    print("Nivel de gravedad invalido.\n")
                    break
 
                consultas = BusquedaGravedadLineal(gravedad)
 
                if consultas == []:
                    print(f"No se encontraron consultas con gravedad {gravedad}.\n")
                    break
 
                print(f"\nConsultas con gravedad {gravedad}:\n")
 
                for consulta in consultas:
                    print(consulta)
 
                #Detener cronometros
                memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                tiempo_fin = time.perf_counter()
 
                #Calcular
                duracion = tiempo_fin - tiempo_inicio
                memoria_kb = memoria_pico / 1024 #bytes a kilobytes
 
                print("\nDuración de la actividad: ", duracion, " segundos.")
                print("Consumo de memoria: ", memoria_kb, " KB.")
 
                
 
 
            case 8:
 
                #Cronometros de tiempo y memoria RAM
                tracemalloc.start()
                tiempo_inicio = time.perf_counter()
 
                try:
                    gravedad = int(input("\nDigite el nivel de gravedad (1-3): "))
                except:
                    print("Nivel de gravedad invalido.\n")
                    break
 
                consultas = BusquedaGravedadBinaria(gravedad)
 
                if consultas == []:
                    print(f"No se encontraron consultas con gravedad {gravedad}.\n")
                    break
 
                print(f"\nConsultas con gravedad {gravedad}:\n")
 
                for consulta in consultas:
                    print(consulta)
 
                #Detener cronometros
                memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                tiempo_fin = time.perf_counter()
 
                #Calcular
                duracion = tiempo_fin - tiempo_inicio
                memoria_kb = memoria_pico / 1024 #bytes a kilobytes
 
                print("\nDuración de la actividad: ", duracion, " segundos.")
                print("Consumo de memoria: ", memoria_kb, " KB.")
 

            case 9:
                print("\nRegresando al menú principal...")
                break
 
            case _:
                print("\nOpcion no es válida.")



#===============================================================================================================================

#                                  Módulo 3 — Árbol de diagnósticos

#===============================================================================================================================


def cargarDiagnosticosArbol(archivo="diagnosticos_base.txt"):
    arbol_diagnosticos = []

    with open(archivo, "r", encoding="utf-8") as f:
        next(f)

        for linea in f:
            linea = linea.strip().split("|")

            codigo = linea[0]
            area = linea[1]
            especialidad = linea[2]
            diagnostico = linea[3]

            area_existente = None
            for a in arbol_diagnosticos:
                if a["area"] == area:
                    area_existente = a
                    break

            if not area_existente:
                area_existente = {"area": area, "especialidades": []}
                arbol_diagnosticos.append(area_existente)

            especialidad_existente = None
            for e in area_existente["especialidades"]:
                if e["nombre"] == especialidad:
                    especialidad_existente = e
                    break

            if not especialidad_existente:
                especialidad_existente = {"nombre": especialidad, "diagnosticos": []}
                area_existente["especialidades"].append(especialidad_existente)

            especialidad_existente["diagnosticos"].append({
                "codigo": codigo,
                "nombre": diagnostico
            })

    return arbol_diagnosticos


base_diagnosticos_arbol = cargarDiagnosticosArbol()


def buscarDiagnosticos(nombre_o_codigo, base_diagnosticos_arbol):
    resultados = []
    for area in base_diagnosticos_arbol:
        for esp in area["especialidades"]:
            for diag in esp["diagnosticos"]:
                if nombre_o_codigo.lower() in diag["nombre"].lower() or nombre_o_codigo.upper() == diag["codigo"]:
                    resultados.append({
                        "area": area["area"],
                        "especialidad": esp["nombre"],
                        "codigo": diag["codigo"],
                        "nombre": diag["nombre"]
                    })
    return resultados

def mostrar_diagnosticos_especialidad(nombre_especialidad):
    resultados = []
    for area in base_diagnosticos_arbol:
        for esp in area["especialidades"]:
            if esp["nombre"].lower() == nombre_especialidad.lower():
                resultados.extend(esp["diagnosticos"])
    return resultados

#----------------------------------------- Recorridos -----------------------------------------

def recorrido_preorden():
    #Raiz - izquierda - derecha
    resultado = []
    for area in base_diagnosticos_arbol:
        resultado.append(area["area"])
        for esp in area["especialidades"]:
            resultado.append(esp["nombre"])
            for diag in esp["diagnosticos"]:
                resultado.append(diag["nombre"])
    return resultado

def recorrido_inorden():
    #izquierda - raiz - derecha
    resultado = []
    for area in base_diagnosticos_arbol:
        mitad_area = len(area["especialidades"]) // 2

        # primera mitad de especialidades
        for esp in area["especialidades"][:mitad_area]:
            mitad_diag = len(esp["diagnosticos"]) // 2
            for diag in esp["diagnosticos"][:mitad_diag]:
                resultado.append(diag["nombre"])
            resultado.append(esp["nombre"])
            for diag in esp["diagnosticos"][mitad_diag:]:
                resultado.append(diag["nombre"])

        # nodo del área en medio
        resultado.append(area["area"])

        # segunda mitad de especialidades
        for esp in area["especialidades"][mitad_area:]:
            mitad_diag = len(esp["diagnosticos"]) // 2
            for diag in esp["diagnosticos"][:mitad_diag]:
                resultado.append(diag["nombre"])
            resultado.append(esp["nombre"])
            for diag in esp["diagnosticos"][mitad_diag:]:
                resultado.append(diag["nombre"])

    return resultado


def recorrido_postorden():
    #izquierda - derecha - raiz
    resultado = []
    for area in base_diagnosticos_arbol:
        for esp in area["especialidades"]:
            for diag in esp["diagnosticos"]:
                resultado.append(diag["nombre"])
            resultado.append(esp["nombre"])
        resultado.append(area["area"])
    return resultado

#----------------------------------------------------------------------------------------------
#                                          Sub-Menu - Modulo 3
#----------------------------------------------------------------------------------------------

def ModuloDiagnosticos():
    while True:
        print("\n")
        print("=" * 45)
        print("        Árbol de Diagnósticos       ")
        print("="*45)
        print("1. Buscar diagnóstico por nombre o código")
        print("2. Mostrar diagnósticos de una especialidad")
        print("3. Recorrido Preorden")
        print("4. Recorrido Inorden")
        print("5. Recorrido Postorden")
        print("6. Salir al menú principal")

        try:
            opcion = int(input("Opcion: "))
        except:
            print("Error: Opcion invalida.")
            continue

        match opcion:
            case 1:

                tracemalloc.start()
                tiempo_inicio = time.perf_counter()

                dato = str(input("\nDigite nombre o código del diagnóstico: ")) #exception

                resultado = buscarDiagnosticos(dato,base_diagnosticos_arbol)
                if resultado:
                    print("\nDiagnóstico encontrado:", resultado)
                else:
                    print("\nNo se encontró el diagnóstico.")

                memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                tiempo_fin = time.perf_counter()
                duracion = tiempo_fin - tiempo_inicio
                memoria_kb = memoria_pico / 1024

                print("\nDuración:", duracion, "segundos.")
                print("Consumo de memoria:", memoria_kb, "KB.")

            case 2:
                tracemalloc.start()
                tiempo_inicio = time.perf_counter()

                esp = str(input("\nDigite el nombre de la especialidad: "))

                resultado = mostrar_diagnosticos_especialidad(esp)
                if resultado:
                    print("\nDiagnósticos de la especialidad", esp)
                    for diag in resultado:
                        print(diag)
                else:
                    print("\nNo se encontraron diagnósticos.")

                memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                tiempo_fin = time.perf_counter()
                duracion = tiempo_fin - tiempo_inicio
                memoria_kb = memoria_pico / 1024

                print("\nDuración:", duracion, "segundos.")
                print("Consumo de memoria:", memoria_kb, "KB.")

            case 3:
                tracemalloc.start()
                tiempo_inicio = time.perf_counter()

                resultado = recorrido_preorden()
                print("\nRecorrido Preorden:", resultado)

                memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                tiempo_fin = time.perf_counter()
                duracion = tiempo_fin - tiempo_inicio
                memoria_kb = memoria_pico / 1024

                print("\nDuración:", duracion, "segundos.")
                print("Consumo de memoria:", memoria_kb, "KB.")

            case 4:
                tracemalloc.start()
                tiempo_inicio = time.perf_counter()

                resultado = recorrido_inorden()
                print("\nRecorrido Inorden:", resultado)

                memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                tiempo_fin = time.perf_counter()
                duracion = tiempo_fin - tiempo_inicio
                memoria_kb = memoria_pico / 1024

                print("\nDuración:", duracion, "segundos.")
                print("Consumo de memoria:", memoria_kb, "KB.")

            case 5:
                tracemalloc.start()
                tiempo_inicio = time.perf_counter()

                resultado = recorrido_postorden()
                print("\nRecorrido Postorden:", resultado)

                memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                tiempo_fin = time.perf_counter()
                duracion = tiempo_fin - tiempo_inicio
                memoria_kb = memoria_pico / 1024
                
                print("\nDuración:", duracion, "segundos.")
                print("Consumo de memoria:", memoria_kb, "KB.")

            case 6:
                print("\nRegresando al menú principal...")
                break

            case _:
                print("\nOpcion no es válida.")

#===============================================================================================================================

#                                  Módulo 4 — Laboratorio de rendimiento

#===============================================================================================================================


# ------------------------------------------------------------------------
#              Memoria de resultados para la curva de crecimiento
# ------------------------------------------------------------------------

historial_ordenamientos = {}


# ------------------------------------------------------------------------
#              Entrada Parametro: Tamaño del archivo
# ------------------------------------------------------------------------

def sizeArchivo():

    while True:
        print("\n----> Paso 1: Seleccione el tamaño del conjunto de datos:")
        print("1. Archivo de 500 registros.")
        print("2. Archivo de 5,000 registros.")
        print("3. Archivo de 50,000 registros.")
        print("4. Archivo de 200,000 registros.")

        opcion = input("Opcion: ").strip()

        if opcion == "1": return "500"
        if opcion == "2": return "5000"
        if opcion == "3": return "50000"
        if opcion == "4": return "200000"

        print("Error: Opción Invalida. Intente de nuevo.\n")


# ------------------------------------------------------------------------
#              Entrada Parametro: Criterio de Ordenamiento
# ------------------------------------------------------------------------

def criterioOrdenPacientes():

    while True:
        print("----> Paso 2: Seleccione el criterio de ordenamiento:")
        print("1. Ordenar registro de pacientes por nombre.")
        print("2. Ordenar registro de pacientes por edad.")
        print("3. Ordenar registro de pacientes por fecha de registro.")
        print("4. Ordenar registro de pacientes por nivel de prioridad.")

        opcion = input("Opcion: ").strip()

        if opcion == "1": return "Nombre"
        if opcion == "2": return "Edad"
        if opcion == "3": return "Fecha"
        if opcion == "4": return "Prioridad"
        print("Error: Opción Invaida. Intente de nuevo.\n")


def criterioOrdenConsultas():
    while True:
        print("---> Seleccione el criterio de ordenamiento:")
        print("1. Ordenar registro de consultas por fecha.")
        print("2. Ordenar registro de consultas por gravedad.")

        opcion = input("Opcion: ").strip()

        if opcion == "1": return "Fecha"
        if opcion == "2": return "Gravedad"
        print("Error: Opción Invaida. Intente de nuevo.\n")


# ------------------------------------------------------------------------
#              Entrada Parametro: Algoritmo de Ordenamiento
# ------------------------------------------------------------------------

def algoritmo():

    while True:
        print("----> Paso 3: Seleccione los métodos de ordenamiento a comparar (Ej: 1,4,5):")
        print("1. Bubble Sort.")
        print("2. Selection Sort.")
        print("3. Insertion Sort.")
        print("4. Quick Sort.")
        print("5. Merge Sort.")

        opcion = input("Opcion: ").replace(" ", "")

        if opcion == "":
            print("Error: Debe seleccionar al menos un algoritmo.\n")
            continue

        listaOpciones = opcion.split(",")
        opcion_valida = True

        for item in listaOpciones:
            if item not in ["1", "2", "3", "4", "5"]:
                opcion_valida = False
                break

        if opcion_valida:

            nombresAlgoritmos = {
                "1": "Bubble Sort",
                "2": "Selection Sort",
                "3": "Insertion Sort",
                "4": "Quick Sort",
                "5": "Merge Sort"
            }

            lista_nombres = []

            for codigo in listaOpciones:
                nombre = nombresAlgoritmos[codigo]
                if nombre not in lista_nombres:
                    lista_nombres.append(nombre)
            return lista_nombres

        print("Error: Ingrese solo números del 1 al 5 separados por comas (ejemplo: 1,4).\n")


# ------------------------------------------------------------------------
#              Funciones de Algoritmos de Ordenamiento
# ------------------------------------------------------------------------

def obtener_llave(paciente, criterio):

    if criterio == "Nombre": return paciente["nombre"].lower()
    if criterio == "Edad": return paciente["edad"]
    if criterio == "Fecha":  return paciente["fecha"]
    if criterio == "Prioridad": return paciente["prioridad"]
    if criterio == "Gravedad": return paciente["gravedad"]

    return paciente["cedula"]


def ejecutarOrdenamiento(nombre_algoritmo, lista, criterio):

    if nombre_algoritmo == "Bubble Sort":  return BubbleSort(lista, criterio)
    if nombre_algoritmo == "Selection Sort": return SelectionSort(lista, criterio)
    if nombre_algoritmo == "Insertion Sort":  return InsertionSort(lista, criterio)
    if nombre_algoritmo == "Quick Sort": return QuickSort(lista, criterio)
    if nombre_algoritmo == "Merge Sort":  return MergeSort(lista, criterio)


def BubbleSort(lista, criterio):

    n = len(lista)

    for i in range(n):
        cambioEnListaOriginal = False

        for j in range(0, n-i-1):

            if obtener_llave(lista[j], criterio) > obtener_llave(lista[j+1], criterio):
                lista[j], lista[j+1] = lista[j+1], lista[j]
                cambioEnListaOriginal = True

        if not cambioEnListaOriginal:
            break

    return lista


def SelectionSort(lista, criterio):

    n = len(lista)

    for i in range(n):

        valorMasPequeno = i

        for j in range(i+1, n):

            if obtener_llave(lista[j], criterio) < obtener_llave(lista[valorMasPequeno], criterio):
                valorMasPequeno = j

        lista[i], lista[valorMasPequeno] = lista[valorMasPequeno], lista[i]

    return lista


def InsertionSort(lista, criterio):

    for i in range(1, len(lista)):

        actual = lista[i]
        valActual = obtener_llave(actual, criterio)
        j = i - 1

        while j >= 0 and obtener_llave(lista[j], criterio) > valActual:
            lista[j+1] = lista[j]
            j = j - 1

        lista[j+1] = actual

    return lista


def QuickSort(lista, criterio):

    if len(lista) <= 1:
        return lista

    pivote = lista[len(lista) // 2]
    valorPivote = obtener_llave(pivote, criterio)

    izq = [x for x in lista if obtener_llave(x, criterio) < valorPivote]
    centro = [x for x in lista if obtener_llave(x, criterio) == valorPivote]
    der = [x for x in lista if obtener_llave(x, criterio) > valorPivote]

    return QuickSort(izq, criterio) + centro + QuickSort(der, criterio)


def MergeSort(lista, criterio):

    if len(lista) <= 1:
        return lista

    medio = len(lista) // 2

    izq = MergeSort(lista[:medio], criterio)
    der = MergeSort(lista[medio:], criterio)

    res = []

    i = j = 0

    while i < len(izq) and j < len(der):

        if obtener_llave(izq[i], criterio) <= obtener_llave(der[j], criterio):
            res.append(izq[i])
            i += 1

        else:
            res.append(der[j])
            j += 1

    return res + izq[i:] + der[j:]


# ------------------------------------------------------------------------
#              Funciones de Busqueda Binaria y Busqueda Lineal
# ------------------------------------------------------------------------

def busquedaLineal(lista_ordenada, criterio, valor_buscado):

    if criterio == "Nombre":
        valor_buscado = str(valor_buscado).lower()

    elif criterio in ["Edad", "Prioridad", "Gravedad"]:
        try:
            valor_buscado = int(valor_buscado)
        except:
            print("Error: El valor", valor_buscado,"no es un número válido para el criterio",criterio)
            return []

    resultados = []

    for elemento in lista_ordenada:

        if obtener_llave(elemento, criterio) == valor_buscado:
            resultados.append(elemento)

    return resultados


def busquedaBinaria(lista_ordenada, criterio, valor):

    if criterio == "Nombre":
        valor = str(valor).lower()

    elif criterio in ["Edad", "Prioridad", "Gravedad"]:
        try:
            valor = int(valor)
        except ValueError:
            return []

    izq = 0
    der = len(lista_ordenada) - 1
    index = -1

    while izq <= der:

        medio = (izq + der) // 2

        valorMedio = obtener_llave(lista_ordenada[medio], criterio)

        if valorMedio == valor:
            index = medio
            break

        elif valorMedio < valor:
            izq = medio + 1

        else:
            der = medio - 1

    if index == -1:
        return []

    resultados = []

    for x in lista_ordenada:

        if obtener_llave(x, criterio) == valor:
            resultados.append(x)

    return resultados


# ------------------------------------------------------------------------
#              Funciones de Generación de Gráficos
# ------------------------------------------------------------------------

def actualizarGraficaBarras(metricas_orden):

    plt.figure("Duración de algoritmos")

    plt.clf()

    nombres = list(metricas_orden.keys())
    tiempos = []

    for algoritmo_nombre in nombres:
        tiempos.append(metricas_orden[algoritmo_nombre]["tiempo"])

    plt.bar(nombres, tiempos)

    plt.title("Duración de los algoritmos de ordenamiento")
    plt.xlabel("Algoritmo")
    plt.ylabel("Tiempo (segundos)")

    plt.xticks(rotation=20)

    plt.tight_layout()

    plt.draw()
    plt.pause(0.1)


def actualizarGraficaCrecimiento():

    plt.figure("Curva de crecimiento")

    plt.clf()

    plt.subplot(1, 2, 1)

    for clave in historial_ordenamientos:

        datos = historial_ordenamientos[clave]

        tamanos = datos["tamanos"]
        tiempos = datos["tiempos"]

        if len(tamanos) > 0:
            plt.plot(tamanos, tiempos, marker="o", label=clave)

    plt.title("Curva de crecimiento del tiempo")
    plt.xlabel("Tamaño del conjunto de datos")
    plt.ylabel("Tiempo (segundos)")

    plt.legend()

    plt.grid(True)

    plt.subplot(1, 2, 2)

    for clave in historial_ordenamientos:

        datos = historial_ordenamientos[clave]

        tamanos = datos["tamanos"]
        memorias = datos.get("memorias", [])

        if len(tamanos) > 0 and len(memorias) == len(tamanos):
            plt.plot(tamanos, memorias, marker="o", label=clave)

    plt.title("Curva de crecimiento de memoria")
    plt.xlabel("Tamaño del conjunto de datos")
    plt.ylabel("Memoria (KB)")

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.draw()
    plt.pause(0.1)


# ------------------------------------------------------------------------
#              Registro de resultados para la curva
# ------------------------------------------------------------------------

def guardarResultadoCrecimiento(algoritmo_nombre, criterio, cantidad, tiempo, memoria=0):

    clave = algoritmo_nombre + " - " + criterio

    if clave not in historial_ordenamientos:

        historial_ordenamientos[clave] = {
            "tamanos": [],
            "tiempos": [],
            "memorias": []
        }

    tamanos = historial_ordenamientos[clave]["tamanos"]
    tiempos = historial_ordenamientos[clave]["tiempos"]

    if "memorias" not in historial_ordenamientos[clave]:
        historial_ordenamientos[clave]["memorias"] = []

    memorias = historial_ordenamientos[clave]["memorias"]

    if cantidad in tamanos:

        posicion = tamanos.index(cantidad)
        tiempos[posicion] = tiempo

        if posicion < len(memorias):
            memorias[posicion] = memoria
        else:
            memorias.append(memoria)

    else:

        tamanos.append(cantidad)
        tiempos.append(tiempo)
        memorias.append(memoria)


# ------------------------------------------------------------------------------------------------------------
#                                      SubMenu Experimentos - Modulo 4
# ------------------------------------------------------------------------------------------------------------

def MenuLabExperimentos():

    plt.ion()

    while True:

        print("\n", "=" * 100)
        print("        Bienvenido al Laboratorio de Rendimiento")
        print("=" * 100)
        print("1. Iniciar experimento comparativo.")
        print("2. Mostrar curva de crecimiento.")
        print("3. Volver al menú principal.")

        opcionInicio = input("Opción: ").strip()

        if opcionInicio == "3":
            plt.close("all")
            print("\nRegresando al menú principal.")
            break

        elif opcionInicio == "2":
            if not historial_ordenamientos:
                print("\nTodavía no hay resultados almacenados.")

            else:
                actualizarGraficaCrecimiento()
                print("\nCurva de crecimiento actualizada.")
            continue

        elif opcionInicio != "1":
            print("Error: Opción inválida. Intente de nuevo.")
            continue

        if plt.fignum_exists("Curva de crecimiento"):
            plt.close("Curva de crecimiento")

        print("\nIniciando Experimento Completo (Ordenar y Buscar)\n")


        # ------------------------------- Recoleccion de parametros -------------------------------

        datos_experimento = []
        pacientes_o_consultas = ""
        archivo = ""
        orden = ""

        while True:
            print("¿Que conjunto de datos desea ordenar?")
            print("1. Ordenar registro de pacientes.")
            print("2. Ordenar registro de consultas.")
            opcion = input("Opción: ").strip()

            if opcion == "1":
                pacientes_o_consultas = "pacientes"
                tamano = sizeArchivo()
                archivo = f"pacientes_{tamano}.txt"
                print("Archivo seleccionado:", archivo, "\n")

                datos_experimento = cargarPacientes(archivo)
                orden = criterioOrdenPacientes()
                print("Criterio de ordenamiento seleccionado:", orden, "\n")
                break  #Rompe el bucle para continuar con el experimento

            elif opcion == "2":
                pacientes_o_consultas = "consultas"
                tamano = sizeArchivo()
                archivo = f"consultas_{tamano}.txt"
                print("Archivo seleccionado:", archivo, "\n")

                datos_experimento = cargarConsultas(archivo)
                orden = criterioOrdenConsultas()
                print("Criterio de ordenamiento seleccionado:", orden, "\n")
                break  # Rompe el bucle para continuar con el experimento

            else: print("Error: Opción inválida. Selecciones 1 o 2.\n")

            #Mismo para ambos (pacientes o consultas)
        algoritmos = algoritmo()
        print("Algoritmos seleccionados:", algoritmos, "\n")

        cantidad_datos = len(datos_experimento)


        # ------------------------------- Ejecución de Ordenamientos -------------------------------

        print(
            "Ejecutando ordenamiento de",cantidad_datos, pacientes_o_consultas,"por", orden, "con algoritmos", algoritmos)

        metricas_orden = {}
        lista_ordenada = []

        for algoritmo_nombre in algoritmos:

            print("\nEjecutando", algoritmo_nombre, "...")

            tracemalloc.start()
            tiempo_inicio = time.perf_counter()

            lista_ordenada = ejecutarOrdenamiento(
                algoritmo_nombre,
                datos_experimento.copy(),
                orden
            )

            tiempo_fin = time.perf_counter()
            memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            duracion = tiempo_fin - tiempo_inicio
            memoria_kb = memoria_pico / 1024

            metricas_orden[algoritmo_nombre] = {
                "tiempo": duracion,
                "memoria": memoria_kb
            }

            guardarResultadoCrecimiento(
                algoritmo_nombre,
                orden,
                cantidad_datos,
                duracion,
                memoria_kb
            )

            print(
                "Tiempo:",
                duracion,
                "segundos"
            )
            print(
                "Memoria:",
                memoria_kb,
                "KB"
            )


            # Actualiza la grafica de barras inmediatamente despues de terminar cada algoritmo

            actualizarGraficaBarras(metricas_orden)


        print("\n¡Ordenamientos completados con éxito!")
        print("¡Graficos generados con éxito!")


        # ------------------------------- Busqueda Lineal vs Binaria -------------------------------

        while True:

            print("\n" + "=" * 100)

            print("                            Experimento de Búsquedas")
            print("=" * 100)
            print("1. Realizar una búsqueda (Lineal vs Binaria)")
            print("2. Terminar experimento (Cambiar parámetros o salir)")
            print("-" * 55)

            opcion = input("Opcion: ").strip()

            if opcion == "2":
                print("\nSaliendo del conjunto de datos actual.")
                break

            elif opcion == "1":
                valorBuscado = input(f"\nIngrese el/la {orden} a buscar: ")

                #Validacion para campos numericos
                if orden in ["Edad", "Prioridad", "Gravedad"]:
                    try:
                        int(valorBuscado)
                    except ValueError:
                        print("\nError: El valor",valorBuscado,"no es un número válido para el criterio",orden,".")
                        print("Regresando al menú de búsquedas...")
                        continue #Salta lo que sigue y vuelve a pedir el input

                #Validacion para campo fecha
                elif orden == "Fecha":
                        try:
                            datetime.strptime(valorBuscado, "%Y-%m-%d")
                        except ValueError:
                            print("Error: El valor",valorBuscado,"no es una fecha válida. Use el formato AAAA-MM-DD (Ej: 2025-03-21).")
                            continue

                metricas_busqueda = {}


                # ---------------- Medicion Busqueda Lineal ----------------

                tracemalloc.start()
                t_inicio_lin = time.perf_counter()

                lineal = busquedaLineal(
                    lista_ordenada,
                    orden,
                    valorBuscado
                )

                t_fin_lin = time.perf_counter()
                _, m_pico_lin = tracemalloc.get_traced_memory()
                tracemalloc.stop()


                metricas_busqueda["Búsqueda Lineal"] = {
                    "tiempo": t_fin_lin - t_inicio_lin,
                    "memoria": m_pico_lin / 1024,
                    "hallados": len(lineal)
                }


                # ---------------- Medicion Busqueda Binaria ----------------

                tracemalloc.start()
                t_inicio_bin = time.perf_counter()

                binaria = busquedaBinaria(
                    lista_ordenada,
                    orden,
                    valorBuscado
                )

                t_fin_bin = time.perf_counter()
                _, m_pico_bin = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                metricas_busqueda["Búsqueda Binaria"] = {
                    "tiempo": t_fin_bin - t_inicio_bin,
                    "memoria": m_pico_bin / 1024,
                    "hallados": len(binaria)
                }

                # ---------------- Resultados ----------------

                print("\n" + "-" * 60)
                print("         Resultados de las Busquedas (Por",orden,")")
                print("-" * 60)

                print("---> Búsqueda Lineal")

                print("Duración:", metricas_busqueda["Búsqueda Lineal"]["tiempo"], "segundos")
                print( "Consumo de memoria:",metricas_busqueda["Búsqueda Lineal"]["memoria"], "KB")
                print( "Resultados encontrados:",metricas_busqueda["Búsqueda Lineal"]["hallados"])

                print("\n---> Búsqueda Binaria:")

                print( "Duración:", metricas_busqueda["Búsqueda Binaria"]["tiempo"], "segundos")
                print( "Consumo de memoria:",  metricas_busqueda["Búsqueda Binaria"]["memoria"],"KB" )
                print("Resultados encontrados:",metricas_busqueda["Búsqueda Binaria"]["hallados"])

            else:
                print("Error: Opcion inválida. Intente de nuevo.")

#===============================================================================================================================

#                                                        MENU PRINCIPAL

#===============================================================================================================================

def menuPrincipal():
    print("\n", "=" * 100)
    print("                               Sistema de Gestión de Clínica ")
    print("", "=" * 100)

    while True:
        print("\n                 Menú Principal  ")
        print("", "=" * 45)
        print("Seleccione una opción:")
        print("1. Sala de Espera de Atención (Cola de prioridad).")
        print("2. Busqueda de expedientes.")
        print("3. Busqueda de diagnósticos.")
        print("4. Búsqueda de pacientes (Experimentos de rendimiento)")
        print("5. Finalizar el sistema.")

        opcion = input("Opción: ").strip()

        if opcion == "1":
            print("\nIngresando a la Sala de Espera.")
            colaPrioridad(base_pacientes)

        elif opcion == "2":
            print("\nIngresando a la Busqueda de expedientes.")
            ExpedientesBusqueda()

        elif opcion == "3":
            print("\nIngresando a la Busqueda de diagnósticos.")
            ModuloDiagnosticos()
        elif opcion == "4":
            print("\nIngresando a la Busqueda de pacientes (Experimentos de rendimiento).")
            MenuLabExperimentos()

        elif opcion == "5":
            print("\nFinalizando el sistema.")
            break

        else: print("Error: Opción inválida. Intente de nuevo.")

menuPrincipal()
