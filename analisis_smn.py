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

def temp_max(observaciones: dict) -> list:
    temp = []
    for datos in observaciones.values():
        if datos['temperatura'] is not None:
            temp.append(datos['temperatura'])
    temp_max = max(temp)

    ciudades = []
    for ciudad, datos in observaciones.items():
        if datos['temperatura'] == temp_max:
            ciudades.append(ciudad)
    return ciudades

def temp_min(observaciones: dict) -> list:
    temp = []
    for datos in observaciones.values():
        if datos['temperatura'] is not None:
            temp.append(datos['temperatura'])
    temp_min = min(temp)

    ciudades = []
    for ciudad, datos in observaciones.items():
        if datos['temperatura'] == temp_min:
            ciudades.append(ciudad)

    return ciudades   


if __name__ == "__main__":
    resultado = leer_observaciones("datos/estado_tiempo.txt")
    print(cantidad_ciudades(resultado))
    print(cant_ciudades_comp(resultado))
    print(temp_max(resultado))
    print(temp_min(resultado))
