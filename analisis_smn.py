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

    with open(ruta, 'r', encoding='latin-1') as archivo:
        for linea in archivo:
            campos = linea.strip().split(";")

            ciudad = campos[0].strip()
            direccion_viento, velocidad_viento = separar_viento(campos[8])

            try:
                sensacion_termica = float(campos[6])
            except ValueError:
                sensacion_termica = None

            datos_ciudad = {
                "fecha": campos[1],
                "hora": campos[2],
                "condicion": campos[3],
                "visibilidad": campos[4],
                "temperatura": float(campos[5]),
                "sensacion_termica": sensacion_termica,
                "humedad": campos[7].strip(),
                "direccion_viento": direccion_viento,
                "velocidad_viento": velocidad_viento,
                "presion": campos[9].strip(), 
            }

            observaciones[ciudad] = datos_ciudad
    return observaciones

if __name__ == "__main__":
    resultado = leer_observaciones("datos/estado_tiempo.txt")
    print(resultado["Azul"])