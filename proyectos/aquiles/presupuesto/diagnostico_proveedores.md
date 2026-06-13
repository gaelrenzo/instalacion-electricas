# Diagnostico de proveedores

**Estado global:** Comparativa con cobertura util en al menos dos proveedores.

| Proveedor | Material probado | URL | Estado HTTP | Redirect | Metodo | Resultados crudos | Resultados aceptados | Estado | Motivo de fallo |
|---|---|---|---:|---|---|---:|---:|---|---|
| promart | Caja estanca IP55 para conexion de bomba - C8 | [abrir](https://www.promart.pe/search?q=caja+electrica+estanca+ip55) | 200 | no | httpx_html | 0 | 0 | html_sin_productos | - |
| promart | Caja estanca IP55 para conexion de bomba - C8 | [abrir](https://www.promart.pe/search?q=caja+estanca+electrica+ip55) | 200 | no | httpx_html | 0 | 0 | html_sin_productos | - |
| promart | Caja estanca IP55 para conexion de bomba - C8 | [abrir](https://www.promart.pe/api/catalog_system/pub/products/search?ft=caja%20de%20paso%20estanca%20ip55) | 206 | no | api_vtex | 5 | 0 | ok_precio | - |
| sodimac | Caja estanca IP55 para conexion de bomba - C8 | [abrir](https://www.sodimac.com.pe/sodimac-pe/search?Ntt=caja+electrica+estanca+ip55) | - | no | httpx_sodimac_legacy | 0 | 0 | parser_fallo | TypeError: Cannot mix str and non-str arguments |
| sodimac | Caja estanca IP55 para conexion de bomba - C8 | [abrir](https://www.falabella.com.pe/falabella-pe/search?Ntt=caja+electrica+estanca+ip55) | 200 | no | httpx_catalogo_falabella | 21 | 0 | ok_precio | - |
| sodimac | Caja estanca IP55 para conexion de bomba - C8 | [abrir](https://www.falabella.com.pe/falabella-pe/search?Ntt=caja+estanca+electrica+ip55) | 200 | no | httpx_catalogo_falabella | 22 | 0 | ok_precio | - |
| sodimac | Caja estanca IP55 para conexion de bomba - C8 | [abrir](https://www.falabella.com.pe/falabella-pe/search?Ntt=caja+de+paso+estanca+ip55) | 200 | no | httpx_catalogo_falabella | 24 | 0 | ok_precio | - |
| maestro | Caja estanca IP55 para conexion de bomba - C8 | [abrir](https://www.maestro.com.pe/maestro-pe/search?Ntt=caja+electrica+estanca+ip55) | - | no | httpx_sodimac_legacy | 0 | 0 | timeout | ConnectTimeout: timed out |
| maestro | Caja estanca IP55 para conexion de bomba - C8 | [abrir](https://www.falabella.com.pe/falabella-pe/search?Ntt=caja+electrica+estanca+ip55) | 200 | no | httpx_catalogo_falabella | 10 | 0 | ok_precio | - |
| maestro | Caja estanca IP55 para conexion de bomba - C8 | [abrir](https://www.falabella.com.pe/falabella-pe/search?Ntt=caja+estanca+electrica+ip55) | 200 | no | httpx_catalogo_falabella | 10 | 0 | ok_precio | - |
| maestro | Caja estanca IP55 para conexion de bomba - C8 | [abrir](https://www.falabella.com.pe/falabella-pe/search?Ntt=caja+de+paso+estanca+ip55) | 200 | no | httpx_catalogo_falabella | 10 | 0 | ok_precio | - |
| mercadolibre | Caja estanca IP55 para conexion de bomba - C8 | [abrir](https://api.mercadolibre.com/sites/MPE/search?q=caja+electrica+estanca+ip55&limit=5) | 403 | no | api_publica | 0 | 0 | bloqueado | - |
| mercadolibre | Caja estanca IP55 para conexion de bomba - C8 | [abrir](https://listado.mercadolibre.com.pe/caja-electrica-estanca-ip55) | 200 | si | httpx_html | 0 | 0 | bloqueado | - |
| promart | Caja de registro para puesta a tierra | [abrir](https://www.promart.pe/api/catalog_system/pub/products/search?ft=caja%20registro%20puesta%20a%20tierra) | 200 | no | api_vtex | 2 | 0 | ok_precio | - |
| promart | Caja de registro para puesta a tierra | [abrir](https://www.promart.pe/api/catalog_system/pub/products/search?ft=caja%20inspeccion%20pozo%20a%20tierra) | 200 | no | api_vtex | 1 | 0 | ok_precio | - |
| sodimac | Caja de registro para puesta a tierra | [abrir](https://www.falabella.com.pe/falabella-pe/search?Ntt=caja+registro+puesta+a+tierra) | 200 | no | httpx_catalogo_falabella | 40 | 0 | ok_precio | - |
| sodimac | Caja de registro para puesta a tierra | [abrir](https://www.falabella.com.pe/falabella-pe/search?Ntt=caja+inspeccion+pozo+a+tierra) | 200 | no | httpx_catalogo_falabella | 34 | 0 | ok_precio | - |
| maestro | Caja de registro para puesta a tierra | [abrir](https://www.falabella.com.pe/falabella-pe/search?Ntt=caja+registro+puesta+a+tierra) | 200 | no | httpx_catalogo_falabella | 10 | 0 | ok_precio | - |
| maestro | Caja de registro para puesta a tierra | [abrir](https://www.falabella.com.pe/falabella-pe/search?Ntt=caja+inspeccion+pozo+a+tierra) | 200 | no | httpx_catalogo_falabella | 10 | 0 | ok_precio | - |
| mercadolibre | Caja de registro para puesta a tierra | [abrir](https://api.mercadolibre.com/sites/MPE/search?q=caja+registro+puesta+a+tierra&limit=5) | 403 | no | api_publica | 0 | 0 | bloqueado | - |
| mercadolibre | Caja de registro para puesta a tierra | [abrir](https://listado.mercadolibre.com.pe/caja-registro-puesta-a-tierra) | 200 | si | httpx_html | 0 | 0 | bloqueado | - |

## Hallazgos tecnicos

- **Promart:** expone un endpoint publico VTEX con productos, precios, stock y enlaces directos.
- **Sodimac:** la URL historica redirige a la portada; el fallback usa el catalogo unificado Falabella y conserva solo ofertas cuyo vendedor es SODIMAC.
- **Maestro:** el dominio historico puede agotar conexion; el fallback consulta el catalogo unificado y conserva solo ofertas identificadas con vendedor MAESTRO.
- **Mercado Libre:** la API publica puede responder 403 y el HTML puede mostrar verificacion de trafico. No se intentan saltar controles; se conserva el enlace de busqueda verificable.
- Los resultados con precio pero categoria, especificacion o unidad no confiable se mantienen como evidencia y no compiten por la recomendacion.
