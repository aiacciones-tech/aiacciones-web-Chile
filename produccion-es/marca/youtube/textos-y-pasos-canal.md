# Canal @AIAccionesEspaña: textos y pasos de carga

Todo se carga en **YouTube Studio › Personalización** (perfil y marca) y **Configuración › Canal**.

## 1. Imágenes (Personalización › Marca)

| Qué | Archivo | Tamaño |
|---|---|---|
| Foto de perfil | `foto-perfil-800.png` | 800×800 (YouTube la recorta en círculo) |
| Banner | `banner-2560x1440.png` | 2560×1440; el texto está dentro de la zona segura de 1546×423 que se ve en móvil |
| Marca de agua del vídeo | `marca-agua-150.png` | 150×150; mostrar "Al final del vídeo" o "Todo el vídeo" |

`banner-control-zona-segura.png` es solo para revisar: marca en rojo lo que se ve en el móvil. No se sube.

## 2. Nombre y descripción (Personalización › Información básica)

**Nombre:** AIAcciones España
**Identificador:** @AIAccionesEspaña

**Descripción** (≈900 caracteres, límite 1.000):

> Resultados de las empresas del IBEX 35, empresa por empresa y explicados en unos cinco minutos.
>
> Cuando una cotizada española publica sus cuentas, normalmente antes de la apertura de la bolsa, preparamos un vídeo con la misma estructura de siempre:
> 1. El titular: qué cambió y cómo quedó frente al consenso
> 2. Ingresos
> 3. Beneficio y beneficio por acción
> 4. Márgenes, inversión y deuda
> 5. Guía de la compañía
> 6. Valoración frente a su propia historia (PER, EV/EBITDA, rentabilidad por dividendo)
> 7. Tres puntos positivos y tres riesgos
>
> Las cifras salen de la información que cada empresa publica en la CNMV y en su web, y de fuentes de mercado que citamos en cada vídeo. Los cálculos propios van siempre marcados.
>
> Contenido informativo. No es una recomendación de inversión ni asesoramiento personalizado. Aviso completo en el enlace "Aviso".

## 3. Enlaces (Personalización › Información básica › Enlaces)

- **Calendario de resultados 3T 2026**: [pendiente: enlace cuando esté en la web]
- **Aviso**: [pendiente: página con el aviso de la sección 6]
- **AIAcciones Chile**: https://www.youtube.com/@aiaccioneschile
- **X**: [cuenta de X si se abre una para España]

## 4. Palabras clave (Configuración › Canal › Palabras clave)

IBEX 35, bolsa española, resultados empresariales, resultados trimestrales, acciones españolas, Iberdrola, Santander, BBVA, CaixaBank, Inditex, Repsol, Telefónica, análisis fundamental, beneficio por acción, PER, dividendos, CNMV

**País del canal:** España. **Idioma de los vídeos:** español (España).

## 5. Tráiler y sección de inicio (Personalización › Diseño)

1. Sube `trailer/trailer-aiacciones-espana.mp4` como vídeo público con este título y descripción:
   - **Título:** AIAcciones España: resultados del IBEX 35, empresa por empresa
   - **Descripción:** la de la sección 2, más el calendario: Iberdrola 21-oct, Bankinter 22-oct, Santander 28-oct, BBVA y Repsol 29-oct, CaixaBank 30-oct.
2. En **Diseño › Tráiler del canal para quienes no están suscritos**, elige ese vídeo.
3. Crea dos listas de reproducción: **Resultados 3T 2026** y **Bancos del IBEX 35**. Añádelas como secciones en Diseño.

## 6. Aviso

El texto completo y la plantilla están en `../aviso-legal.txt` (Daniel pidió usar todos los disclaimers necesarios, 12-oct-2026). Va al final de cada descripción y como página "Aviso" cuando exista en la web.

## 7. Para que la rutina pueda subir vídeos

1. **Verifica el canal** con tu teléfono en youtube.com/verify. Sin eso no se pueden subir miniaturas propias.
2. **Token de subida** (OAuth Playground, mismo Client ID y Secret que Chile, scope `https://www.googleapis.com/auth/youtube.upload`, eligiendo el canal AIAcciones España al autorizar). Guárdalo en GitHub › Settings › Secrets › Actions como `YT_ES_REFRESH_TOKEN`. No lo pegues en el chat.
