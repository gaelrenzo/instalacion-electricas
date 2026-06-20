# Núcleo del Sistema (src/electra_core/)

Contiene la librería de Python interna (`electra_core`) que implementa la lógica algorítmica, tipos de datos estáticos y validadores del proyecto.

## Componentes

*   **Modelos de Datos:** Clases e interfaces que representan ambientes, muros, conductores, tableros, interruptores y cargas.
*   **Validadores:** Algoritmos para verificar el correcto cierre de polígonos de ambientes, escala y distancias mínimas de seguridad.
*   **Fórmulas Base:** Métodos matemáticos estandarizados para caída de tensión, factor de potencia y factores de demanda.

## Desarrollo y Pruebas
Cualquier cambio en la lógica de cálculo general debe implementarse aquí y pasar el conjunto completo de pruebas unitarias (`tests/`) antes de su despliegue en producción.
