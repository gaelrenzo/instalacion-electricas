# Propuesta Técnica: Motor Dinámico de Cálculos Eléctricos
**Proyecto:** Herramientas de Cálculo Reutilizables para Instalaciones Eléctricas Domiciliarias

Para eliminar la dependencia eterna de plantillas Excel (que suelen contener fórmulas ocultas, rígidas o con errores como el factor de caída de tensión monofásico), se propone el desarrollo de un **motor de cálculo programático en Python** (Fase 1) y una **interfaz web local ligera** (Fase 2) para ingresar datos de manera interactiva.

---

## 1. Arquitectura de la Solución

```
                                  +-----------------------+
                                  |   Archivo de Entrada  |
                                  |   (JSON o YAML)       |
                                  +-----------+-----------+
                                              |
                                              v
  +-------------------------+     +-----------+-----------+
  |  Interfaz Web Local     |     |   Motor de Cálculo    |
  |  (FastAPI / HTML + JS)  +---->|   en Python (core)    |
  |      [Fase 2]           |     |       [Fase 1]        |
  +-------------------------+     +-----------+-----------+
                                              |
                                              +---> [Cálculos del CNE]
                                              +---> [Caída de Tensión (1F/3F)]
                                              +---> [Coordinación Ib <= In <= Iz]
                                              |
                                              v
                                  +-----------+-----------+
                                  |  Archivos de Salida   |
                                  |  - Tablas LaTeX (.tex)|
                                  |  - JSON de Resultados |
                                  +-----------------------+
```

---

## 2. Fase 1: Motor Core en Python (Recomendado)

El script en Python recibirá un archivo JSON con los datos del proyecto, procesará las fórmulas y generará el informe técnico y las tablas LaTeX listas para compilar.

### Estructura de Datos de Entrada (`proyecto_input.json`)
```json
{
  "proyecto": "Instalaciones Eléctricas Vivienda Aquiles",
  "parametros_sistema": {
    "tension": 220,
    "frecuencia": 60,
    "fases": 1,
    "cos_phi": 0.90,
    "resistividad_cobre": 0.0178
  },
  "vivienda": {
    "pisos": 2,
    "area_piso_1": 80.0,
    "area_piso_2": 120.0
  },
  "cargas_especiales": [
    {"nombre": "Cocina Amplia 2do Piso", "potencia_w": 3400, "factor_demanda": 0.8, "circuito": "C6"},
    {"nombre": "Lavadora", "potencia_w": 800, "factor_demanda": 0.8, "circuito": "C7"},
    {"nombre": "Bomba de Agua", "potencia_w": 746, "factor_demanda": 1.0, "circuito": "C8"}
  ],
  "ambientes": [
    {
      "piso": 1,
      "nombre": "Cuarto 1 Grande",
      "puntos_luz": 2,
      "potencia_luz_w": 12,
      "tomacorrientes": 3,
      "potencia_toma_w": 180,
      "circuito_luz": "C1",
      "circuito_toma": "C2"
    }
  ]
}
```

### Funciones Principales del Engine Python
1. **`calcular_demanda_cne_area(vivienda)`**:
   Aplica la Regla 050-200(1)(a)(i-ii) para determinar el presupuesto de potencia por área techada:
   - Primeros 90 m² = 2500 W.
   - Exceso de 90 m² hasta 180 m² = 1000 W.
   - Exceso de 180 m² hasta 270 m² = 1000 W.
2. **`calcular_demanda_circuitos(ambientes, cargas_especiales)`**:
   Agrupa las cargas reales por circuito derivado, suma las potencias instaladas y aplica los factores de demanda del circuito ($f_{d,\text{alumbrado}} = 1.0$, $f_{d,\text{tomas}} = 0.7$, $f_{d,\text{cocina}} = 0.8$).
3. **`dimensionar_conductores_y_tuberias(circuitos)`**:
   - Calcula $I_n = P_{\text{dem}} / (V \cdot \cos\phi)$.
   - Calcula $I_d = 1.25 \times I_n$.
   - Busca en un diccionario de ampacidades el conductor mínimo que cumple con $I_z \geq I_d$.
   - Determina el diámetro mínimo de la tubería PVC según la cantidad y sección de cables.
4. **`verificar_caida_tension(circuitos)`**:
   Aplica de forma estricta la fórmula monofásica corregida:
   $$
   \Delta V = \frac{2 \times L \times I_b \times \rho}{S}
   $$
   Verifica que $\%\Delta V \leq 2.5\%$.
5. **`generar_latex()`**:
   Genera directamente archivos `.tex` con la estructura de `longtable` y `booktabs` listos para ser leídos mediante `\input{}` en el documento LaTeX.

---

## 3. Fase 2: Interfaz Web Local (Opcional)

Si el motor en Python funciona de manera robusta, se puede empaquetar una pequeña aplicación web local usando **FastAPI** para el backend y una plantilla HTML estática con Tailwind CSS para la interfaz:

- **Formulario Interactivo:** Permite añadir pisos y habitaciones dinámicamente, y añadir cargas especiales desde un menú desplegable (bomba de agua, lavadora, secadora, cocina, terma).
- **Visualización en Tiempo Real:** Muestra el diagrama de bloques del tablero general y los calibres de las llaves resultantes de forma gráfica.
- **Exportación:** Un botón para descargar directamente el JSON del proyecto y las tablas LaTeX pregeneradas.
