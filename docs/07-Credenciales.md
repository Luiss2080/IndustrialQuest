# Gestión de Credenciales y Sesiones

Este documento aclara el funcionamiento y la seguridad del videojuego **IndustrialQuest** en relación con el almacenamiento de credenciales, autenticación de usuarios y persistencia de estados.

---

## 1. Ausencia de Autenticación de Usuarios

**IndustrialQuest** es un videojuego educativo de escritorio offline. 

- **Sin Servidor Central/Registro:** No requiere un inicio de sesión, credenciales de usuario (como contraseñas o nombres de usuario) ni conexión a bases de datos remotas.
- **Sin API Keys/Secretos:** El juego no utiliza servicios de terceros en la nube, por lo que no existen tokens de API, llaves públicas/privadas ni archivos de configuración con secretos incrustados.

---

## 2. Persistencia del Estado de Juego

El progreso del usuario (como la puntuación actual, las vidas restantes y el tiempo transcurrido) es **efímero** (transitorio) y reside exclusivamente en la memoria RAM del equipo del cliente durante la ejecución de la aplicación:

- Las estadísticas se manejan a nivel de clase dentro de la instancia de `MotorJuego` (`self.puntuacion`, `self.vidas`, etc.).
- Al cerrarse la ventana del juego o desencadenarse un *Game Over*, estas variables se restablecen a sus valores por defecto al iniciar una nueva partida.
- No se realiza almacenamiento en archivos locales (como archivos JSON o bases de datos SQLite) ni escrituras de registro del sistema.

---

## 3. Seguridad Local

Dado que la aplicación se ejecuta de forma local y no realiza conexiones de red:
- No existen riesgos de interceptación de datos de sesión.
- Cualquier modificación del código fuente local puede alterar las estadísticas, lo cual es de nulo impacto dado el enfoque meramente educativo y recreativo sin marcadores globales competitivos online.
