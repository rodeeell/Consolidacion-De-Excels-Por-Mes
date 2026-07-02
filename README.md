- Consolidación Automática de P&L 

Este proyecto automatiza la extracción, limpieza y transformación de los reportes financieros mensuales P&L. Convierte archivos Excel con formato de matriz (ancho) a un formato de base de datos relacional (largo), ideal para integraciones con herramientas de Business Intelligence o bases de datos centralizadas.

- Características Principales
- **Detección Dinámica de Compañías:** Identifica automáticamente las empresas presentes en el reporte mensual, adaptándose sin errores a la adición o eliminación de partners.
- **Limpieza Financiera:** Estandarización de nombres corporativos (eliminación de caracteres inválidos) y manejo automático de formatos numéricos (conversión de comas a puntos y redondeo contable a 2 decimales).
- **Escudo contra Duplicados:** Mantiene un registro de memoria (`procesados.json`) para procesar únicamente archivos nuevos. En caso de actualizaciones sobre el mismo periodo, conserva siempre el registro más reciente.
- **Lectura Inteligente:** Ignora encabezados decorativos y columnas "fantasmas" (`Unnamed`), limpiando celdas vacías para asegurar la integridad de la data final.

- Estructura del Directorio
Para asegurar el correcto funcionamiento, el directorio debe estar organizado de la siguiente manera:

Estructuración!
/
├── archivosbase/           # Carpeta donde se deben depositar los Excels mensuales crudos.
├── desafio_sura.py         # Script principal de ejecución.
├── procesados.json         # (Autogenerado) Bitácora de archivos ya consolidados.
└── ejemplo_tabla.xlsx      # (Autogenerado) Tabla maestra consolidada. (recomendable cambiarle el nombre)

Dependencias: 
-Librería Pandas (pip install pandas pentyl)
