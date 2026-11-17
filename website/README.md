# Menú de los talleres

El menú está en [index.html](index.html), con estilos en [styles.css](styles.css).
Sus tres talleres siguen [el temario](../documents_overleaf/temario.tex).
La sesión 1 del Taller 1 ya tiene enlace. Las demás sesiones muestran sus títulos
en listas desplegables hasta que tengan diapositivas.

## Vista previa

Desde la raíz del repositorio:

```bash
bash slides/publicar.sh
python3 -m http.server 8000 --bind 0.0.0.0 --directory slides/_site
```

En Codespaces, abre el puerto 8000 en **Ports**. La tarea **HTML: vista previa**
de VS Code también compila las presentaciones y sirve el menú.

## Añadir una presentación

Cuando una sesión esté lista, incluye sus archivos en el
[empaquetado de Pages](../slides/publicar.sh) y convierte su título en un enlace
relativo a `./taller-N/sesion-M/` dentro de `index.html`.
Comprueba en la vista previa que el enlace abra las diapositivas.
GitHub Actions publica el menú como [entrada de GitHub Pages](https://raulabcastro.github.io/talleres_garyc/)
al subir cambios a `main`.
