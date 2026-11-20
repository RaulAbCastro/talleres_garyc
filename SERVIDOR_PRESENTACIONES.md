# 🎓 Servidor de Presentaciones - Talleres GARyC

## Estado del Servidor
✅ **El servidor está corriendo en puerto 8000**

## Acceso a las Presentaciones

### Página Principal
```
http://localhost:8000
```
Desde aquí puedes acceder a todas las sesiones.

### Sesiones Disponibles

#### 📊 Sesión 1: De la muestra a la inferencia
```
http://localhost:8000/taller-1/sesion-1/
```
Fundamentos de estadística inferencial con datos bancarios. Distribuciones muestrales, intervalos de confianza y contrastes de hipótesis.

#### 🎯 Sesión 2: Resultados potenciales y sesgo de selección
```
http://localhost:8000/taller-1/sesion-2/
```
Introducción a causalidad observacional. Contrafactuales, ATE, ATT y el poder de la aleatorización para resolver sesgo de selección.

## Cómo Acceder

### Opción 1: Local (desde la máquina)
Abre tu navegador e ingresa:
```
http://localhost:8000
```

### Opción 2: Desde Codespaces (Forwarded Port)
Si estás en Codespaces:
1. Ve a la terminal
2. Busca el puerto 8000 en "Ports" (abajo a la derecha)
3. Haz clic en la URL pública que aparece

### Opción 3: Acceso remoto
Si necesitas acceder desde otra máquina, reemplaza `localhost` con:
- IP de la máquina: `http://<ip-address>:8000`
- Dominio: `http://<domain>:8000`

## Troubleshooting

### Si no ves las presentaciones:
1. **Recarga la página** (Ctrl+F5 o Cmd+Shift+R para limpiar caché)
2. **Verifica la consola** (F12) para errores
3. **Comprueba que el servidor está corriendo**:
   ```bash
   ps aux | grep "http.server 8000"
   ```

### Si faltan recursos (CSS, JS):
Los archivos están en:
- `/workspaces/talleres_garyc/slides/taller-1/sesion-1/index_files/`
- `/workspaces/talleres_garyc/slides/taller-1/sesion-2/index_files/`

Verifica que existen y tienen contenido.

## Iniciar/Detener el Servidor

### Iniciar
```bash
cd /workspaces/talleres_garyc/slides
python3 -m http.server 8000
```

### Detener
Presiona `Ctrl+C` en la terminal donde corre el servidor.

---
**Generado por Copilot** | Talleres GARyC 2026
