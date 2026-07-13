# Plan de migración a Firebase Authentication

**Estado:** Pendiente — planificado para un sprint específico de arquitectura.
**Última actualización:** Junio 2026
**Contexto:** Colliers Nexus (`index.html`, single-file + Firestore + Vercel).

> Objetivo del documento: dejar asentado por qué el modelo de permisos actual es
> suficiente para seguir evolucionando los módulos funcionales, y qué se necesita
> para migrar a un enforcement real de permisos con Firebase Auth cuando el resto
> de los módulos estén estabilizados.

---

## 1. Cómo funciona hoy el modelo de permisos

### 1.1. Autenticación
- El login se hace con **Google Identity Services (GSI)** en el cliente.
- `handlePayload(payload)` decodifica el JWT de Google, setea la variable global
  `user = { email, displayName, ... }` y valida el dominio contra
  `ALLOWED_DOMAINS = ["gmail.com","colliers.com.ar","colliers.com"]`.
- Firebase se inicializa **sólo** con `firebase.initializeApp(FIREBASE_CONFIG)`.
  **No** se llama a `firebase.auth()` ni a `signInWithCredential`.

### 1.2. Autorización (roles)
- No hay un sistema de roles formal. El "rol admin" es una **whitelist de emails**:
  ```js
  const ANALYTICS_ALLOWED = [
    'mazaretto@gmail.com', 'matias.azaretto@colliers.com',
    'colliers.arg@gmail.com', 'desarrollo@colliers.com.ar'
  ];
  ```
- `ANALYTICS_ALLOWED` controla: visibilidad de **Analytics**, del módulo
  **Administración**, y de los campos restringidos de Cuenta
  (**Categoría, Rubro, Subrubro, Gestionado por**) vía `_cdrIsAdmin()`.

### 1.3. Acceso a datos
- Todo el acceso a Firestore es `db.collection(...)` **sin sesión de Firebase Auth**.
- Desde la perspectiva de Firestore, **todas las peticiones son anónimas**
  (`request.auth == null`).
- Las reglas activas (`firestore.rules`, Sección A) validan **integridad de datos**
  (tipos, estructura, tamaños de `rubros`/`subrubros`, etc.), pero **no** identidad.

---

## 2. Limitaciones del modelo actual

| # | Limitación | Detalle / Riesgo |
|---|------------|------------------|
| 1 | **Permisos sólo en el cliente** | El gating de admin (Categoría/Rubro/Gestionado por, Analytics, Admin) vive en JS. Un usuario técnico puede escribir directo a Firestore (SDK/consola/REST) saltándose la UI. |
| 2 | **Firestore sin identidad** | Como `request.auth` es nulo, las reglas no pueden distinguir usuarios ni admins. La seguridad server-side se limita a validar la **forma** de los datos, no **quién** los escribe. |
| 3 | **Base de datos efectivamente abierta** | Las reglas de las demás colecciones son `allow read, write: if true`. Cualquiera con la config de Firebase (que viaja en el cliente) podría leer/escribir. |
| 4 | **Relación subrubro→rubro no validable en reglas** | El lenguaje de reglas no itera listas; esa integridad se valida sólo en el cliente (`_cdrValidSubrubros`). |
| 5 | **Whitelist hardcodeada** | Cambiar admins requiere editar `index.html` y redeployar; no es gestionable desde una UI ni desde claims. |
| 6 | **Sin auditoría confiable de autor** | Campos como `capturadoPor`/`usuarioUltimaModificacion` se setean desde el cliente y podrían falsificarse. |

> **Por qué es aceptable por ahora:** el uso es interno, con dominios corporativos
> controlados y un equipo acotado y de confianza. La prioridad es estabilizar los
> módulos funcionales; el endurecimiento server-side se difiere a un sprint propio.

---

## 3. Cambios necesarios para migrar a Firebase Auth

### 3.1. Idea central
Iniciar sesión en **Firebase Auth** con la credencial de Google que ya devuelve GSI,
para que Firestore reciba `request.auth` y las reglas puedan enforcar permisos por rol.

### 3.2. Pasos

1. **Habilitar el proveedor Google** en Firebase Console → Authentication → Sign-in
   method → Google (Enable).
2. **Authorized domains** en Authentication → Settings: agregar los dominios de
   Vercel (producción y previews) además de `localhost`.
3. **Alinear el OAuth Client ID**: el `id_token` de GSI debe tener un `aud`
   (client_id) reconocido por Firebase. Opciones:
   - Usar el **Web client ID** que Firebase crea para el proyecto como client de GSI, **o**
   - Agregar el client_id actual de GSI a la config del proveedor Google en Firebase.
   > ⚠️ Gotcha típico: `auth/invalid-credential` o `aud` mismatch si el client_id de
   > GSI no coincide con el que Firebase espera. Resolver acá antes de tocar reglas.
4. **Agregar el SDK de Firebase Auth (compat)** en el `<head>`:
   ```html
   <script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-auth-compat.js"></script>
   ```
5. **Sign-in en el flujo de login** (`handlePayload`), usando el `id_token` crudo
   que hoy ya se recibe de GSI:
   ```js
   const cred = firebase.auth.GoogleAuthProvider.credential(id_token);
   await firebase.auth().signInWithCredential(cred);
   ```
   - Capturar el `id_token` sin procesar (hoy se decodifica el JWT; hay que guardar
     también el token original).
   - Preferentemente derivar `user` de `firebase.auth().currentUser` y/o esperar a
     `onAuthStateChanged` antes de arrancar la carga de datos.
6. **Logout**: en el botón "Salir" agregar `firebase.auth().signOut()`.
7. **Gating de arranque**: no disparar los `load*()` de Firestore hasta que la sesión
   de Firebase Auth esté establecida (evita lecturas denegadas por reglas nuevas).
8. **Activar la Sección B de `firestore.rules`** (permisos por rol) y **endurecer**
   las demás colecciones de `if true` a por lo menos `if isSignedIn()`.
9. (Opcional recomendado) Migrar la whitelist de admins a **Custom Claims**
   (`admin: true`) vía Cloud Function / Admin SDK, para no hardcodear emails en
   reglas ni en el cliente.

---

## 4. Archivos que se deberán modificar

| Archivo | Cambio |
|---------|--------|
| `index.html` | Agregar SDK `firebase-auth-compat.js`; en `handlePayload` capturar el `id_token` y hacer `signInWithCredential`; gatear el arranque a `onAuthStateChanged`; `signOut()` en el logout. (Opcional) leer rol desde `getIdTokenResult().claims`. |
| `firestore.rules` | Reemplazar el bloque `match /clientes/...` de la **Sección A** por la **Sección B** (ya escrita y comentada). Endurecer `contactos`, `buildings`, `leads`, `descargas`, `transacciones`, `timeline`, `history`, `sheets`, `feedback` a `if isSignedIn()` (o reglas por colección más finas). |
| Firebase Console (no es archivo, pero es parte del cambio) | Habilitar proveedor Google; authorized domains; alinear OAuth client_id. |
| (Opcional) `functions/` nuevo | Cloud Function para setear Custom Claims `admin` si se migra la whitelist a claims. |
| `HANDOVER.md` / `CLAUDE.md` | Actualizar la sección de Auth y el estado de las reglas una vez migrado. |

---

## 5. Impacto sobre usuarios, permisos y reglas

### 5.1. Usuarios
- **Re-login**: al desplegar, los usuarios deberán volver a iniciar sesión (ahora
  también contra Firebase Auth).
- **Dominios**: `ALLOWED_DOMAINS` (cliente) debe quedar consistente con los
  *authorized domains* de Firebase Auth y con el consent de Google Workspace.
- **Riesgo de lockout**: si el sign-in de Firebase falla (aud mismatch, dominio no
  autorizado) y las reglas ya exigen auth, la app queda inaccesible → **probar en un
  proyecto/entorno de staging o con las reglas de la Sección A aún activas** hasta
  confirmar que `request.auth` llega bien.

### 5.2. Permisos
- El gating de admin pasa de **cosmético (UI)** a **efectivo (server-side)**: un
  no-admin no podrá escribir `categoria/rubro/subRubro/rubros/subrubros/gestionadoPor/
  ejecutivoComercial` ni siquiera saltándose la UI.
- Lecturas: pasan a requerir sesión (deja de ser base abierta).
- La whitelist de emails puede seguir en las reglas (Sección B) o migrar a Custom
  Claims (más escalable y sin redeploy de `index.html`).

### 5.3. Reglas
- Se activa la **Sección B** de `firestore.rules` (identidad + permisos por campo).
- La relación **subrubro→rubro** seguirá validándose en el cliente (limitación del
  lenguaje de reglas); las reglas cubren tipos/estructura/tamaños.
- **Rollback**: si algo falla, revertir `firestore.rules` a la **Sección A**
  restablece el comportamiento actual sin tocar `index.html`.

---

## 6. Checklist de migración (para el sprint de arquitectura)

- [ ] Habilitar proveedor Google en Firebase Auth + authorized domains.
- [ ] Alinear/verificar el OAuth client_id (evitar `aud` mismatch).
- [ ] Agregar `firebase-auth-compat.js` al `<head>`.
- [ ] `signInWithCredential` en `handlePayload` (capturar `id_token` crudo).
- [ ] Gatear arranque de datos a `onAuthStateChanged` / sesión lista.
- [ ] `signOut()` en el logout.
- [ ] Verificar en **staging** que `request.auth.token.email` llega en las reglas.
- [ ] Endurecer colecciones a `if isSignedIn()` y activar Sección B para `/clientes`.
- [ ] Probar: admin puede editar campos restringidos; no-admin no; lecturas OK.
- [ ] (Opcional) Migrar whitelist de admins a Custom Claims.
- [ ] Actualizar `HANDOVER.md` / `CLAUDE.md`.

---

## 7. Estado actual (referencia rápida)

- ✅ `firestore.rules` con Sección A (integridad, sin auth) **activa** y Sección B
  (permisos por rol) **lista y comentada**.
- ✅ Gating de admin client-side vía `ANALYTICS_ALLOWED` / `_cdrIsAdmin()`.
- ✅ Integridad rubro/subrubro validada en el cliente (`_cdrValidSubrubros`).
- ⏳ Firebase Auth: **diferido** a este sprint de arquitectura.
