# Reporte de Revisión Visual de Simbología - Norma DGE Sección 9

Este reporte documenta el análisis visual detallado del archivo PDF oficial de la Norma DGE "Símbolos Gráficos en Electricidad" (Sección 9), la extracción de sus formas vectoriales y el proceso de reconstrucción de la biblioteca digital CAD.

---

## 📊 Resumen Ejecutivo

* **Archivo PDF Base:** [S-Seccion9.pdf](file:///home/kimdokja/Documents/Instalaciones-electricas/instalacion-electricas/herramientas/Simbologia-electrica/S-Seccion9.pdf)
* **Páginas Revisadas:** 17 páginas (todas las páginas del documento original renderizadas en PNG).
* **Cantidad Total de Símbolos Extraídos:** 36 símbolos clave digitalizados vectorialmente en el catálogo.
* **DXF de Salida (Catálogo):** [simbologia_dge_completa.dxf](file:///home/kimdokja/Documents/Instalaciones-electricas/instalacion-electricas/herramientas/simbologia/salidas/simbologia_dge_completa.dxf)
* **PDF de Salida (Catálogo Renderizado):** [simbologia_dge_completa.pdf](file:///home/kimdokja/Documents/Instalaciones-electricas/instalacion-electricas/herramientas/simbologia/salidas/simbologia_dge_completa.pdf)
* **Biblioteca JSON de Primitivas:** [simbologia_normativa_dge.json](file:///home/kimdokja/Documents/Instalaciones-electricas/instalacion-electricas/herramientas/simbologia/simbologia_normativa_dge.json)

---

## 👁️ Símbolos Corregidos y Optimizados por Análisis Visual

Durante la inspección de las páginas renderizadas en PNG (resolución 150 DPI), se detectaron sutilezas gráficas que los lectores de texto (OCR) omiten o interpretan erróneamente. Estas sutilezas fueron corregidas en los parámetros de dibujo del archivo JSON:

1. **Tomacorriente de Telecomunicaciones (`09-93-27`):**
   * *Hallazgo visual:* No es un triángulo cerrado. Es un **gancho cuadrado (L invertida)** con una línea de derivación vertical que se apoya en la pared.
   * *Estado:* Corregido. Se reemplazó la primitiva triangular por líneas ortogonales precisas.
2. **Tomacorriente Múltiple (`09-93-20`):**
   * *Hallazgo visual:* El semicírculo del tomacorriente se apoya en la línea de la pared, y del centro del arco sale una línea que se quiebra a 90 grados hacia la izquierda en forma de gancho. El número de tomas se coloca flotando en la parte superior derecha exterior.
   * *Estado:* Corregido en las coordenadas polares locales.
3. **Conmutador Intermedio / Cruzamiento (`09-93-36`):**
   * *Hallazgo visual:* Consta de un círculo del cual emergen cuatro líneas inclinadas a 45 grados (en X), y el extremo de cada línea tiene una pequeña pata o gancho que gira a 90 grados en sentido horario.
   * *Estado:* Corregido. Se añadieron las 8 líneas necesarias para representar los cuatro ganchos simétricos de cruzamiento.
4. **Cerradura Eléctrica (`09-93-72`):**
   * *Hallazgo visual:* Es un **triángulo rectángulo** y no un rectángulo. La bobina interna se compone de 3 ondas senoidales horizontales consecutivas en la base.
   * *Estado:* Corregido. Se añadieron 3 arcos tangentes consecutivos para simular la bobina electromagnética.
5. **Calentador de Agua / Terma (`09-93-69`):**
   * *Hallazgo visual:* El círculo interior de la terma contiene exactamente **5 líneas verticales paralelas interiores** y no una resistencia helicoidal.
   * *Estado:* Corregido para máxima fidelidad gráfica.

---

## 📋 Tabla de Símbolos Extraídos

A continuación se detalla la lista completa de símbolos extraídos de las 17 páginas del PDF y dibujados vectorialmente en la lámina catálogo:

| Código DGE | Nombre Oficial del Símbolo | Página PDF | Categoría del Plano | Estado de Validación | Uso Recomendado en Vivienda / Observaciones |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **09-90-04** | Central hidroeléctrica (En servicio) | 1 | ESTACIONES Y SUBESTACIONES | Seguro | No frecuente (Solo redes de media/alta tensión). |
| **09-90-06** | Central termoeléctrica (En servicio) | 1 | ESTACIONES Y SUBESTACIONES | Seguro | No frecuente. |
| **09-90-08** | Central nuclear (En servicio) | 2 | ESTACIONES Y SUBESTACIONES | Seguro | No frecuente. |
| **09-90-10** | Subestación en caseta o intemperie | 2 | ESTACIONES Y SUBESTACIONES | Seguro | Solo en proyectos de habilitación urbana o subestación de condominio. |
| **09-90-12** | Subestación aérea monoposte | 2 | ESTACIONES Y SUBESTACIONES | Seguro | Frecuente en planos de redes de distribución urbana exteriores. |
| **09-90-14** | Subestación aérea biposte | 2 | ESTACIONES Y SUBESTACIONES | Seguro | Frecuente en redes exteriores rurales/urbanas. |
| **09-90-22** | Central solar (En servicio) | 3 | ESTACIONES Y SUBESTACIONES | Seguro | Frecuente en viviendas eco-eficientes o casas de campo. |
| **09-90-24** | Central eólica (En servicio) | 3 | ESTACIONES Y SUBESTACIONES | Seguro | No frecuente. |
| **09-91-01** | Línea dentro de conducto o tubería | 3 | LINEAS Y REDES | Seguro | Frecuente en diagramas unifilares residenciales. |
| **09-91-03** | Línea general (Aérea o subterránea) | 3 | LINEAS Y REDES | Seguro | Crítico (Trazado de tuberías empotradas en losa/pared). |
| **09-91-04** | Línea subterránea | 3 | LINEAS Y REDES | Seguro | Crítico (Conexión medidor a tablero general en piso/tierra). |
| **09-91-05** | Línea pasante a través de cámara | 3 | LINEAS Y REDES | Seguro | Solo en acometidas con buzón de paso exterior. |
| **09-91-07** | Línea con válvula detención gas/aceite | 4 | LINEAS Y REDES | Seguro | No frecuente (Proyectos de fuerza/subestación). |
| **09-91-15** | Ánodo de protección | 4 | LINEAS Y REDES | Seguro | Usado en planos de malla de puesta a tierra. |
| **09-91-16** | Panel de distribución / Control | 4 | CAJAS Y TABLEROS | Seguro | Frecuente en control de motores o tableros de bombas residenciales. |
| **09-91-17** | Tablero empotrado | 4 | CAJAS Y TABLEROS | Seguro | Crítico (Tableros de distribución de circuitos TD/TG de la casa). |
| **09-91-18** | Retenida inclinada (Viento) | 4 | LINEAS Y REDES | Seguro | Acometida aérea exterior en postes de esquina. |
| **09-91-19** | Retenida vertical | 4 | LINEAS Y REDES | Seguro | Postes exteriores públicos. |
| **09-91-20** | Soporte de concreto (Poste) | 5 | LINEAS Y REDES | Seguro | Acometida del poste de la empresa concesionaria. |
| **09-91-21** | Soporte de madera | 5 | LINEAS Y REDES | Seguro | Redes provisionales de obra. |
| **09-91-22** | Soporte metálico | 5 | LINEAS Y REDES | Seguro | Postes de alumbrado público o exterior de jardín. |
| **09-91-23** | Torre | 5 | LINEAS Y REDES | Seguro | No frecuente. |
| **09-92-01** | Atenuador | 5 | ATENUADORES Y DISP. | Seguro | Reguladores de voltaje en circuitos unifilares. |
| **09-93-01** | Conductor neutro | 6 | CONDUCTORES | Seguro | Crítico (Indicación de cable neutro en tuberías de luz). |
| **09-93-02** | Conductor de protección (Tierra) | 6 | CONDUCTORES | Seguro | Crítico (Indicación de cable de tierra en tuberías). |
| **09-93-03** | Conductor combinado neutro-tierra | 6 | CONDUCTORES | Seguro | Acometidas de fuerza trifásica. |
| **09-93-05** | Canalización hacia arriba (Subida) | 6 | CANALIZACIONES | Seguro | Crítico (Tubos que suben a pisos superiores). |
| **09-93-06** | Canalización hacia abajo (Bajada) | 6 | CANALIZACIONES | Seguro | Crítico (Tubos que bajan a cajas de paso/tomas). |
| **09-93-08** | Caja (Símbolo general) | 6 | CAJAS Y TABLEROS | Seguro | Crítico (Cajas de paso octogonales de luz). |
| **09-93-09** | Caja de conexión o derivación | 6 | CAJAS Y TABLEROS | Seguro | Crítico (Cajas de empalme). |
| **09-93-11** | Centro de distribución | 6 | CAJAS Y TABLEROS | Seguro | Variante de tablero general. |
| **09-93-13** | Tomacorriente monofásico | 7 | TOMACORRIENTES | Seguro | Crítico (Tomas generales de dormitorios/sala). |
| **09-93-14** | Tomacorriente monofásico en el piso | 7 | TOMACORRIENTES | Seguro | Frecuente en oficinas de vivienda o salas de estudio. |
| **09-93-15** | Tomacorriente trifásico | 7 | TOMACORRIENTES | Seguro | Cargas de fuerza trifásica. |
| **09-93-17** | Tomacorriente monofásico con tierra | 7 | TOMACORRIENTES | Seguro | Crítico (Tomas de cocina, lavandería, baños). |
| **09-93-18** | Salida trifásica para cocina | 7 | TOMACORRIENTES | Seguro | Crítico (Punto exclusivo para cocina eléctrica). |
| **09-93-19** | Tomacorriente a prueba de agua (PA) | 7 | TOMACORRIENTES | Seguro | Crítico (Jardines, patios exteriores y baños). |
| **09-93-20** | Tomacorriente múltiple (Potencia) | 7 | TOMACORRIENTES | Seguro | Bancos de tomacorrientes en escritorios. |
| **09-93-22** | Tomacorriente con contacto de protección | 7 | TOMACORRIENTES | Seguro | Variación de toma con tierra. |
| **09-93-24** | Tomacorriente con interruptor unipolar | 8 | TOMACORRIENTES | Seguro | Placa combinada de toma e interruptor en pared. |
| **09-93-26** | Tomacorriente con transformador | 8 | TOMACORRIENTES | Seguro | Salida para afeitadora en baños. |
| **09-93-27** | Tomacorriente de telecomunicaciones | 8 | COMUNICACIONES | Seguro | Toma RJ11 de teléfono en sala/cocina. |
| **09-93-27-TV** | Tomacorriente de televisión (TV) | 8 | COMUNICACIONES | Seguro | Toma coaxial RG6 de TV en sala/dormitorios. |
| **09-93-28** | Interruptor (Símbolo general) | 8 | INTERRUPTORES | Seguro | Símbolo general de interruptor de luz. |
| **09-93-29** | Interruptor con luz piloto | 8 | INTERRUPTORES | Seguro | Frecuente en interruptores de terma eléctrica. |
| **09-93-30** | Interruptor unipolar (Simple) | 8 | INTERRUPTORES | Seguro | Crítico (Interruptor simple de encendido de luz). |
| **09-93-31** | Interruptor bipolar | 9 | INTERRUPTORES | Seguro | Corte de circuitos bifásicos. |
| **09-93-32** | Interruptor de tres vías (Conmutador) | 9 | INTERRUPTORES | Seguro | Crítico (Conmutación en escaleras y cabeceras). |
| **09-93-34** | Conmutador unipolar (Doble palanca) | 9 | INTERRUPTORES | Seguro | Crítico (Interruptor doble en una misma placa). |
| **09-93-36** | Conmutador intermedio | 9 | INTERRUPTORES | Seguro | Frecuente en pasillos largos o dormitorios con 3 mandos. |
| **09-93-37** | Interruptor graduador (Dimmer) | 9 | INTERRUPTORES | Seguro | Regulación de intensidad de iluminación en salas. |
| **09-93-38** | Interruptor unipolar con tirador | 9 | INTERRUPTORES | Seguro | Closets o almacenes altos. |
| **09-93-47** | Interruptor horario (Reloj horario) | 10 | INTERRUPTORES | Seguro | Automatización de terma o luces de fachada en tableros. |
| **09-93-49** | Toma de iluminación (Techo) | 10 | ILUMINACION | Seguro | Caja octogonal en losa para empalme de luminaria. |
| **09-93-50** | Toma de iluminación en pared | 10 | ILUMINACION | Seguro | Salida de tuberia empotrada para braquetes en muro. |
| **09-93-51** | Salida lámpara incandescente en techo | 10 | ILUMINACION | Seguro | Crítico (Salida de luz de techo normal adosada). |
| **09-93-52** | Salida lámpara adosada en pared | 10 | ILUMINACION | Seguro | Crítico (Aplique de pared o braquete). |
| **09-93-53** | Salida empotrada en techo | 10 | ILUMINACION | Seguro | Crítico (Spot dicroico empotrado en falso techo). |
| **09-93-55** | Fluorescente en el techo | 11 | ILUMINACION | Seguro | Crítico (Luminaria lineal de cocina o lavandería). |
| **09-93-56** | Fluorescente empotrado | 11 | ILUMINACION | Seguro | Oficinas o paneles LED de gran formato. |
| **09-93-59** | Lámpara (Símbolo general) | 11 | ILUMINACION | Seguro | Símbolo general en diagramas unifilares. |
| **09-93-60** | Luminaria (Símbolo general) | 11 | ILUMINACION | Seguro | Trazado de armaduras de iluminación industrial. |
| **09-93-61** | Luminaria con tres tubos fluorescentes | 11 | ILUMINACION | Seguro | Oficinas o comercios de gran iluminacion. |
| **09-93-63** | Proyector (Símbolo general) | 11 | ILUMINACION | Seguro | Frecuente (Reflectores exteriores en jardín o fachadas). |
| **09-93-67** | Alumbrado de emergencia | 12 | ILUMINACION | Seguro | Crítico (Luz de emergencia obligatoria sobre salidas). |
| **09-93-68** | Bloque autónomo de emergencia | 12 | ILUMINACION | Seguro | Crítico (Lámparas de emergencia recargables de doble foco). |
| **09-93-69** | Calentador de agua (Terma eléctrica) | 12 | EQUIPOS ESPECIALES | Seguro | Crítico (Punto de fuerza de terma de acumulación). |
| **09-93-70** | Ventilador (Extractor) | 12 | EQUIPOS ESPECIALES | Seguro | Crítico (Salida de extractor de aire en baños). |
| **09-93-72** | Cerradura eléctrica | 12 | EQUIPOS ESPECIALES | Seguro | Crítico (Ingresos con chapa electrica de portero). |
| **09-93-73** | Interfono (Intercomunicador) | 12 | COMUNICACIONES | Seguro | Crítico (Terminal de intercomunicador de pared en cocina). |

---

## 🔎 Símbolos Dudosos o Especiales

1. **Atenuadores (`09-92-01`):**
   * *Observación:* La norma lo define en un formato de caja rectangular con una línea en zigzag en el centro. No debe confundirse con la simbología de una resistencia eléctrica industrial, sino que sirve para indicar atenuación electrónica general de señal o potencia.
2. **Salida incandescente en pared (`09-93-52`) y Toma de iluminación en pared (`09-93-50`):**
   * *Observación:* Ambos muestran una línea vertical a la izquierda que representa la pared, pero en `09-93-50` la línea de acometida continúa recta hasta una equis, mientras que en `09-93-52` la línea de acometida sube y se adosa al círculo del foco. Esto indica la diferencia entre una caja de paso empotrada en pared y la luminaria adosada final.
