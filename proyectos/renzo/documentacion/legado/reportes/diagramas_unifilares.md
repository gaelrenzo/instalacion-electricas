# DIAGRAMAS UNIFILARES DEL PROYECTO
## Proyecto: Instalación Eléctrica Residencial - Vivienda Unifamiliar de 3 Pisos

Este documento detalla el esquema de conexión unifilar de la vivienda unifamiliar de tres pisos. Se incluye el Diagrama Unifilar General del Proyecto y los diagramas unifilares de distribución de cada uno de los niveles (TG-01, TD-01, TD-02).

---

### 1. Diagrama Unifilar General del Proyecto

A continuación se presenta el flujo de alimentación general desde la acometida de la red pública, pasando por el medidor, el Tablero General y los Subtableros secundarios de distribución:

```mermaid
graph TD
    Acometida["Acometida 220V Monofásica <br> (Red de Distribución Pública)"]
    --> Medidor["Medidor wh <br> (Ubicado en Fachada)"]
    --> ITM_Gral["Interruptor General Termomagnético <br> 2P - 32A"]
    --> ID_Gral["Interruptor Diferencial Principal <br> 2P - 40A / 30mA"]
    --> TG01["Tablero General: TG-01 <br> (Primer Piso)"]

    TG01 --> C1["Circuito C1: Alumbrado 1er Piso <br> ITM 2P-10A <br> Cable 3x1.5 mm² Cu (F+N+PE)"]
    TG01 --> C2["Circuito C2: Tomacorrientes 1er Piso <br> ITM 2P-16A / ID 2P-25A-30mA <br> Cable 3x2.5 mm² Cu (F+N+PE)"]
    TG01 --> C3["Circuito C3: Tomacorrientes Cocina <br> ITM 2P-20A / ID 2P-25A-30mA <br> Cable 3x2.5 mm² Cu (F+N+PE)"]
    
    TG01 --> Sub_TD01["Sub-alimentador TD-01 <br> ITM 2P-25A <br> Cable 3x6 mm² Cu (F+N+PE)"]
    TG01 --> Sub_TD02["Sub-alimentador TD-02 <br> ITM 2P-25A <br> Cable 3x6 mm² Cu (F+N+PE)"]

    Sub_TD01 --> TD01["Subtablero de Distribución: TD-01 <br> (Segundo Piso)"]
    Sub_TD02 --> TD02["Subtablero de Distribución: TD-02 <br> (Tercer Piso)"]

    TD01 --> C4["Circuito C4: Alumbrado 2do Piso <br> ITM 2P-10A <br> Cable 3x1.5 mm² Cu (F+N+PE)"]
    TD01 --> C5["Circuito C5: Tomacorrientes 2do Piso <br> ITM 2P-16A / ID 2P-25A-30mA <br> Cable 3x2.5 mm² Cu (F+N+PE)"]

    TD02 --> C6["Circuito C6: Alumbrado 3er Piso <br> ITM 2P-10A <br> Cable 3x1.5 mm² Cu (F+N+PE)"]
    TD02 --> C7["Circuito C7: Tomacorrientes 3er Piso <br> ITM 2P-16A / ID 2P-25A-30mA <br> Cable 3x2.5 mm² Cu (F+N+PE)"]
    
    SPAT["Sistema de Puesta a Tierra <br> (Varilla de Cobre 5/8')"] --> TG01
```

---

### 2. Diagrama Unifilar del Primer Piso (Tablero General TG-01)

El Tablero General (TG-01) recibe la acometida de la calle y distribuye el alumbrado y tomacorrientes del primer piso, además de las alimentaciones para los pisos superiores.

```text
       Línea de Acometida (Monofásico 220V, 60Hz)
                    │
           [Medidor Wh en Fachada]
                    │
            [ITM General 2P-32A]
                    │
          [ID Principal 2P-40A / 30mA]
                    │
        ┌───────────┴────────────────────────────────────────┐
        │                 TABLERO GENERAL TG-01             │
        ├────────────────────────────────────────────────────┤
        │  [Barra de Neutro]        [Barra de Tierra (PE)]   │
        │         │                          │               │
        │         │                          └────── Pozo    │
        │         │                                  Tierra  │
        ├─────────┼──────────┬──────────┬──────────┬─────────┤
        │         │          │          │          │         │
      [C1]      [C2]       [C3]    [Alim. TD01] [Alim. TD02] │
    Alumbrado  T.C. Gral   Cocina   Piso 2 sub   Piso 3 sub  │
     2P-10A    2P-16A      2P-20A     2P-25A       2P-25A    │
        │         │          │          │            │       │
      ID-25A    ID-25A     ID-25A       │            │       │
     (30 mA)   (30 mA)    (30 mA)       │            │       │
        │         │          │          │            │       │
    3x1.5 mm²  3x2.5 mm²  3x2.5 mm²  3x6.0 mm²    3x6.0 mm²  │
     (PVC 3/4") (PVC 3/4") (PVC 3/4") (PVC 1")     (PVC 1")  │
        │         │          │          │            │       │
      Luz       Tomas      Tomas      A TD-01      A TD-02   │
        └─────────┴──────────┴──────────┴────────────┘       
```

---

### 3. Diagrama Unifilar del Segundo Piso (Subtablero TD-01)

El Subtablero 1 (TD-01) está ubicado en el hall del segundo piso y distribuye la energía para las luminarias y tomacorrientes del nivel intermedio.

```text
                  Alimentación desde TG-01
                             │
                      [Cable 3x6 mm²]
                             │
                     [ITM General 2P-25A]
                             │
        ┌────────────────────┴──────────────────────┐
        │            SUBTABLERO DE DISTRIBUCIÓN     │
        │                     TD-01                 │
        ├───────────────────────────────────────────┤
        │                                           │
      [C4]                                        [C5]
    Alumbrado                                 Tomacorrientes
     2P-10A                                      2P-16A
        │                                           │
        │                                         ID-25A
        │                                        (30 mA)
        │                                           │
    3x1.5 mm²                                   3x2.5 mm²
    (PVC 3/4")                                  (PVC 3/4")
        │                                           │
     Luz 2do Piso                               Tomas 2do Piso
```

---

### 4. Diagrama Unifilar del Tercer Piso (Subtablero TD-02)

El Subtablero 2 (TD-02) se ubica en el pasadizo del tercer piso, controlando de manera local las luminarias y tomacorrientes de las habitaciones superiores.

```text
                  Alimentación desde TG-01
                             │
                      [Cable 3x6 mm²]
                             │
                     [ITM General 2P-25A]
                             │
        ┌────────────────────┴──────────────────────┐
        │            SUBTABLERO DE DISTRIBUCIÓN     │
        │                     TD-02                 │
        ├───────────────────────────────────────────┤
        │                                           │
      [C6]                                        [C7]
    Alumbrado                                 Tomacorrientes
     2P-10A                                      2P-16A
        │                                           │
        │                                         ID-25A
        │                                        (30 mA)
        │                                           │
    3x1.5 mm²                                   3x2.5 mm²
    (PVC 3/4")                                  (PVC 3/4")
        │                                           │
     Luz 3er Piso                               Tomas 3er Piso
```

---

### 5. Resumen de Protección de Personas (Interruptores Diferenciales)
* **Principio de Funcionamiento:** Los interruptores diferenciales (ID) de **30 mA** instalados protegen de forma directa a las personas contra contactos indirectos y fugas a tierra.
* **Distribución:** Cada circuito de tomacorrientes (`C2`, `C3`, `C5`, `C7`) dispone de un diferencial asociado de **2P - 25 A / 30 mA**, lo que asegura que una falla en un tomacorriente no afecte al alumbrado.
