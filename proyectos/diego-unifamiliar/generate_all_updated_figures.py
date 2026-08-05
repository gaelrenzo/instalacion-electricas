import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

TARGET_DIR = "/storage/emulated/0/universida-datos/diego"
REPO_TARGET = "/storage/emulated/0/universida-datos/instalacion-electricas/proyectos/diego-unifamiliar"

# -----------------------------------------------------------------------------
# 1. DIAGRAMA UNIFILAR SIN PUESTA A TIERRA (QUITA LA PUESTA A TIERRA)
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 9.5), dpi=300)
ax.set_xlim(0, 12)
ax.set_ylim(0, 13.5)
ax.axis('off')

# Title & Metadata
ax.text(6, 13.0, "DIAGRAMA UNIFILAR DEL TABLERO GENERAL (TD)", fontsize=13, fontweight='bold', ha='center', color='#0F2043')
ax.text(6, 12.6, "VIVIENDA UNIFAMILIAR DE 3 NIVELES - SUMINISTRO TRIFÁSICO 220V 3Ø 60Hz", fontsize=9.5, ha='center', color='#184C78', fontweight='bold')
ax.text(6, 12.2, "Proyectista: CHARAJA MAMANI DIEGO JEFFERSON (Cód. 214254) | Docente: ING. VILLANUEVA CORNEJO MARCOS JOSE", fontsize=8, ha='center', color='#404040')

# Suministro y Acometida
ax.plot([6, 6], [11.9, 11.0], color='#0F2043', lw=2.5)
ax.text(6.2, 11.5, "ACOMETIDA BT - ELECTRO PUNO S.A.A.\nRed Pública Subterránea / Aérea 220V 3Ø 60Hz\nCable 3-1x10 mm² N2XH", fontsize=7.5, color='#0F2043')

# Caja de Medición
rect_m = patches.Rectangle((5.0, 10.2), 2.0, 0.8, edgecolor='#0F2043', facecolor='#F0F4F8', lw=1.8)
ax.add_patch(rect_m)
ax.text(6, 10.6, "CAJA DE MEDICIÓN L-T\nMedidor Eletrónico 3Ø", fontsize=7.5, fontweight='bold', ha='center', va='center', color='#0F2043')

# Alimentador General
ax.plot([6, 6], [10.2, 9.1], color='#0F2043', lw=2.5)
ax.text(6.2, 9.6, "ALIMENTADOR GENERAL (L = 15 m):\n3-1x10 mm² NH-80 en Tubo PVC-P (SAP) 25 mmØ (1\"Ø)\nΔV = 1.79 V (0.81% ≤ 2.5%)", fontsize=7, color='#184C78', fontweight='bold')

# Interruptor General ITM 3x40A
rect_itm = patches.Rectangle((4.8, 8.2), 2.4, 0.9, edgecolor='#0F2043', facecolor='#D9E2EC', lw=1.8)
ax.add_patch(rect_itm)
ax.text(6, 8.65, "INTERRUPTOR GENERAL (TD)\nITM 3 x 40 A / Curva C / Icu = 10 kA\nNorma IEC 60947-2 / IEC 60898", fontsize=7.5, fontweight='bold', ha='center', va='center', color='#0F2043')

# Down to Busbars
ax.plot([6, 6], [8.2, 7.3], color='#0F2043', lw=2.5)

# Busbars 3Ø
ax.plot([1.0, 11.0], [7.3, 7.3], color='#0F2043', lw=3.5)
ax.text(6, 7.5, "BARRAS COLECTORAS DE COBRE ELECTROLÍTICO 99.9% Cu (100 A)", fontsize=8, fontweight='bold', ha='center', color='#184C78')

# 8 Circuitos Derivados
ckts_detailed = [
    ("C-1", "Alum. y Tomac.\n1er Piso", "2.5 kW\n12.6A", "ITM 2x16A (6kA)\nID 2x25A 30mA", "2x2.5mm² NH80", "PVC-L 20mm"),
    ("C-2", "Alum./Tomac.\n2do y Azotea", "0.7 kW\n3.5A", "ITM 2x16A (6kA)\nID 2x25A 30mA", "2x2.5mm² NH80", "PVC-L 20mm"),
    ("C-3", "Cocina Eléctrica\n(1er Piso 3Ø)", "4.8 kW\n14.0A", "ITM 3x25A (6kA)\nID 3x32A 30mA", "3x6.0mm² NH80", "PVC-P 25mm"),
    ("C-4", "Terma Eléctrica\n(2do Piso)", "1.5 kW\n7.6A", "ITM 2x16A (6kA)\nID 2x25A 30mA", "2x4.0mm² NH80", "PVC-P 20mm"),
    ("C-5", "Electrobomba\n0.75 HP Cisterna", "0.75 kW\n3.8A", "ITM 2x16A (6kA)\nID 2x25A 30mA", "2x2.5mm² NH80", "PVC-P 20mm"),
    ("C-6", "Tomac. Cocina\nArtefactos", "0.75 kW\n3.8A", "ITM 2x20A (6kA)\nID 2x25A 30mA", "2x4.0mm² NH80", "PVC-P 20mm"),
    ("C-7", "Lavadora/Secad.\nAzotea", "1.75 kW\n8.8A", "ITM 2x20A (6kA)\nID 2x25A 30mA", "2x4.0mm² NH80", "PVC-P 20mm"),
    ("C-8", "Reserva Especial\nAmpliaciones", "0.75 kW\n3.8A", "ITM 2x20A (6kA)\n(Reserva)", "2x4.0mm² NH80", "PVC-P 20mm")
]

x_coords = np.linspace(1.1, 10.9, 8)

for i, (code, name, pwr, prot, cable, pipe) in enumerate(ckts_detailed):
    x = x_coords[i]
    ax.plot([x, x], [7.3, 6.2], color='#0F2043', lw=1.5)
    
    # Box Protecciones (ITM + ID)
    rect_p = patches.Rectangle((x-0.55, 4.7), 1.1, 1.5, edgecolor='#184C78', facecolor='#F0F4F8', lw=1.2)
    ax.add_patch(rect_p)
    ax.text(x, 5.45, f"{code}", fontsize=7.5, ha='center', va='center', fontweight='bold', color='#0F2043')
    ax.text(x, 5.05, prot, fontsize=5.8, ha='center', va='center')
    
    # Conductor info line
    ax.plot([x, x], [4.7, 3.3], color='#0F2043', lw=1.5)
    ax.text(x+0.05, 4.0, f"{cable}\n{pipe}", fontsize=5.5, ha='left', va='center', color='#2D3748', backgroundcolor='white')
    
    # Load Box
    rect_l = patches.Rectangle((x-0.6, 1.8), 1.2, 1.5, edgecolor='#0F2043', facecolor='#E2E8F0', lw=1.2)
    ax.add_patch(rect_l)
    ax.text(x, 2.7, name, fontsize=6.2, ha='center', va='center', fontweight='bold', color='#0F2043')
    ax.text(x, 2.1, pwr, fontsize=6, ha='center', va='center', color='#184C78', fontweight='bold')

plt.tight_layout()
fig_unifilar_path = os.path.join(TARGET_DIR, "fig_diagrama_unifilar.png")
plt.savefig(fig_unifilar_path, dpi=300)
plt.savefig(os.path.join(REPO_TARGET, "fig_diagrama_unifilar.png"), dpi=300)
plt.close()
print("Updated fig_diagrama_unifilar.png (sin puesta a tierra) generated.")


# -----------------------------------------------------------------------------
# 2. PLANO ARQUITECTÓNICO Y ELÉCTRICO DE DIEGO CHARAJA (LÁMINA A2 - ESCALA 1:50)
# -----------------------------------------------------------------------------
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 8), dpi=300)

for ax in [ax1, ax2, ax3]:
    ax.set_aspect('equal')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 16)
    ax.axis('off')

# LEVEL 1: PRIMER PISO
ax1.set_title("PRIMER PISO (LÁMINA A2)\nÁrea Social, Servicio y Cisterna", fontsize=10, fontweight='bold', color='#0F2043')
ax1.add_patch(patches.Rectangle((0.5, 0.5), 9.0, 14.5, edgecolor='#0F2043', facecolor='#F7FAFC', lw=2))

# Sub-rooms Level 1
ax1.add_patch(patches.Rectangle((1.0, 10.0), 4.0, 4.5, edgecolor='#4A5568', facecolor='#EDF2F7', lw=1))
ax1.text(3.0, 12.25, "SALA - COMEDOR\n(Centro Luz LED 30W\n+ Tomacorrientes)", fontsize=7, ha='center', va='center', color='#1A202C')

ax1.add_patch(patches.Rectangle((5.0, 10.0), 4.0, 4.5, edgecolor='#4A5568', facecolor='#E2E8F0', lw=1))
ax1.text(7.0, 12.25, "ESTAR FAMILIAR\n(Centro Luz LED 20W\n+ Tomacorrientes)", fontsize=7, ha='center', va='center', color='#1A202C')

ax1.add_patch(patches.Rectangle((1.0, 5.0), 4.5, 5.0, edgecolor='#4A5568', facecolor='#FEFCBF', lw=1))
ax1.text(3.25, 7.5, "COCINA\n(Cocina 3Ø C-3 6.0kW\n+ Tomacorrientes C-6)", fontsize=7, ha='center', va='center', fontweight='bold', color='#744210')

ax1.add_patch(patches.Rectangle((5.5, 5.0), 3.5, 5.0, edgecolor='#4A5568', facecolor='#EDF2F7', lw=1))
ax1.text(7.25, 7.5, "DORMITORIO 1\n(Centro Luz LED 20W\n+ Tomacorrientes)", fontsize=7, ha='center', va='center', color='#1A202C')

ax1.add_patch(patches.Rectangle((1.0, 1.0), 3.0, 4.0, edgecolor='#4A5568', facecolor='#EBF8FF', lw=1))
ax1.text(2.5, 3.0, "CISTERNA Y\nELECTROBOMBA\n(C-5 0.75 HP)", fontsize=6.5, ha='center', va='center', color='#2B6CB0')

ax1.add_patch(patches.Rectangle((4.0, 1.0), 4.5, 4.0, edgecolor='#4A5568', facecolor='#E2E8F0', lw=1))
ax1.text(6.25, 3.0, "PATIO POSTERIOR\n(Al aire libre)", fontsize=7, ha='center', va='center', color='#1A202C')

# Tablero General Location
ax1.add_patch(patches.Rectangle((4.8, 9.2), 0.8, 0.4, edgecolor='red', facecolor='red'))
ax1.text(5.2, 9.7, "TABLERO GENERAL (TD)\n(Empotrado a 1.80m N.P.T.)", fontsize=6.5, fontweight='bold', color='red', ha='center')

# LEVEL 2: SEGUNDO PISO
ax2.set_title("SEGUNDO PISO (LÁMINA A2)\nÁrea Íntima y Dormitorios", fontsize=10, fontweight='bold', color='#0F2043')
ax2.add_patch(patches.Rectangle((0.5, 0.5), 9.0, 14.5, edgecolor='#0F2043', facecolor='#F7FAFC', lw=2))

ax2.add_patch(patches.Rectangle((1.0, 9.5), 4.0, 5.0, edgecolor='#4A5568', facecolor='#EDF2F7', lw=1))
ax2.text(3.0, 12.0, "DORMITORIO\nPRINCIPAL\n(Luz LED + S.H. Privado)", fontsize=7, ha='center', va='center', color='#1A202C')

ax2.add_patch(patches.Rectangle((5.0, 9.5), 4.0, 5.0, edgecolor='#4A5568', facecolor='#EDF2F7', lw=1))
ax2.text(7.0, 12.0, "DORMITORIO 2\n(Luz LED\n+ Tomacorrientes)", fontsize=7, ha='center', va='center', color='#1A202C')

ax2.add_patch(patches.Rectangle((1.0, 4.5), 4.0, 5.0, edgecolor='#4A5568', facecolor='#EDF2F7', lw=1))
ax2.text(3.0, 7.0, "DORMITORIO 3\n(Luz LED\n+ Tomacorrientes)", fontsize=7, ha='center', va='center', color='#1A202C')

ax2.add_patch(patches.Rectangle((5.0, 4.5), 4.0, 5.0, edgecolor='#4A5568', facecolor='#EDF2F7', lw=1))
ax2.text(7.0, 7.0, "DORMITORIO 4\n(Luz LED\n+ Tomacorrientes)", fontsize=7, ha='center', va='center', color='#1A202C')

ax2.add_patch(patches.Rectangle((1.0, 1.0), 3.5, 3.5, edgecolor='#4A5568', facecolor='#EBF8FF', lw=1))
ax2.text(2.75, 2.75, "SERVICIO HIGIÉNICO\nCOMÚN Y TERMA\n(C-4 1.5 kW)", fontsize=6.5, ha='center', va='center', color='#2B6CB0')

ax2.add_patch(patches.Rectangle((4.5, 1.0), 4.5, 3.5, edgecolor='#4A5568', facecolor='#E2E8F0', lw=1))
ax2.text(6.75, 2.75, "HALL Y DUC. VENTILACIÓN", fontsize=7, ha='center', va='center', color='#1A202C')

# LEVEL 3: AZOTEA
ax3.set_title("AZOTEA (LÁMINA A2)\nLavandería, Tendedero y Depósito", fontsize=10, fontweight='bold', color='#0F2043')
ax3.add_patch(patches.Rectangle((0.5, 0.5), 9.0, 14.5, edgecolor='#0F2043', facecolor='#F7FAFC', lw=2))

ax3.add_patch(patches.Rectangle((1.0, 8.0), 4.5, 6.5, edgecolor='#4A5568', facecolor='#FEFCBF', lw=1))
ax3.text(3.25, 11.25, "LAVANDERÍA\n(C-7 Lavadora/Secadora\n2.5 kW)", fontsize=7, ha='center', va='center', fontweight='bold', color='#744210')

ax3.add_patch(patches.Rectangle((5.5, 8.0), 3.5, 6.5, edgecolor='#4A5568', facecolor='#EDF2F7', lw=1))
ax3.text(7.25, 11.25, "DEPÓSITO\n(Centro Luz LED\n+ Tomacorriente)", fontsize=7, ha='center', va='center', color='#1A202C')

ax3.add_patch(patches.Rectangle((1.0, 1.0), 8.0, 7.0, edgecolor='#4A5568', facecolor='#E2E8F0', lw=1))
ax3.text(5.0, 4.5, "TENDEDERO Y ZONA AL AIRE LIBRE\n(Luminarias al aire libre resistente a intemperie IP65)", fontsize=7.5, ha='center', va='center', color='#1A202C')

plt.tight_layout()
fig_plano_path = os.path.join(TARGET_DIR, "fig_plano_diego_arquitectura.png")
plt.savefig(fig_plano_path, dpi=300)
plt.savefig(os.path.join(REPO_TARGET, "fig_plano_diego_arquitectura.png"), dpi=300)
plt.close()
print("Updated fig_plano_diego_arquitectura.png generated.")

