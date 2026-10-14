# Conciliación KML–GISEM — Rev. 3

**Fecha:** 14-10-2026. **Fuentes:** KML original inalterado, derived/route.json (ruta inferida sobre GISEM), EPSG:32719. Los resultados con seis decimales están en derived/reconciliacion_corredores_rev3.json; no representan precisión de levantamiento.

| Concepto | Metros | Clase |
|---|---:|---|
| Suma de cuatro polilíneas KML | 13 939,512 | Calculado |
| Eje GIS publicado en Rev. 2 | 13 834,030 | Calculado y redondeado |
| Diferencia publicada | **105,482** | Calculado |
| Distancia recta entre extremos de segmentos KML | 14,133 + 43,965 + 6,979 = **65,077** | Calculado, trayectoria no comprobada |
| Resta 105,482 − 65,077 | **40,405** | Solo identidad aritmética; **no es longitud de obra ni un tramo localizado** |
| Longitud KML si se insertaran tres cuerdas rectas | 14 004,589 | Escenario geométrico no validado |
| Diferencia de ese escenario frente al GIS | 170,559 | Escenario geométrico no validado |

Los valores originales de geometría dan 13 939,511910 m y 13 834,028618 m: diferencia **105,483292 m**. La suma no redondeada de las brechas es **65,077277 m** y su resta es **40,406015 m**. El cambio de 0,001 m frente a las cifras publicadas deriva del redondeo del GIS a 13 834,030 m. Ninguna de las dos restas separa físicamente la diferencia: las brechas **no estaban sumadas** a los 13 939,512 m iniciales. La divergencia proviene también de ejes, extremos y detalle de digitalización distintos.

## Localización de las discrepancias

| Segmento | Longitud KML UTM (m) | Distancia de sus extremos al eje GIS (m) | Interpretación |
|---|---:|---:|---|
| 1 | 255,990 | 190,0 / 116,8 | Arranque KML separado del eje GIS anterior |
| 2 | 4 132,229 | 117,2 / 17,3 | Convergencia parcial; trazados no idénticos |
| 3 | 4 578,385 | 45,8 / 269,3 | Divergencia fuerte hacia el último empalme |
| 4 | 4 972,908 | 269,1 / 71,0 | Continúa con otro eje y termina separado del GIS |

**Empalme 1:** 14,133 m entre extremos; ambos están a unos 117 m del GIS y se proyectan a la misma progresiva GIS. El KML no indica cómo conectarlos. **Empalme 2:** 43,965 m de separación recta; sus proyecciones sobre el GIS avanzan 33,489 m. Falta levantar el enlace real. **Empalme 3:** los extremos se separan 6,979 m, pero las líneas 3 y 4 se intersecan: el cruce está 1,781 m antes del final de la línea 3 y 5,271 m después del inicio de la línea 4. El orden, duplicidad y continuidad deben comprobarse en campo; no se recortaron segmentos.

Las proyecciones de puntos KML al GIS son diagnósticos de proximidad, no estaciones homólogas garantizadas. La longitud GIS usa 152 coordenadas de una ruta inferida sobre tramos publicados; el KML manual tiene 187 vértices en cuatro polilíneas. No procede repartir los 40,405 m entre segmentos ni corregir un eje para igualar al otro. La decisión requiere levantamiento y confirmación del titular sobre la red existente y el alcance de nueva obra.
