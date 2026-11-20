# 🎓 Guía Rápida - Presentaciones Talleres GARyC

## ✅ Estado Actual
El servidor web está **ACTIVO** y sirviendo todas las presentaciones correctamente.

---

## 🚀 Cómo Acceder

### **Opción 1: Desde este dispositivo (Local)**
Abre tu navegador e ingresa:
```
http://localhost:8000
```

### **Opción 2: Desde Codespaces (Si estás usando Github Codespaces)**
1. En VS Code, busca la pestaña **"Ports"** (abajo a la derecha)
2. Localiza el puerto **8000**
3. Haz clic en la URL pública que aparece
4. Se abrirá en tu navegador automáticamente

### **Opción 3: Desde otra máquina en la red**
Reemplaza `localhost` con:
- La dirección IP de esta máquina: `http://<IP>:8000`
- O el dominio/hostname: `http://<hostname>:8000`

---

## 📊 Presentaciones Disponibles

### 📊 **Sesión 1: De la muestra a la inferencia**
- **URL**: http://localhost:8000/taller-1/sesion-1/
- **Diapositivas**: 39
- **Contenido**: Fundamentos de estadística inferencial, distribuciones muestrales, intervalos de confianza, contrastes de hipótesis

### 🎯 **Sesión 2: Resultados potenciales y sesgo de selección**
- **URL**: http://localhost:8000/taller-1/sesion-2/
- **Diapositivas**: 21
- **Contenido**: Causalidad observacional, contrafactuales, ATE, ATT, aleatorización

---

## ⌨️ Controles de las Presentaciones

Las presentaciones usan **reveal.js**. Controles:

| Acción | Control |
|--------|---------|
| Siguiente diapositiva | ➡️ Flecha derecha o Espacio |
| Diapositiva anterior | ⬅️ Flecha izquierda |
| Bajar en la misma diapositiva | ⬇️ Flecha abajo |
| Subir en la misma diapositiva | ⬆️ Flecha arriba |
| Pantalla completa | `F` |
| Vista general | `ESC` |
| Notas del orador | `S` |

---

## 🛠️ Troubleshooting

### ❓ **No veo las presentaciones**
1. **Recarga la página**: Presiona `Ctrl+Shift+R` (o `Cmd+Shift+R` en Mac) para limpiar la caché
2. **Verifica la URL**: Asegúrate de usar `http://` (no `https://`)
3. **Abre la consola**: Presiona `F12` para ver errores en la consola

### ❓ **Las imágenes o gráficos no se ven**
1. Recarga la página con `Ctrl+Shift+R`
2. Verifica que tienes conexión de internet (algunos CDN necesitan internet)
3. Abre la consola (`F12`) y mira si hay errores 404

### ❓ **El servidor no funciona**
Ejecuta en la terminal:
```bash
# Verifica que el servidor está corriendo
ps aux | grep "http.server"

# Si no está corriendo, inicia uno nuevo
cd /workspaces/talleres_garyc/slides
python3 -m http.server 8000
```

### ❓ **Quiero cambiar el puerto**
```bash
# En lugar de 8000, usa otro puerto (ej: 3000)
cd /workspaces/talleres_garyc/slides
python3 -m http.server 3000
```

---

## 📁 Estructura de Archivos

```
/workspaces/talleres_garyc/slides/
├── index.html                    # Página principal (menú de sesiones)
├── start-server.sh              # Script para iniciar servidor
└── taller-1/
    ├── sesion-1/
    │   ├── index.html           # Presentación (39 diapositivas)
    │   ├── assets/              # Imágenes y gráficos
    │   └── index_files/         # Librerías y dependencias
    └── sesion-2/
        ├── index.html           # Presentación (21 diapositivas)
        ├── assets/              # Imágenes y gráficos
        ├── animaciones.js       # Scripts de animación
        ├── interacciones.js     # Scripts de interactividad
        └── index_files/         # Librerías y dependencias
```

---

## 🔐 Notas de Seguridad
- Este servidor es **solo para desarrollo/presentación local**
- NO se recomienda exponerlo a internet sin medidas de seguridad adicionales
- Los datos se sirven desde esta máquina, sin encriptación por defecto

---

## 📞 Soporte
Si algo no funciona:
1. Verifica que el puerto 8000 no esté en uso: `lsof -i :8000`
2. Recarga la página con `Ctrl+Shift+R`
3. Abre la consola (`F12`) para ver errores
4. Reinicia el servidor si es necesario

---

**Última actualización**: 2026-11-20  
**Estado**: ✅ Funcionando correctamente  
**Servidor**: Python HTTP Server en puerto 8000
