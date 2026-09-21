# Análisis de observaciones meteorológicas del SMN

Trabajo Práctico — Programación 1 (Comisión 2)

## Descripción

Herramienta de línea de comandos que lee el archivo de observaciones actuales
del Servicio Meteorológico Nacional (SMN), arma un diccionario indexado por
ciudad/estación, y calcula estadísticas sobre esos datos: estaciones leídas,
datos faltantes por campo, líneas mal formadas, temperaturas y vientos
extremos, y rankings de las ciudades más cálidas/frías y con más/menos viento.

Además, exporta los datos procesados a un archivo JSON para uso en futuros
trabajos prácticos.

## Cómo ejecutarlo

```bash
python analisis_smn.py
```

El programa lee por defecto `datos/estado_tiempo.txt`. Al finalizar, muestra
un resumen por pantalla y genera `datos/observaciones.json` con los datos ya
procesados (este archivo se regenera en cada ejecución y no está versionado
en el repositorio — ver `.gitignore`).

## Cómo conseguir el archivo de entrada

1. Ir a la página de descarga de datos del SMN: <https://www.smn.gob.ar/descarga-de-datos>
2. Buscar la sección de **observaciones actuales** y descargar el archivo comprimido (`.rar`).
3. Descomprimirlo (en Mac, si el Finder no lo abre solo, se puede usar una app como The Unarchiver).
4. Copiar el `.txt` que queda adentro a la carpeta `datos/` del repositorio, con el nombre `estado_tiempo.txt`.

El archivo cambia constantemente porque son datos en vivo, así que cada
ejecución puede reflejar una "foto" distinta según el momento de la descarga.


## Decisiones de diseño

- El campo de viento `"Calma"` se representa con dirección `"Calma"` y
  velocidad `0` (en vez de `None`), para simplificar los cálculos de
  extremos y rankings sin tener que filtrar casos especiales.
- Los campos numéricos que no se pudieron convertir (por dato faltante o
  formato inesperado, como `"No se calcula"` o valores con sufijos extraños)
  se representan como `None`.