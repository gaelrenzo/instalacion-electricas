# Pruebas Unitarias y de Integración (tests/)

Este directorio contiene las pruebas automáticas del sistema para asegurar que los motores de cálculo, generación CAD y análisis de cotizaciones funcionen sin errores.

## Ejecución de Pruebas

Para correr todas las pruebas del repositorio, asegúrate de tener el entorno virtual activo y ejecuta:

```bash
make test
```

O directamente mediante pytest:
```bash
pytest tests/
```

## Estructura
Las pruebas deben seguir la misma estructura que el paquete principal y validar casos límite (por ejemplo: caídas de tensión extremas, cargas no válidas o geometría mal cerrada).
