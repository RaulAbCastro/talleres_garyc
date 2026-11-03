# Staging temporal para Overleaf

Fuentes LaTeX (en español) generadas a partir de `syllabus/Syllabus_v3.docx`
y `Recursos_taller.docx`. Están aquí temporalmente porque el entorno de
trabajo no pudo conectarse a `git.overleaf.com`; se moverán al submódulo
`documents_overleaf/` en cuanto haya acceso.

- `syllabus.tex`: syllabus de los tres talleres.
- `recursos.tex`: recursos y requerimientos.
- `garyc.sty`: estilo común (tipografía, colores, encabezados, listas).

Compilar con pdfLaTeX (`latexmk -pdf syllabus.tex`). En Overleaf, elegir el
documento principal en Menú > Documento principal.
