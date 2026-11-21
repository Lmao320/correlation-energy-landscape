# Correlation Energy Landscape

Visualización animada de la relación entre el **S&P 500** y el **NASDAQ-100**: correlación móvil y análisis de liderazgo (*lead-lag*).

## Qué hace

- Retornos logarítmicos diarios desde 2018.
- **Correlación móvil** de 60 días.
- **Lead-lag:** prueba desfases de −5 a +5 días para identificar qué índice se adelanta.
- Superficie 3D animada: la amplitud depende de la correlación y la inclinación del liderazgo.

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python Correlation.py
```

## Limitaciones

- La superficie es una visualización ilustrativa controlada por los datos, no un modelo predictivo.
- Correlación lineal (Pearson) con ventana fija.

## Autor

**Santiago Peña Díaz** — Estudiante de Ingeniería de Sistemas (CUN, Colombia)

- GitHub: [Lmao320](https://github.com/Lmao320)
- Documentación completa: [Portafolio en Notion](https://freezing-hope-5b5.notion.site/Portafolio-de-Proyectos-Santiago-Pe-a-D-az-41f7f18e4ca2811793dcece91c3d00c0)
