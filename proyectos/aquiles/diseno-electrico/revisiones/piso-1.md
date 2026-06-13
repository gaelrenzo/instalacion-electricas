# Revisión Eléctrico Piso 1 — v6

| Campo               | Valor                                      |
|---------------------|--------------------------------------------|
| **Versión**         | v6                                         |
| **Fecha**           | 2026-06-08                                 |
| **DXF maestro base**| `electrico_piso1_v4.dxf`                  |
| **JSON documentación** | `electrico_piso1_v6.json`              |
| **Autor**           | Asistente IA (documentación)               |

---

## Cambios realizados en v6

### 1. Luminarias — corrección de símbolo
- **Antes (v4):** símbolo de luminaria dibujado como **+** (cruz ortogonal)
- **Después (v6):** símbolo corregido a **X** (cruz diagonal, 45°)
- Aplica a todas las luminarias: L-P1-01, L-P1-02, L-P1-03, L-P1-05
- Posiciones sin cambios; solo se modificó la geometría del símbolo

### 2. SPAT — Sistema de Puesta a Tierra
- **Agregado** en coordenadas **(15.45, 3.60)**, cerca del medidor
- Capa: `ELEC_PUESTA_TIERRA`
- Símbolo: triángulo de tierra con etiqueta "SPAT"
- Conectado al tablero general (TG)

### 3. Conductor PE (protección a tierra)
- Ruta trazada desde SPAT hasta TG:
  - `(15.45, 3.90)` → `(15.45, 4.75)` → `(14.35, 4.75)`
- Tipo de línea: `DASHED`
- Capa: `ELEC_PUESTA_TIERRA`
- Circuito identificado como **PE**

### 4. Elementos preservados (sin cambios)
- ✅ Todos los interruptores (S-P1-01 a S-P1-04)
- ✅ Todos los tomacorrientes (T-P1-01 a T-P1-09)
- ✅ Tablero general TG en (14.35, 4.75)
- ✅ Medidor M en (15.45, 4.75)
- ✅ Bomba exterior B-P1 en (-0.55, 1.0)
- ✅ Todas las rutas de circuitos C1, C2, C3, C8
- ✅ Ruta medidor-TG
- ✅ Línea límite de techo

### 5. Base arquitectónica
- **Sin cambios** — se mantiene `piso1_v3.dxf` como base

---

## Verificación

- ✅ Revisión visual por PNG confirmada
- ✅ Entidades contadas y verificadas contra v4
- ✅ No se eliminaron ni movieron elementos existentes
- ✅ SPAT visible y correctamente posicionado en zona del medidor
- ✅ Conductor PE visible con línea discontinua desde SPAT a TG

---

## Pendientes

- ⏳ **Verificación con telurómetro in situ** — medir resistencia de puesta a tierra
- ⏳ Confirmar calibre del conductor PE según normativa local
- ⏳ Validar profundidad y tipo de electrodo de tierra en campo

---

## Nota importante

> Este archivo y su JSON asociado (`electrico_piso1_v6.json`) son **documentación únicamente**.
> El DXF maestro (`electrico_piso1_v4.dxf` editado como v6) es la **fuente de verdad**.
> Los JSON **NO regeneran** el DXF — solo documentan su contenido para referencia.
