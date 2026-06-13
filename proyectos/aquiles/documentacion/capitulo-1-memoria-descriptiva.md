# Capitulo I: Memoria descriptiva

## 1. Objetivo del capitulo

Presentar la descripcion general del mini proyecto de instalacion electrica domiciliaria, indicando ubicacion, alcance, caracteristicas de la vivienda, ambientes considerados, criterios de diseno y base normativa aplicable.

## 2. Estructura propuesta

| Seccion | Contenido a desarrollar | Fuente principal |
|---|---|---|
| 1.1 Introduccion | Presentacion del proyecto y finalidad academica | `informe_instalaciones_electricas.md` |
| 1.2 Objetivos | Objetivo general y objetivos especificos | `latex/capitulos/01-memoria-descriptiva.tex` |
| 1.3 Base normativa | CNE-U, EM.010 y normas complementarias | `normativas/fuentes-oficiales.md` |
| 1.4 Ubicacion | Direccion, distrito, provincia y departamento | Dato pendiente del estudiante |
| 1.5 Caracteristicas de la vivienda | Tipo, pisos, area, material y zona | `pautas-vivienda-2-pisos.md` |
| 1.6 Ambientes considerados | Primer piso: 2 cuartos grandes, cocina, pasadizo y escalera. Segundo piso: sala, 2 cuartos, cocina amplia, cuarto de uso varios y bano | `respuestas-cuestionario-aquiles.md` |
| 1.7 Alcance tecnico | Circuitos, tablero, protecciones, canalizaciones y puesta a tierra | `proyecto-casa/01-memoria-descriptiva/memoria-descriptiva.md` |
| 1.8 Criterios de diseno | Seguridad, sectorizacion, continuidad, mantenimiento | `latex/capitulos/01-memoria-descriptiva.tex` |
| 1.9 Restricciones | Trabajo academico, no expediente ejecutivo | `informe_instalaciones_electricas.md` |

## 3. Datos base a confirmar

| Dato | Valor actual | Estado |
|---|---|---|
| Ubicacion | Avenida Horacio con Jr. Marineros, manzana F7, lotes 11 y 12 | Definido |
| Distrito | San Miguel | Definido |
| Provincia | San Román | Definido |
| Departamento | Puno | Definido |
| Tipo de vivienda | Unifamiliar (casa grande) | Definido |
| Numero de pisos | 2 pisos | Definido para el avance |
| Area construida | Por definir (el primer piso tiene menos área que el segundo) | En proceso |
| Sistema electrico | Monofasico, 220 V, 60 Hz | Definido |
| Empresa distribuidora | Electro Puno | Definido |
| Material predominante | Ladrillo y concreto | Definido |
| Numero de miembros | 7 miembros | Definido para el avance |

## 4. Distribucion preliminar de ambientes

| Piso | Ambiente | Alumbrado preliminar | Tomacorrientes preliminares |
|---|---|---:|---:|
| Primer piso | Cuarto 1 grande | 2 focos | 3 tomacorrientes |
| Primer piso | Cuarto 2 grande | 2 focos | 3 tomacorrientes |
| Primer piso | Cocina | 2 focos | 1 tomacorriente |
| Primer piso | Pasadizo | 3 focos | 0 tomacorrientes |
| Primer piso / intermedio | Escalera o plataforma intermedia | 1 foco | 0 tomacorrientes |
| Segundo piso | Sala | 2 focos | Por definir |
| Segundo piso | Cuarto con cama 1 | 2 focos | Por definir |
| Segundo piso | Cuarto con cama 2 | 2 focos | Por definir |
| Segundo piso | Cocina amplia / zona de servicio | 2 focos | 4 tomacorrientes |
| Segundo piso | Cuarto de uso varios | 2 focos | Por definir |
| Segundo piso | Bano | 1 foco | 1 tomacorriente |

## 5. Cargas y criterios especiales identificados

| Elemento | Criterio preliminar |
|---|---|
| Cocina primer piso | Solo licuadora y artefactos pequenos |
| Cocina amplia segundo piso | Considerar microondas/horno, waflera y artefactos de consumo medio/alto |
| Lavadora | Prevista en segundo piso |
| Bomba de agua | Existe en exterior del primer piso, asociada a pozo |
| Terma | Solar, no electrica |
| Ducha electrica | No se considera |
| Puesta a tierra | La vivienda no cuenta con puesta a tierra; se propone incluir sistema de puesta a tierra |
| Croquis | Pendiente de dibujo manual y posterior digitalizacion |
| Dimensiones | Aproximadas, quedan en observacion |

## 6. Contenido minimo para entregar

- Descripcion clara del proyecto.
- Objetivo general y objetivos especificos.
- Tabla de caracteristicas de la vivienda.
- Tabla de ambientes considerados.
- Alcance de la instalacion electrica interior.
- Criterios tecnicos de seguridad.
- Base normativa resumida.
- Nota de que el trabajo es academico y requiere validacion profesional para ejecucion real.

## 7. Pendientes del capitulo

| Pendiente | Accion |
|---|---|
| Completar nombre del docente | Solicitar dato al estudiante |
| Confirmar provincia y distrito exactos | Validar ubicacion San Miguel / San Roman |
| Confirmar distribucion real por pisos | Usar croquis o plano arquitectonico propio |
| Definir area aproximada por piso | Usar croquis y medidas aproximadas |
| Completar tomacorrientes del segundo piso | Definir sala, cuartos y cuarto de uso varios |
| Definir ubicacion de tablero general | Marcarlo en el croquis |
| Definir tipo de canalizacion | Empotrada, superficial o mixta |
| Agregar numerales normativos | Revisar CNE-U y EM.010 |
| Verificar si el ingeniero exige cronograma o presupuesto dentro del alcance | Consultar indicaciones de clase |

## 8. Notas de Actualización de Planos (Versión 6)

La versión 6 (v6) se generó mediante edición directa sobre los DXF maestros v4, sin regenerar desde JSON. Los DXF v4 contenían correcciones manuales que debían preservarse.

Correcciones aplicadas en v6:
- **Puesta a Tierra (SPAT):** Se incorporó el símbolo de puesta a tierra en el plano del Piso 1, ubicado en (15.45, 3.60), cerca del medidor y del TG, en zona exterior/frontal. Se creó la capa `ELEC_PUESTA_TIERRA`. Se trazó conductor de protección PE desde el SPAT hasta el TG.
- **Simbología de Luminarias:** Se corrigió el símbolo de salidas de techo en **ambos pisos**. Las líneas ortogonales (+) fueron reemplazadas por diagonales (X/aspa), conforme al estándar DGE_09_93_51_SALIDA_TECHO. Se editaron 10 luminarias en Piso 1 y 12 luminarias en Piso 2.
- **Consistencia Segundo Piso:** Se verificó que el segundo piso use la misma simbología que el primero. Se creó la capa `ELEC_PUESTA_TIERRA` y se agregó nota de conductor PE proveniente del SPAT del Piso 1.
- **Elementos preservados:** Medidor (M), Tablero General (TG), Tablero T2, Ducto Vertical (VD), todos los circuitos C1-C8, canalizaciones, interruptores, tomacorrientes y arquitectura base. Ningún elemento fue eliminado ni reubicado.
- **Flujo aplicado:** DXF maestro v4 → copia a v6 → edición directa con ezdxf → exportación PDF con QCAD → revisión visual PNG.
