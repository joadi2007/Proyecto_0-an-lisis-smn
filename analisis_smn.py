from datetime import datetime

MESES_ESP = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, 
    "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11,
    "diciembre": 12
    }

import json

def guardar_json(observaciones: dict, ruta_salida: str) -> None:
    """Guarda el diccionario de observaciones en un archivo JSON."""
    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        json.dump(observaciones, archivo, ensure_ascii=False, indent=2, default=str)

def separar_viento(campo_viento: str) -> tuple:
    partes = campo_viento.split()
    if len(partes) == 1:
        direccion = partes[0]
        velocidad = 0
    else:
        direccion = partes[0]
        velocidad = float(partes[1])

    return direccion, velocidad

def leer_observaciones(ruta: str) -> dict:
    observaciones = {}
    lineas_invalidas = []

    try:
        with open(ruta, 'r', encoding='latin-1') as archivo:
            for linea in archivo:
                campos = linea.strip().split(";")

                if len(campos) != 10:
                    lineas_invalidas.append(len(campos))
                    continue

                ciudad = campos[0].strip()
                direccion_viento, velocidad_viento = separar_viento(campos[8])

                try:
                    dia, mes_texto, año = campos[1].split("-")
                    hora, minuto = campos[2].split(":")
                    fecha_hora = datetime(int(año), MESES_ESP[mes_texto], int(dia), int(hora), int(minuto))
                except (ValueError, KeyError):
                    fecha_hora = None

                try:
                    sensacion_termica = float(campos[6])
                except ValueError:
                    sensacion_termica = None

                try:
                    presion = float(campos[9].strip().split()[0])
                except ValueError:
                    presion = None

                try:
                    temperatura = float(campos[5])
                except ValueError:
                    temperatura = None

                datos_ciudad = {
                    "fecha": campos[1],
                    "hora": campos[2],
                    "condicion": campos[3],
                    "visibilidad": campos[4],
                    "temperatura": temperatura,
                    "sensacion_termica": sensacion_termica,
                    "humedad": campos[7].strip(),
                    "direccion_viento": direccion_viento,
                    "velocidad_viento": velocidad_viento,
                    "presion": presion,
                    "fecha_hora": fecha_hora
                }

                observaciones[ciudad] = datos_ciudad

    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{ruta}'")
        return observaciones, lineas_invalidas

    return observaciones, lineas_invalidas

def cantidad_ciudades(observaciones: dict) -> int:
    return len(observaciones)

def cant_ciudades_comp(observaciones: dict) -> int:
    completas = 0
    for datos in observaciones.values():
        falta = any(valor is None for valor in datos.values())
        if not falta:
            completas += 1
    return completas

def top_n_ciudades(observaciones: dict, campo: str, n: int, descendente: bool = True) -> list:
    pares = []
    for ciudad, datos in observaciones.items():
        if datos[campo] is not None:
            pares.append((datos[campo], ciudad))

    pares.sort(reverse=descendente)

    top = pares[:n]

    ciudades = []
    for valor, ciudad in top:
        ciudades.append(ciudad)

    return ciudades

def faltantes_por_campo(observaciones: dict) -> dict:
    if not observaciones:
        return {}

    primera_ciudad = next(iter(observaciones.values()))
    campos = list(primera_ciudad.keys())

    resultado ={}
    for campo in campos:
        ciudades_con_faltante =[]
        for ciudad, datos in observaciones.items():
            if datos[campo] is None:
                ciudades_con_faltante.append(ciudad)
        resultado[campo] = {
            "cantidad": len(ciudades_con_faltante),
            "ciudades": ciudades_con_faltante
        }
    return resultado

def mostrar_resumen(observaciones: dict, lineas_invalidas: list) -> None:
    print('=' * 40)
    print('RESUMEN DE OBSERVACIONES SMN')
    print('=' * 40)

    print(f"Ciudades leídas: {cantidad_ciudades(observaciones)}")
    print(f"Ciudades con datos completos: {cant_ciudades_comp(observaciones)}")   

    print(f"Líneas inválidas: {len(lineas_invalidas)}")
    if lineas_invalidas:
        print(f"  (cantidad de campos encontrados en cada una: {lineas_invalidas})")

    print("Datos faltantes por campo:")
    faltantes = faltantes_por_campo(observaciones)
    for campo, info in faltantes.items():
        print(f"  {campo}: {info['cantidad']} faltantes")

    print("Extremos:")
    print(f"  Ciudad más cálida: {top_n_ciudades(observaciones, 'temperatura', 1)}")
    print(f"  Ciudad más fría: {top_n_ciudades(observaciones, 'temperatura', 1, descendente=False)}")
    print(f"  Ciudad con más viento: {top_n_ciudades(observaciones, 'velocidad_viento', 1)}")
    print(f"  Ciudad con menos viento: {top_n_ciudades(observaciones, 'velocidad_viento', 1, descendente=False)}")

    print("Top 5 rankings:")
    print(f"  Más cálidas: {top_n_ciudades(observaciones, 'temperatura', 5)}")
    print(f"  Más frías: {top_n_ciudades(observaciones, 'temperatura', 5, descendente=False)}")
    print(f"  Más viento: {top_n_ciudades(observaciones, 'velocidad_viento', 5)}")
    print(f"  Menos viento: {top_n_ciudades(observaciones, 'velocidad_viento', 5, descendente=False)}")

if __name__ == "__main__":
    resultado, lineas_invalidas = leer_observaciones("datos/estado_tiempo.txt")
    mostrar_resumen(resultado, lineas_invalidas)
    guardar_json(resultado, "datos/observaciones.json")