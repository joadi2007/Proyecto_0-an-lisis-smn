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
                presion = float(campos[9].strip())
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

    print(f"Líneas inválidas encontradas: {lineas_invalidas}")
    return observaciones

if __name__ == "__main__":
    resultado = leer_observaciones("datos/estado_tiempo.txt")
    print(resultado["Azul"])