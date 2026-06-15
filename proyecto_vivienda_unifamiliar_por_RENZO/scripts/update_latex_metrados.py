import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
capitulos_dir = os.path.join(base_dir, "capitulos")
metrado_path = os.path.join(capitulos_dir, "06-metrado.tex")
presupuesto_path = os.path.join(capitulos_dir, "09-presupuesto.tex")

# 1. Generate 06-metrado.tex content
metrado_content = r"""\chapter{METRADO}

\section{Alcance}

El presente metrado cuantifica los materiales necesarios para la instalacion electrica interior de la vivienda unifamiliar de tres niveles, conforme a la sectorizacion de siete circuitos (C1 a C7) definida para el proyecto de Renzo Gabriel Mamani Galindo. Las cantidades se obtienen de los planos electricos y de los recorridos estimados de canalizacion por nivel.

Los metrados se agrupan por las siguientes categorias: tuberias, conductores, cajas, tableros, accesorios, protecciones, luminarias y sistema de puesta a tierra.

\section{Resumen de puntos electricos por circuito}

\begin{table}[H]
\centering
\small
\caption{Puntos electricos por circuito (Proyecto de Renzo)}
\label{tab:puntos-por-circuito}
\begin{tabularx}{\textwidth}{c L{4.5cm} c c c Y}
\toprule
\textbf{Cto.} & \textbf{Uso} & \textbf{Luminarias} & \textbf{TCs} & \textbf{Interruptores} & \textbf{Long. est. (m)} \\
\midrule
C1 & Alumbrado 1er piso & 4 & -- & 2 & 12 \\
C2 & TCs generales 1er piso & -- & 5 & -- & 15 \\
C3 & Tomacorrientes Cocina & -- & 3 & -- & 10 \\
C4 & Alumbrado 2do piso & 4 & -- & 3 & 14 \\
C5 & TCs generales 2do piso & -- & 8 & -- & 20 \\
C6 & Alumbrado 3er piso & 4 & -- & 3 & 16 \\
C7 & TCs generales 3er piso & -- & 6 & -- & 18 \\
\midrule
\textbf{Total} & & \textbf{12} & \textbf{22} & \textbf{8} & \textbf{105} \\
\bottomrule
\end{tabularx}
\end{table}

\section{Metrado de tuberias (canalizaciones)}

\begin{landscape}
\begin{table}[H]
\centering
\small
\caption{Metrado de tuberias PVC}
\label{tab:metrado-tuberias}
\begin{tabularx}{\textwidth}{c L{4.5cm} L{1.5cm} c L{1.8cm} L{3.5cm} Y}
\toprule
\textbf{Item} & \textbf{Descripcion} & \textbf{Tipo} & \textbf{Und.} & \textbf{Cant.} & \textbf{Circuitos} & \textbf{Observacion} \\
\midrule
1 & Tuberia PVC liviana 3/4" para alumbrado & PV-L & m & 120 & C1, C4, C6 & Empotrada en losa de techo \\
2 & Tuberia PVC pesada 3/4" para tomacorrientes & PV-P & m & 150 & C2, C3, C5, C7 & Empotrada en contrapiso y muros \\
3 & Tuberia PVC pesada 1" para alimentador & PV-P & m & 25 & Alimentador general & Desde medidor a TG y subtableros \\
\bottomrule
\end{tabularx}
\end{table}
\end{landscape}

\section{Metrado de conductores}

\begin{landscape}
\begin{table}[H]
\centering
\small
\caption{Metrado de conductores de cobre}
\label{tab:metrado-conductores}
\begin{tabularx}{\textwidth}{c L{4.5cm} c L{1.8cm} L{1.8cm} L{1.8cm} c Y}
\toprule
\textbf{Item} & \textbf{Descripcion} & \textbf{Und.} & \textbf{Seccion} & \textbf{Cant.} & \textbf{Tipo} & \textbf{Uso} & \textbf{Observacion} \\
\midrule
1 & Conductor fase alumbrado & m & 1.5 mm2 & 120 & LSOH & C1, C4, C6 & Cableado unipolar \\
2 & Conductor neutro alumbrado & m & 1.5 mm2 & 120 & LSOH & C1, C4, C6 & Cableado unipolar \\
3 & Conductor de proteccion alumbrado & m & 1.5 mm2 & 110 & LSOH & C1, C4, C6 & Segun CNE-U \\
4 & Conductor fase tomacorrientes & m & 2.5 mm2 & 160 & LSOH & C2, C3, C5, C7 & Cableado unipolar \\
5 & Conductor neutro tomacorrientes & m & 2.5 mm2 & 160 & LSOH & C2, C3, C5, C7 & Cableado unipolar \\
6 & Conductor de proteccion tomacorrientes & m & 2.5 mm2 & 160 & LSOH & C2, C3, C5, C7 & Cableado unipolar \\
7 & Conductor alimentador general fase & m & 10 mm2 & 30 & LSOH & TG & Cableado unipolar \\
8 & Conductor alimentador general neutro & m & 10 mm2 & 30 & LSOH & TG & Cableado unipolar \\
\bottomrule
\end{tabularx}
\end{table}
\end{landscape}

\clearpage

\section{Metrado de cajas}

\begin{table}[H]
\centering
\small
\caption{Metrado de cajas de pase y derivacion}
\label{tab:metrado-cajas}
\begin{tabularx}{\textwidth}{c L{4.5cm} L{2.5cm} c L{2.5cm} Y}
\toprule
\textbf{Item} & \textbf{Descripcion} & \textbf{Material} & \textbf{Und.} & \textbf{Cant.} & \textbf{Observacion} \\
\midrule
1 & Cajas octogonales 4" x 2" para luminarias & Fierro galvanizado & pza & 12 & Puntos de luz y derivacion \\
2 & Cajas rectangulares 4" x 2" para interruptores & Fierro galvanizado & pza & 8 & Interruptores simples y conmutadores \\
3 & Cajas rectangulares 4" x 2" para tomacorrientes & Fierro galvanizado & pza & 24 & Tomacorrientes generales y especiales \\
4 & Caja de pase rectangular 4" x 2" & Fierro galvanizado & pza & 6 & Para derivaciones en cambios de direccion \\
\bottomrule
\end{tabularx}
\end{table}

\section{Metrado de tableros}

\begin{table}[H]
\centering
\small
\caption{Metrado de tableros electricos}
\label{tab:metrado-tableros}
\begin{tabularx}{\textwidth}{c L{4.5cm} L{1.8cm} c L{1.8cm} Y}
\toprule
\textbf{Item} & \textbf{Descripcion} & \textbf{Polos} & \textbf{Und.} & \textbf{Cant.} & \textbf{Observacion} \\
\midrule
1 & Tablero general TG-01 (metalico empotrable) & 12 polos & u & 1 & Primer piso, zona de ingreso \\
2 & Tablero de distribucion TD-01 & 8 polos & u & 1 & Segundo piso, zona central \\
3 & Tablero de distribucion TD-02 & 8 polos & u & 1 & Tercer piso o zona de servicio \\
\bottomrule
\end{tabularx}
\end{table}

\section{Metrado de accesorios y protecciones}

\begin{landscape}
\begin{table}[H]
\centering
\small
\caption{Metrado de accesorios, interruptores y protecciones}
\label{tab:metrado-accesorios}
\begin{tabularx}{\textwidth}{c L{4.5cm} c L{2.0cm} L{2.0cm} Y}
\toprule
\textbf{Item} & \textbf{Descripcion} & \textbf{Und.} & \textbf{Cant.} & \textbf{Circuito} & \textbf{Observacion} \\
\midrule
1 & Interruptor simple (unipolar) & pza & 4 & C1, C4, C6 & Ambientes generales \\
2 & Interruptor conmutacion 3 vias (S3) & pza & 4 & C1, C4, C6 & Escaleras y pasadizo \\
3 & Tomacorriente doble con toma a tierra & pza & 22 & C2, C3, C5, C7 & Uso general \\
4 & Tomacorriente doble con proteccion GFCI & pza & 2 & C5, C7 & Banos (protegido) \\
5 & Interruptor termomagnetico 2P-10A & pza & 3 & C1, C4, C6 & Proteccion alumbrado \\
6 & Interruptor termomagnetico 2P-16A & pza & 3 & C2, C5, C7 & Proteccion tomacorrientes \\
7 & Interruptor termomagnetico 2P-20A & pza & 1 & C3 & Proteccion cocina \\
8 & Interruptor termomagnetico general 2P-40A & pza & 1 & Alimentador & Proteccion general TG \\
9 & Interruptor diferencial 2P-25A-30mA & pza & 4 & C2, C3, C5, C7 & Proteccion de personas \\
10 & Interruptor diferencial 2P-40A-30mA (General) & pza & 1 & TG-01 & Proteccion diferencial general \\
11 & Luminaria LED interior 12 W (circular o rectangular) & pza & 12 & C1, C4, C6 & Iluminacion LED \\
\bottomrule
\end{tabularx}
\end{table}
\end{landscape}

\section{Metrado de puesta a tierra}

\begin{table}[H]
\centering
\small
\caption{Metrado del sistema de puesta a tierra}
\label{tab:metrado-puesta-tierra}
\begin{tabularx}{\textwidth}{c L{4.5cm} L{2.0cm} c L{2.5cm} Y}
\toprule
\textbf{Item} & \textbf{Descripcion} & \textbf{Material} & \textbf{Und.} & \textbf{Cant.} & \textbf{Observacion} \\
\midrule
1 & Varilla de puesta a tierra 5/8" x 2.40 m & Cobre solido & pza & 1 & Electrodo principal \\
2 & Conector de bronce para varilla & Bronce & pza & 1 & Conexion certificada \\
3 & Conductor de puesta a tierra 6 mm2 & Cobre desnudo & m & 25 & Conexion a barra de tierra \\
4 & Caja de registro de puesta a tierra & Metalico & pza & 1 & Para inspeccion \\
5 & Barra de tierra para tablero & Cobre & pza & 1 & En tablero general \\
6 & Gel o mejorador de suelo & Quimico & kg & 5 & Reduccion de resistencia \\
\bottomrule
\end{tabularx}
\end{table}

\section{Resumen general de metrados}

\begin{landscape}
\begin{table}[H]
\centering
\tiny
\caption{Resumen general de metrados (Proyecto Renzo)}
\label{tab:resumen-metrados}
\begin{tabularx}{\textwidth}{c L{4.8cm} L{2.2cm} c L{1.8cm} L{3.0cm} Y}
\toprule
\textbf{Item} & \textbf{Descripcion} & \textbf{Und.} & \textbf{Especificacion} & \textbf{Cant.} & \textbf{Plano ref.} & \textbf{Observacion} \\
\midrule
1 & Tuberia PVC liviana 3/4" & m & PV-L & 120 & IE-02, IE-04 & Alumbrado empotrado en techo \\
2 & Tuberia PVC pesada 3/4" & m & PV-P & 150 & IE-03, IE-04 & Tomacorrientes empotrado en muro \\
3 & Tuberia PVC pesada 1" & m & PV-P & 25 & IE-01 & Alimentador general \\
4 & Conductor 1.5 mm2 Cu LSOH & m & LSOH 1.5 mm2 & 350 & IE-02 & Fase+neutro+PE alumbrado \\
5 & Conductor 2.5 mm2 Cu LSOH & m & LSOH 2.5 mm2 & 480 & IE-03 & Fase+neutro+PE tomacorrientes \\
6 & Conductor 10 mm2 Cu LSOH & m & LSOH 10 mm2 & 30 & IE-01 & Alimentador general \\
7 & Conductor 6 mm2 Cu & m & Cu desnudo & 25 & IE-06 & Puesta a tierra \\
8 & Caja octogonal 4" x 2" FG & pza & FG & 12 & IE-02 & Luminarias \\
9 & Caja rectangular 4" x 2" FG & pza & FG & 32 & IE-02, IE-03 & Interruptores y tomacorrientes \\
10 & Caja de pase rectangular & pza & FG & 6 & IE-04 & Derivaciones \\
11 & Tablero general TG-01 & u & 12 polos & 1 & IE-05 & Primer piso \\
12 & Tablero distribucion TD-01 & u & 8 polos & 1 & IE-05 & Segundo piso \\
13 & Tablero distribucion TD-02 & u & 8 polos & 1 & IE-05 & Tercer piso \\
14 & Interruptor simple & pza & Unipolar & 4 & IE-02 & Alumbrado \\
15 & Interruptor conmutador S3 & pza & 3 vias & 4 & IE-02 & Escaleras \\
16 & Tomacorriente doble c/tierra & pza & 15 A - 250 V & 22 & IE-03 & Uso general \\
17 & Tomacorriente GFCI & pza & 15 A - 30 mA & 2 & IE-03 & Banos \\
18 & Interruptor termomagnetico 2P-10A & pza & 10 A & 3 & IE-05 & Alumbrado \\
19 & Interruptor termomagnetico 2P-16A & pza & 16 A & 3 & IE-05 & Tomacorrientes \\
20 & Interruptor termomagnetico 2P-20A & pza & 20 A & 1 & IE-05 & Cocina \\
21 & Interruptor termomagnetico general 2P-40A & pza & 40 A & 1 & IE-05 & General TG \\
22 & Interruptor diferencial 2P-25A-30mA & pza & 25 A - 30 mA & 4 & IE-05 & Circuitos tomacorrientes \\
23 & Interruptor diferencial 2P-40A-30mA & pza & 40 A - 30 mA & 1 & IE-05 & General TG \\
24 & Luminaria LED 12 W & pza & 12 W LED & 12 & IE-02 & Iluminacion interior \\
25 & Kit de puesta a tierra completo & jgo & 5/8" x 2.40 m & 1 & IE-06 & Incluye varilla, conector, caja \\
\bottomrule
\end{tabularx}
\end{table}
\end{landscape}

\section{Nota tecnica}

Los metrados presentados son referenciales y corresponden a un anteproyecto academico. Las cantidades definitivas deberan recalcularse en un proyecto ejecutivo considerando:

\begin{itemize}
  \item Planos arquitectonicos con cotas definitivas.
  \item Longitudes reales de recorridos de tuberias en obra.
  \item Criterios de la empresa distribuidora (Electro Puno S.A.A.).
  \item Verificacion de curvas, accesorios y desperdicios de obra (se recomienda agregar 5\% a 10\% de desperdicio en la compra real).
\end{itemize}
"""

with open(metrado_path, "w", encoding="utf-8") as f:
    f.write(metrado_content)
print(f"Updated: {metrado_path}")


# 2. Generate 09-presupuesto.tex content
presupuesto_content = r"""\chapter{PRESUPUESTO ESTIMADO}

\section{Alcance}

El presente presupuesto estima el costo referencial de los materiales, mano de obra e impuestos para la instalacion electrica interior de la vivienda unifamiliar de tres niveles para el proyecto de Renzo Gabriel Mamani Galindo. Los precios unitarios corresponden a valores referenciales del mercado local a la fecha del proyecto.

El presupuesto se estructura en las siguientes partidas:
\begin{itemize}
  \item Tuberias y canalizaciones.
  \item Conductores electricos.
  \item Cajas de pase y derivacion.
  \item Tableros electricos.
  \item Accesorios, interruptores y tomacorrientes.
  \item Protecciones electricas.
  \item Luminarias.
  \item Sistema de puesta a tierra.
  \item Mano de obra.
  \item Impuestos (IGV 18\%).
\end{itemize}

\section{Precios unitarios referenciales}

La siguiente tabla muestra los precios unitarios estimados para cada material, basados en cotizaciones de proveedores locales y ferreterias especializadas de la region.

\begin{table}[H]
\centering
\footnotesize
\caption{Precios unitarios referenciales de materiales (Proyecto Renzo)}
\label{tab:precios-unitarios}
\begin{tabularx}{\textwidth}{c Y c c R{1.8cm} L{2.0cm} L{2.5cm}}
\toprule
\textbf{Item} & \textbf{Descripcion} & \textbf{Und.} & \textbf{Cant.} & \textbf{P. Unit. (S/)} & \textbf{Proveedor ref.} & \textbf{Observacion} \\
\midrule
1 & Tuberia PVC liviana 3/4" & m & 120 & 3.50 & Ferreteria local & Tuberia SELVA o similar \\
2 & Tuberia PVC pesada 3/4" & m & 150 & 4.50 & Ferreteria local & Tuberia SELVA o similar \\
3 & Tuberia PVC pesada 1" & m & 25 & 8.50 & Ferreteria local & Tuberia SELVA o similar \\
4 & Conductor LSOH 1.5 mm2 (rollo 100 m) & m & 350 & 2.80 & Indeco / Promel & Cable unipolar cobre \\
5 & Conductor LSOH 2.5 mm2 (rollo 100 m) & m & 480 & 4.50 & Indeco / Promel & Cable unipolar cobre \\
6 & Conductor LSOH 10 mm2 (rollo 100 m) & m & 30 & 16.00 & Indeco / Promel & Cable unipolar cobre \\
7 & Conductor 6 mm2 Cu desnudo (rollo 50 m) & m & 25 & 8.00 & Indeco / Promel & Puesta a tierra \\
8 & Caja octogonal FG 4" x 2" & pza & 12 & 3.50 & Ferreteria local & -- \\
9 & Caja rectangular FG 4" x 2" & pza & 32 & 3.20 & Ferreteria local & -- \\
10 & Caja de pase rectangular FG & pza & 6 & 4.50 & Ferreteria local & -- \\
11 & Tablero general TG-01 12 polos equipado & u & 1 & 450.00 & SEIN / TICINO & Completo con barra N/T y puerta \\
12 & Tablero distribucion TD-01 8 polos equipado & u & 1 & 320.00 & SEIN / TICINO & Completo con barra N/T y puerta \\
13 & Tablero distribucion TD-02 8 polos equipado & u & 1 & 320.00 & SEIN / TICINO & Completo con barra N/T y puerta \\
14 & Interruptor simple unipolar (placa completa) & pza & 4 & 12.00 & TICINO / BTICINO & Color blanco \\
15 & Interruptor conmutador S3 (placa completa) & pza & 4 & 15.00 & TICINO / BTICINO & Color blanco \\
16 & Tomacorriente doble c/tierra (placa completa) & pza & 22 & 14.50 & TICINO / BTICINO & 15 A - 250 V \\
17 & Tomacorriente GFCI (placa completa) & pza & 2 & 45.00 & TICINO / BTICINO & Proteccion diferencial integrada \\
18 & Interruptor termomagnetico 2P-10A & pza & 3 & 35.00 & SEIN / LEGRAND & Curva C \\
19 & Interruptor termomagnetico 2P-16A & pza & 3 & 38.00 & SEIN / LEGRAND & Curva C \\
20 & Interruptor termomagnetico 2P-20A & pza & 1 & 42.00 & SEIN / LEGRAND & Curva C \\
21 & Interruptor termomagnetico general 2P-40A & pza & 1 & 85.00 & SEIN / LEGRAND & Curva C \\
22 & Interruptor diferencial 2P-25A-30mA & pza & 4 & 120.00 & SEIN / LEGRAND & Proteccion de personas \\
23 & Interruptor diferencial 2P-40A-30mA & pza & 1 & 140.00 & SEIN / LEGRAND & Proteccion general \\
24 & Luminaria LED interior 12 W & pza & 12 & 25.00 & Philips / OSRAM & Panel LED circular o rectangular \\
25 & Kit de puesta a tierra completo & jgo & 1 & 650.00 & Ferreteria especializada & Varilla 5/8" x 2.40 m + accesorios \\
26 & Varios (curvas, uniones, cinta aislante, conectores) & glb & 1 & 200.00 & Ferreteria local & Accesorios de instalacion \\
\bottomrule
\end{tabularx}
\end{table}

\clearpage

\section{Presupuesto general}

\begin{table}[H]
\centering
\footnotesize
\setlength{\tabcolsep}{4pt}
\caption{Presupuesto general estimado (Proyecto Renzo)}
\label{tab:presupuesto-general}
\begin{tabularx}{\textwidth}{c Y c c R{1.8cm} R{1.8cm} R{1.8cm}}
\toprule
\textbf{Item} & \textbf{Descripcion de partida / material} & \textbf{Und.} & \textbf{Cant.} & \textbf{P. Unit. (S/)} & \textbf{Parcial (S/)} & \textbf{Subtotal (S/)} \\
\midrule
\multicolumn{7}{l}{\textbf{01.00 TUBERIAS Y CANALIZACIONES}} \\
01.01 & Tuberia PVC liviana 3/4" para alumbrado & m & 120 & 3.50 & 420.00 & \\
01.02 & Tuberia PVC pesada 3/4" para tomacorrientes & m & 150 & 4.50 & 675.00 & \\
01.03 & Tuberia PVC pesada 1" para alimentador & m & 25 & 8.50 & 212.50 & \\
 & & & & & \textbf{Subtotal 01} & \textbf{1,307.50} \\
\midrule
\multicolumn{7}{l}{\textbf{02.00 CONDUCTORES ELECTRICOS}} \\
02.01 & Conductor LSOH 1.5 mm2 (fase+neutro+PE) & m & 350 & 2.80 & 980.00 & \\
02.02 & Conductor LSOH 2.5 mm2 (fase+neutro+PE) & m & 480 & 4.50 & 2,160.00 & \\
02.03 & Conductor LSOH 10 mm2 (fase+neutro) & m & 30 & 16.00 & 480.00 & \\
02.04 & Conductor Cu desnudo 6 mm2 (PT) & m & 25 & 8.00 & 200.00 & \\
 & & & & & \textbf{Subtotal 02} & \textbf{3,820.00} \\
\midrule
\multicolumn{7}{l}{\textbf{03.00 CAJAS}} \\
03.01 & Caja octogonal FG 4" x 2" & pza & 12 & 3.50 & 42.00 & \\
03.02 & Caja rectangular FG 4" x 2" & pza & 32 & 3.20 & 102.40 & \\
03.03 & Caja de pase rectangular FG & pza & 6 & 4.50 & 27.00 & \\
 & & & & & \textbf{Subtotal 03} & \textbf{171.40} \\
\midrule
\multicolumn{7}{l}{\textbf{04.00 TABLEROS}} \\
04.01 & Tablero general TG-01 12 polos & u & 1 & 450.00 & 450.00 & \\
04.02 & Tablero distribucion TD-01 8 polos & u & 1 & 320.00 & 320.00 & \\
04.03 & Tablero distribucion TD-02 8 polos & u & 1 & 320.00 & 320.00 & \\
 & & & & & \textbf{Subtotal 04} & \textbf{1,090.00} \\
\midrule
\multicolumn{7}{l}{\textbf{05.00 ACCESORIOS Y PROTECCIONES}} \\
05.01 & Interruptor simple unipolar & pza & 4 & 12.00 & 48.00 & \\
05.02 & Interruptor conmutador S3 & pza & 4 & 15.00 & 60.00 & \\
05.03 & Tomacorriente doble con toma a tierra & pza & 22 & 14.50 & 319.00 & \\
05.04 & Tomacorriente GFCI (banos) & pza & 2 & 45.00 & 90.00 & \\
05.05 & Interruptor termomagnetico 2P-10A & pza & 3 & 35.00 & 105.00 & \\
05.06 & Interruptor termomagnetico 2P-16A & pza & 3 & 38.00 & 114.00 & \\
05.07 & Interruptor termomagnetico 2P-20A & pza & 1 & 42.00 & 42.00 & \\
05.08 & Interruptor termomagnetico general 2P-40A & pza & 1 & 85.00 & 85.00 & \\
05.09 & Interruptor diferencial 2P-25A-30mA & pza & 4 & 120.00 & 480.00 & \\
05.10 & Interruptor diferencial 2P-40A-30mA (General) & pza & 1 & 140.00 & 140.00 & \\
05.11 & Luminaria LED interior 12 W & pza & 12 & 25.00 & 300.00 & \\
 & & & & & \textbf{Subtotal 05} & \textbf{1,783.00} \\
\midrule
\multicolumn{7}{l}{\textbf{06.00 PUESTA A TIERRA Y VARIOS}} \\
06.01 & Kit de puesta a tierra completo & jgo & 1 & 650.00 & 650.00 & \\
06.02 & Varios (accesorios de instalacion) & glb & 1 & 200.00 & 200.00 & \\
 & & & & & \textbf{Subtotal 06} & \textbf{850.00} \\
\midrule
\multicolumn{5}{r}{\textbf{VALOR TOTAL DE MATERIALES}} & & \textbf{9,021.90} \\
\multicolumn{5}{r}{Mano de Obra (40\%)} & & \textbf{3,608.76} \\
\multicolumn{5}{r}{\textbf{SUBTOTAL GENERAL}} & & \textbf{12,630.66} \\
\multicolumn{5}{r}{Impuesto General a las Ventas (IGV 18\%)} & & \textbf{2,273.52} \\
\multicolumn{5}{r}{\textbf{PRESUPUESTO TOTAL GENERAL}} & & \textbf{14,904.18} \\
\bottomrule
\end{tabularx}
\end{table}

\section{Nota tecnica}

Los costos presentados estan basados en cotizaciones locales de la region de Puno. Para una ejecucion real de obra se sugiere considerar un incremento del 5\% al 10\% por concepto de desperdicios de materiales y variabilidad en el mercado de cobre.
"""

with open(presupuesto_path, "w", encoding="utf-8") as f:
    f.write(presupuesto_content)
print(f"Updated: {presupuesto_path}")
