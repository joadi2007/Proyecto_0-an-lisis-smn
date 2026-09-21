from datetime import datetime

MESES_ESP = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, 
    "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11,
    "diciembre": 12
    }

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
    lineas_invalidas = 0

    try:
        with open(ruta, 'r', encoding='latin-1') as archivo:
            for linea in archivo:
                campos = linea.strip().split(";")

                if len(campos) != 10:
                    lineas_invalidas += 1
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
        return observaciones

    print(f"Líneas inválidas encontradas: {lineas_invalidas}")
    return observaciones

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
            pares.append((ciudad, datos[campo]))
    pares_ordenados = sorted(pares, key = lambda par: par[1], reverse= descendente)

    top = pares_ordenados[:n]

    ciudades = [ciudad for ciudad, valor in top]
    return ciudades


if __name__ == "__main__":
    resultado = leer_observaciones("datos/estado_tiempo.txt")
    print(cantidad_ciudades(resultado))
    print(cant_ciudades_comp(resultado))

    print(top_n_ciudades(resultado, "temperatura", 5))
    print(top_n_ciudades(resultado, "temperatura", 5, descendente=False))
    print(top_n_ciudades(resultado, "velocidad_viento", 5))
    print(top_n_ciudades(resultado, "velocidad_viento", 5, descendente=False))


