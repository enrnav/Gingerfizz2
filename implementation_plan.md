# Plan de Implementación: GingerFizz Dashboard

Aplicación web con diseño moderno premium (paleta de colores naranja y blanco) para gestionar necesidades de clientes e inventario, además de un sistema de autenticación de usuarios y notificaciones automáticas.

## User Review Required
> [!IMPORTANT]
> Propongo utilizar **Flask** como framework web para Python. Es un framework muy ligero, moderno, e ideal para aplicaciones de este tamaño que utilizan SQLite y requieren rápida integración con plantillas de HTML. ¿Estás de acuerdo con avanzar utilizando Flask, o prefieres una alternativa como FastAPI/Django?

## Proposed Changes

La aplicación se construirá de una manera modular en la ruta `/Desktop/PAGINA DE EDWIN/Gingerfizz2/`.

### Dominio de Backend y Configuración
#### [NEW] `app.py`
Archivo principal de la aplicación Flask. Alojará la inicialización, configuración de sesión, la conexión a la base de datos y los controladores principales.
#### [NEW] `models.py`
Configuración de la conexión a SQLite y definición de las tablas necesarias (`Usuario`, `Inventario`, `NecesidadCliente`, `Notificacion`).
#### [NEW] `requirements.txt`
Dependencias del entorno Python (Ej: `Flask`, `Flask-Session`, `Werkzeug`).

### Vistas y Plantillas de UI
#### [NEW] `templates/base.html`
Plantilla HTML raíz que importará Tailwind CSS y establecerá los diseños estándar usando nuestros colores naranja (`bg-orange-500`, etc.) y blanco junto a fuentes modernas. Aquí se agregará el logo moderno que diga "GingerFizz" y una barra de navegación (responsive).
#### [NEW] `templates/auth/login.html` & `templates/auth/register.html`
Formularios de autenticación de usuario. Aplicarán principios de diseño visual premium (ej: glassmorphism, sombras pronunciadas).
#### [NEW] `templates/dashboard/index.html`
El Dashboard principal. Presentará dinámicamente: resumen del inventario, gestión de las necesidades de clientes y área de notificaciones.
#### [NEW] `templates/dashboard/inventory.html`
Vista específica para agregar productos o visualizar los registros. Utilizará JavaScript para renderizar automáticamente 'cuántos hay' versus 'cuántos faltan'.

### Assets Estáticos (CSS y JS extra)
#### [NEW] `static/css/styles.css`
Aquí irán micro-animaciones personalizadas y clases de utilidad en Vanilla CSS para apoyar fuertemente el trabajo estético de Tailwind y darle un acabado "wow" a la app.
#### [NEW] `static/js/main.js`
Lógica frontend para manipular notificaciones emergentes (toasts) e interacciones asíncronas ligeras sin recargar toda la página web.

## Verification Plan

### Manual Verification
1. Instalar dependencias mediante Python y correr `flask run`.
2. Acceder al inicio, registrar un nuevo usuario con contraseñas cifradas y autenticarse.
3. Evaluar el diseño en versión móvil (teléfono móvil, responsivo) y versión escritorio, garantizando que cumple la estética premium, y validando los colores Naranja/Blanco.
4. Agregar registros al Inventario y Needs del Cliente, validar que las operativas matemáticas del sistema (disponibilidad y faltantes) respondan según lo requerido.
