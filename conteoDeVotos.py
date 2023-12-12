from tabulate import tabulate
import csv
import os.path
import sys
import configparser
import re
import datetime

config = configparser.ConfigParser()
MAX_CANDIDATOS = 0
MAX_ESTADOS = 0
nombre = 0
apellido = 1
nombreEstado = 1
candidatoCedula = []
candidatoNacimiento = []
configurado = 'no'
candidatos = []
estados = []
anio = 0
paisSeleccionado = ""
pais = ""
historialDeElecciones = []
historialDeErrores = []
pausa = "Presione enter para continuar...\n"
cabeceraResultados = ["Candidatos", "Votos totales", "Porcentaje", "status", "año", "país"]
paises = ["Argentina", "Bolivia", "Brasil", "Chile", "Colombia", "Costa Rica", "Cuba", "Ecuador", "El Salvado",
          "Guayana Francesa", "Granada", "Guatemala", "Guayana", "Haití", "Honduras", "Jamaica", "México", "Nicaragua",
          "Paraguay", "Panamá", "Perú", "Puerto Rico", "República Dominicana", "Surinam", "Uruguay", "Venezuela"
          ]


def importar():
    global configurado
    global MAX_CANDIDATOS
    global MAX_ESTADOS
    global anio
    global pais
    global estados
    global candidatos
    global historialDeElecciones

    # ver si existe el archivo config.ini
    existeConfig = os.path.exists('config.ini')
    if not existeConfig:
        # configuracion por default
        config['rutas'] = {
            'log_errores': 'log_errores.txt',
            'log_elecciones': 'log_historialDeElecciones.csv',
        }
        config['modulos'] = {
            'reportes_elecciones': 'si',
            'reportes_errores': 'si',
            'datos_prestablecidos': 'si'
        }
        config['configVotacion'] = {
            'configurado': "no",
            'max_candidatos': 0,
            'max_estados': 0,
            'anio_eleccion': 0,
            'pais': '',
        }
        config['candidatos'] = {}
        config['estados'] = {}
        # se guarda la configuracion por default
        with open('config.ini', 'w') as archivoConfig:
            config.write(archivoConfig)
    else:
        # importar configuracion existente
        config.read('config.ini')

        # importar configuracion de votacion si hay
        if config['configVotacion']['configurado'] == 'si':
            configurado = 'si'
            MAX_CANDIDATOS = int(config['configVotacion']['max_candidatos'])
            MAX_ESTADOS = int(config['configVotacion']['max_estados'])
            anio = config['configVotacion']['anio_eleccion']
            pais = config['configVotacion']['pais']
            for candidato in range(MAX_CANDIDATOS):
                candidatos.append(config['candidatos'][str(candidato)].split())

            # importar variable estados
            for i in range(MAX_ESTADOS):
                estado = [i, config['estados'][str(i)]]
                for candidato in range(MAX_CANDIDATOS):
                    estado.append(0)
                estados.append(estado)

    # importar elecciones
    existeEleccionesLog = os.path.exists(f"{config['rutas']['log_elecciones']}")
    #ver si existe el log de elecciones
    if not existeEleccionesLog:
        with open(f"{config['rutas']['log_elecciones']}", 'a', newline='') as archivocsv:
            csvwriter = csv.writer(archivocsv,  dialect="excel")
            csvwriter.writerow(cabeceraResultados)
    else:
        # si existe se lee 
        with open(f"{config['rutas']['log_elecciones']}", newline='') as archivocsv:
            reader = csv.DictReader(archivocsv)
            for row in reader:
                historialDeElecciones.append([[row['Candidatos'], row['Votos totales'], row['Porcentaje'],
                                                  row['status'], row['año'], row['país']]])


        # importar errores
        existeErroresLog = os.path.exists(f"{config['rutas']['log_errores']}")
        if existeErroresLog:
            with open(f"{config['rutas']['log_errores']}") as f:
                errores = f.readlines()
                if errores:
                    for err in range(len(errores)):
                        historialDeErrores.append([])
                        historialDeErrores[err].append([errores[err]])
importar()


def reset():
    global configurado
    global estados
    global candidatos
    global anio
    configurado = 'no'
    candidatos.clear()
    estados.clear()
    anio = 0
    config['configVotacion']['configurado'] = "no"
    config['configVotacion']['max_candidatos'] = str(0)
    config['configVotacion']['max_estados'] = str(0)
    config['configVotacion']['anio_eleccion'] = str(0)
    config['configVotacion']['pais'] = ''
    config['candidatos'].clear()
    config['estados'].clear()

    with open('config.ini', 'w') as archivoConfig:
        config.write(archivoConfig)
# Módulo de configuración
def configMaquina():
    print("============ Configuración de la Máquina ============")
    global estados
    global candidatos
    global configurado
    global config
    global MAX_CANDIDATOS
    global MAX_ESTADOS
    global candidatoCedula
    global candidatoNacimiento
    global anio
    global pais
    if configurado == 'si':
        eleccion = entrada("esta máquina ya está configurada ¿desea reiniciar la configuración? (S/N):\n", "siOno",
                           "configMaquina")
        if eleccion == "s":
            reset()
            configMaquina()
        else:
            main()
    else:
        while True:
            MAX_CANDIDATOS = entrada("Ingrese la cantidad de candidatos: ", "numerico", "configMaquina")
            if MAX_CANDIDATOS <= 1:
                print("[ERROR] ingrese más de 1 candidato")
                guardarErrores(f"{datetime.datetime.now()}", "solo se ingresó 1 candidato", "configMaquina")
            else:
                break

        while True:
            MAX_ESTADOS = entrada("Ingrese la cantidad de estados: ", "numerico", "configMaquina")
            if MAX_ESTADOS == 0:
                print("[ERROR] ingrese al menos 1 estado")
                guardarErrores(f"{datetime.datetime.now()}", "se ingresó 0 estados", "configMaquina")
            else:
                break

        anio = entrada("Ingrese el año de la eleccion (ejem: 2023): ", "año", "configMaquina")
        pais = escogerPais()

        for estado in range(MAX_ESTADOS):
            estados.append([])
            estados[estado].append(estado)
            print("")
            print(str(estado + 1) + "/" + str(MAX_ESTADOS))
            estados[estado].append(entrada("Ingrese el nombre de un estado: ", "estado", "configMaquina"))
        for estado in range(MAX_ESTADOS):
            for i in range(MAX_CANDIDATOS):
                estados[estado].append(0)
        for i in range(MAX_CANDIDATOS):
            candidatos.append([])
        for candidato in range(MAX_CANDIDATOS):
            print("")
            print("insercion DE CANDIDATOS")
            print(str(candidato + 1) + "/" + str(MAX_CANDIDATOS))
            candidatos[candidato].append(entrada("Ingrese el nombre del candidato: ", "texto", "configMaquina"))
            candidatos[candidato].append(entrada("Ingrese el apellido del candidato: ", "texto", "configMaquina"))
            candidatoCedula.append(
                entrada("Ingrese la cedula del candidato separado por puntos (.): ", "cedula", "configMaquina"))
            candidatoNacimiento.append(
                entrada("Ingrese fecha de nacimiento del candidato dd/mm/aa: ", "fecha", "configMaquina"))
        configurado = "si"
        config['configVotacion']['configurado'] = configurado
        config['configVotacion']['max_candidatos'] = str(MAX_CANDIDATOS)
        config['configVotacion']['max_estados'] = str(MAX_ESTADOS)
        config['configVotacion']['anio_eleccion'] = str(anio)
        config['configVotacion']['pais'] = pais

        for candidato in range(MAX_CANDIDATOS):
            config['candidatos'][str(candidato)] = candidatos[candidato][nombre] + " " + candidatos[candidato][apellido]
        for estado in range(MAX_ESTADOS):
            config['estados'][str(estado)] = estados[estado][1]
        with open('config.ini', 'w') as archivoConfig:
            config.write(archivoConfig)
        print("La máquina ha sido configurada exitosamente")
        input(pausa)
        main()


def voto():
    print("============ Proceso de votación iniciado ============")
    while True:
        # impresion de los estados
        while True:
            for estado in range(MAX_ESTADOS):
                print(str(estado + 1) + ".- " + estados[estado][nombreEstado])
            votoEstado = int(entrada("Ingrese el numero de su estado: ", "opcion", "voto"))
            if votoEstado > MAX_ESTADOS or votoEstado == 0:
                print("[ERROR] Opcion incorrecta")
                guardarErrores(f"{datetime.datetime.now()}", "opcion incorrecta", "voto")
            else:
                break
        # impresion de los candidatos
        while True:
            for candidato in range(MAX_CANDIDATOS):
                print(
                    str(candidato + 1) + ".- " + candidatos[candidato][nombre] + " " + candidatos[candidato][apellido])
            votoCandidato = int(entrada("Ingrese el numero del candidato por quien quiere votar: ", "opcion", "voto"))
            if votoCandidato > MAX_CANDIDATOS or votoCandidato == 0:
                print("[ERROR] Opcion incorrecta")
                guardarErrores(f"{datetime.datetime.now()}", "opcion incorrecta", "voto")
            else:
                break
        # se guarda el voto
        estados[votoEstado - 1][votoCandidato + 1] = estados[votoEstado - 1][votoCandidato + 1] + 1

        print("voto agregado con exito!")
        eleccion = entrada("Desea cerrar la máquina? (s/n): ", "siOno", "voto")
        if eleccion == "s":
            conteo()
            print("")
            print("La máquina ha cerrado")
            exportar()
            input(pausa)
            main()
            break


# MODULO DE CONTEO DE VOTOS
def conteo():
    global MAX_ESTADOS
    global MAX_CANDIDATOS
    global estados
    global candidatos
    global pais
    votos = []
    resultados = []
    porcentajes = []
    hayUnGanador = False
    count = 0
    candidatoStatus = ""
    porcentajesOrdenados = None
    resultadosOrdenados = None
    for candidato in range(MAX_CANDIDATOS):
        votos.append(0)
        for estado in range(MAX_ESTADOS):
            votos[candidato] = votos[candidato] + estados[estado][candidato + 2]
    for candidato in range(MAX_CANDIDATOS):
        resultados.append([])
        resultados[candidato].append(candidatos[candidato][nombre] + " " + candidatos[candidato][apellido])
        resultados[candidato].append(votos[candidato])
        calculoPorcentaje = int(votos[candidato] / sum(votos) * 100)
        porcentajes.append(calculoPorcentaje)
        resultados[candidato].append((porcentajes[candidato]))
        resultadosOrdenados = sorted(resultados, key=lambda v: v[1], reverse=True)
        porcentajesOrdenados = sorted(resultados, key=lambda v: v[1], reverse=True)

    for candidato in range(MAX_CANDIDATOS):
        if not hayUnGanador:
            if porcentajesOrdenados[candidato][2] > 50:
                candidatoStatus = " (Ganador)"
                hayUnGanador = True
            else:
                if count < 2:
                    candidatoStatus = " (Más votado)"
                    count = count + 1
        resultadosOrdenados[candidato].append(candidatoStatus)
        resultadosOrdenados[candidato].append(anio)
        resultadosOrdenados[candidato].append(pais)
        candidatoStatus = ""
    guardarEnHistorial(resultadosOrdenados)
    impresion(resultadosOrdenados)

def votoPrestablecido():
    print("============ Votación con datos Prestablecidos ============")
    global MAX_CANDIDATOS
    global MAX_ESTADOS
    global candidatos
    global estados
    global anio
    global pais
    global paisSeleccionado
    MAX_CANDIDATOS = 4
    MAX_ESTADOS = 5
    anio = 2023
    pais = escogerPais()
    #   paisSeleccionado = "Venezuela"
    candidatos = [
        ["candidato", "A"],
        ["candidato", "B"],
        ["candidato", "C"],
        ["candidato", "D"],
    ]
    estados = [
        [1, "distrito capital", 180, 20, 320, 16],
        [2, "cojedes", 221, 90, 50, 61],
        [3, "apure", 432, 50, 821, 14],
        [4, "zulia", 820, 61, 946, 18],
        [5, "barinas", 820, 61, 946, 18]
    ]
    conteo()


def impresion(resultadosOrdenados):
    print("============ Resultados de las Votaciones ============")
    cabecera = ["N° ESTADO", "ESTADO"]
    for candidato in range(MAX_CANDIDATOS):
        cabecera.append(candidatos[candidato][nombre] + " " + candidatos[candidato][apellido])
    print(tabulate(estados, cabecera))
    print("-------------------------------------")
    print("============ Resultados Totales de las Votaciones ============")
    print(tabulate(resultadosOrdenados, cabeceraResultados))


def guardarEnHistorial(eleccion):
    global historialDeElecciones
    historialDeElecciones.append(eleccion)


def entrada(texto, tipo, modulo):
    regex = ""
    global historialDeErrores
    eleccion = str(input(texto))
    while True:
        if len(eleccion) == 0:
            print("[ERROR] no se introdujo nada, intente de nuevo")
            guardarErrores(f"{datetime.datetime.now()},", "[ERROR] no se introdujo nada, intente de nuevo", modulo)
            eleccion = str(input(texto))
        else:
            break
    if tipo == "opcion":
        regex = "^\d$"
    elif tipo == "año":
        regex = "^\d{4}$"
    elif tipo == "estado":
        regex = "^[a-zA-Z]+\s?[a-zA-Z]+$"
    elif tipo == "paisOpcion":
        regex = "^([0-9]|1[0-9]|2[0-5])$"
    elif tipo == "cedula":
        regex = "^\d{1,2}\.\d{3}\.\d{3}$"
    elif tipo == "fecha":
        regex = "^\S+$"
    elif tipo == "texto":
        regex = "^[a-zA-Z]+$"
    elif tipo == "numerico":
        regex = "^\d+$"
    elif tipo == "siOno":
        regex = "^(s|n)$"
    while True:
        coincidir = re.search(regex, eleccion)
        if coincidir == None:
            print("[ERROR] Datos incorrectos, intente de nuevo")
            guardarErrores(f"{datetime.datetime.now()}", "datos incorrectos", "entrada")
            eleccion = str(input(texto))
        else:
            break
    if tipo == "paisOpcion" or tipo == "año" or tipo == "numerico":
        return int(eleccion)
    else:
        return eleccion


def exportar():
    print("===== Exportar Elecciones =====")
    if len(historialDeElecciones) == 0:
        print("El historial esta vacio")
        input(pausa)
        reportes()
    else:
        with open(f"{config['rutas']['log_elecciones']}", 'a', newline='') as archivocsv:
            csvwriter = csv.writer(archivocsv,  dialect="excel")
            for eleccion in range(len(historialDeElecciones)):
                for candidato in range(len(historialDeElecciones[eleccion])):
                    csvwriter.writerows(historialDeElecciones[eleccion])

        print("Lista exportada correctamente")
        input(pausa)
        reportes()


def historial():
    print("===== Historial =====")
    if len(historialDeElecciones) == 0:
        print("El historial esta vacio")
    else:
        for eleccion in range(len(historialDeElecciones)):
            print("Elección N°" + str(eleccion) + ":")
            print(tabulate(historialDeElecciones[eleccion], cabeceraResultados))


def historialFiltrado(lista):
    global historialDeErrores
    print("===== Historial | Búsqueda avanzada =====")
    if len(historialDeElecciones) == 0:
        print("El historial esta vacío")
        input(pausa)
        return
    rangoAnioA = entrada("Paso 1/2 - Buscar desde el año (ejem: 2020):\n", "año", "historailFIltrado")
    rangoAnioB = entrada("Paso 2/2 Buscar hasta el año (ejem: 2022):\n", "año", "historailFIltrado")

    # if rangoAnioA and rangoAnioA:
    if rangoAnioA > rangoAnioB:
        print(" =======[ERROR] =======")
        print("[ERROR] debes colocar un año mayor a", rangoAnioA, ", intente de nuevo")
        guardarErrores(f"{datetime.datetime.now()}", "debes colocar un año mayor", "historialFiltrado")
        historialFiltrado(lista)

    if lista == 1:
        pais = escogerPais()
        # Imprime el historial de elecciones filtrado por pais y año
        for eleccion in range(len(historialDeElecciones)):
            if historialDeElecciones[eleccion][0][5] == pais and \
                    int(historialDeElecciones[eleccion][0][4]) >= int(rangoAnioA) and \
                    int(historialDeElecciones[eleccion][0][4]) <= int(rangoAnioB):
                print("Elección N°" + str(eleccion) + ":")
                print(tabulate(historialDeElecciones[eleccion], cabeceraResultados))
            else:
                print("No se han encontrado resultados desde el año:", rangoAnioA, " hasta el año:", rangoAnioB,
                      " con pais: ", pais)
            input(pausa)
            reportes()
    elif lista == 2:
        cabecera = ["Pais", "Votos totales", "año"]
        pais = escogerPais()
        historialDeEleccionesTotales = []

        for eleccion in range(len(historialDeElecciones)):
            historialDeEleccionesTotales.append([])

        # Imprime el historial de elecciones filtrado por año y por total votaciones
        for eleccion in range(len(historialDeElecciones)):
            votosTotales = 0
            anioEleccion = 0
            paisEleccion = ""
            for candidato in range(MAX_CANDIDATOS):
                votosTotales = votosTotales + historialDeElecciones[eleccion][candidato][1]
                anioEleccion = historialDeElecciones[eleccion][candidato][4]
                paisEleccion = historialDeElecciones[eleccion][candidato][5]

            if historialDeElecciones[eleccion][0][5] == paisEleccion and \
                    int(historialDeElecciones[eleccion][0][4]) >= int(rangoAnioA) and \
                    int(historialDeElecciones[eleccion][0][4]) <= int(rangoAnioB):
                historialDeEleccionesTotales[eleccion].append(paisEleccion)
                historialDeEleccionesTotales[eleccion].append(votosTotales)
                historialDeEleccionesTotales[eleccion].append(anioEleccion)
                historialDeEleccionesOrdenada = sorted(historialDeEleccionesTotales, key=lambda v: v[0], reverse=True)
                for eleccion in range(len(historialDeEleccionesOrdenada)):
                    print("Elección N°" + str(eleccion) + ":")
                    print(tabulate(historialDeEleccionesOrdenada, cabecera))
            else:
                print("No se han encontrado resultados desde el año:", rangoAnioA, " hasta el año:", rangoAnioB,
                      " con pais: ", pais)
            input(pausa)
            reportes()


def reportes():
    print("============ Reportes ============")
    print("|1.- Lista de elecciones                   |")
    print("|2.- Lista de elecciones por año y país    |")
    print("|3.- Lista de elecciones con más votaciones|")
    print("|4.- Exportar lista de elecciones          |")
    print("|5.- SALIR                                 |")

    eleccion = entrada("escoja una opción:\n", int, "reportes")
    if eleccion == "1":
        historial()
        input(pausa)
        reportes()
    elif eleccion == "2":
        historialFiltrado(1)
        reportes()
    elif eleccion == "3":
        historialFiltrado(2)
        reportes()
    elif eleccion == "4":
        exportar()
    elif eleccion == "5":
        main()
    else:
        print("[ERROR] opción incorrecta")
        guardarErrores(f"{datetime.datetime.now()}", "opción incorrecta", "reportes")
        reportes()


def guardarErrores(fecha, error, modulo):
    global historialDeErrores
    historialDeErrores.append([fecha, error, modulo])
    with open(f"{config['rutas']['log_errores']}", 'a') as f:
        f.write(f'{fecha}-[Error]{modulo}:{error}')
    with open(f"{config['rutas']['log_errores']}", 'a') as f:
        f.write("\n")


def reporteErrores():
    print("============REPORTE DE ERRORES=================")
    if historialDeErrores:
        print(tabulate(historialDeErrores))
        input(pausa)
    else:
        print("El historial de errores esta vacío")
        input(pausa)

    main()


def escogerPais():
    global pais
    for i in range(len(paises)):
        print("N°", i, " ", paises[i])
    while True:
        paisSeleccionado = int(entrada("escoja un pais:\n", "paisOpcion", "escogerPais"))
        if paisSeleccionado <= 25:
            pais = paises[paisSeleccionado]
            break
        else:
            print("[ERROR] opcion incorrecta")
            guardarErrores(f"{datetime.datetime.now()}", "opcion incorrecta", "escogerPais")
            input(pausa)
    return pais


def main():
    global historialDeErrores
    global configurado
    print("============ Menú de opciones ============")
    print("|1.- Configurar máquina              |")

    if config['modulos']['datos_prestablecidos'] == 'si':
        print("|2.- Prueba con datos prestablecidos |")

    print("|3.- Votar                           |")

    if config['modulos']['reportes_elecciones'] == 'si':
        print("|4.- Reportes de elecciones          |")

    if config['modulos']['reportes_errores'] == 'si':
        print("|5.- Reportes de errores             |")

    print("|6.- SALIR                           |")
    # eleccion = int(input("escoja una opción: "))
    eleccion = entrada("escoja una opción: \n", int, "escogerPais")
    # Configurar máquina
    if eleccion == "1":
        configMaquina()
        main()
    # Prueba con datos prestablecidos
    elif eleccion == '2' and config['modulos']['datos_prestablecidos'] == 'si':
        votoPrestablecido()
        input(pausa)
        main()
    # Votar
    elif eleccion == "3":
        if configurado == "si":
            voto()
            input(pausa)
            main()
        else:
            print("La máquina no esta configurada para empezar unas votaciones")
            input(pausa)
            main()
    elif eleccion == '4' and config['modulos']['reportes_elecciones'] == 'si':
        reportes()
        main()
    elif eleccion == '5' and config['modulos']['reportes_errores'] == 'si':
        reporteErrores()
    elif eleccion == "6":
        sys.exit()
    else:
        print("[ERROR] opción incorrecta")
        guardarErrores(f"{datetime.datetime.now()}", "opción incorrecta", "main")
        main()
        return


main()
