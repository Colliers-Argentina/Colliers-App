# Colliers Nexus — Contexto del Proyecto

## Descripción
SaaS inmobiliario para Colliers Argentina. **Un solo archivo**: `index.html` (~6200 líneas). Sin build system, sin npm, sin framework. HTML + CSS + JS inline.

## Stack
- **Firebase Firestore** compat SDK v10.7.1 (modo compat: `db.collection(...)`)
- **Auth**: Google Identity Services (GSI), login con Google
- **Mapa**: Leaflet.js 1.9.4 + Leaflet.markercluster 1.5.3, tiles CartoDB Voyager
- **PPTs**: PptxGenJS 3.12.0 (CDN)
- **Deploy**: Vercel — push a `main` = autodeploy

## Seguridad crítica — NO ROMPER
```javascript
const ANALYTICS_ALLOWED = ['mazaretto@gmail.com', 'matias.azaretto@colliers.com'];
```
Los usuarios no autorizados NO deben ver Analytics — ni deshabilitado ni griseado: **directamente inexistente en la UI**.

## Firestore — Colecciones

| Colección | Descripción |
|-----------|-------------|
| `clientes` | Cuentas (empresas). También referenciada como "cuentas" en la UI |
| `contactos` | Personas, vinculadas a cuentas via `cuentaId` |
| `buildings` | Edificios del inventario |
| `descargas` | Historial de PPTs generados (analytics) |
| `timeline` | Eventos de CRM por cliente |
| `history` | Historial de cambios de edificios |
| `sheets` | Datos sincronizados desde Google Sheets |
| `feedback` | Feedback de usuarios |

## Módulos de la app

La app tiene una barra de navegación lateral/superior. Los módulos son:
- **home** — Dashboard / inicio
- **crm** — CRM (Leads / Cuentas / Contactos)
- **generator** — Generador de informes PPT
- **buildings / inventario** — Inventario de edificios
- **analytics** — Solo visible para `ANALYTICS_ALLOWED`

## Módulo CRM (estructura actual)

Subnav horizontal con 3 secciones:
1. **Cuentas** (`#crm-cuentas-section`) — antigua "Clientes". Lista + detalle. Drawer "Nueva Cuenta" (`#cdr-drawer`).
2. **Contactos** (`#crm-contactos-section`) — nuevo. Lista + detalle. Drawer "Nuevo Contacto" (`#ctdr-drawer`). Colección Firestore `contactos`.
3. **Leads** (`#crm-leads-section`) — placeholder "Próximamente".

### Ficha de Cuenta (openClientDetail)
Tabs: Información / Resumen / Búsquedas / PPTs generados / Alternativas enviadas / Notas / **Contactos** / Timeline

El tab Contactos llama `loadCuentaContactos(cuentaId)` que consulta `contactos` where `cuentaId==`.

### Datos de Cuenta (Firestore `clientes`)
`nombre`, `razonSocial`, `categoria`, `ubicacionPrincipal`, `clienteColliers`, `propietarioOcupante`, `contactoPrincipal`, `cargo`, `emailContacto`, `telefono`, `sitioWeb`, `rubro`, `subRubro`, `bu`, `esBroker`, `cuentaCorporativa`, `esDesarrollador`, `esAdministradora`, `brokerCreador`, `pptsGenerados`, `cantidadPPTs`, `fechaCreacion`, `ultimaActividad`

### Datos de Contacto (Firestore `contactos`)
`cuentaId`, `cuentaNombre`, `nombre`, `apellidos`, `cargo` (segmentado), `puesto`, `propietario`, `email`, `estadoCorreo` (funcional/sin_comprobar/rebotado), `telefono`, `interno`, `linkedin`, `inversor`, `prefsInversion[]`, `volumenInversion`, `comentarios`, `brokerResponsable`, `fechaCreacion`, `ultimoContacto`, `ultimaActividad`

## Módulo Inventario (Buildings)

- Vistas: grid / lista / mapa
- Mapa con clustering (`L.markerClusterGroup`)
- Tiles: CartoDB Voyager
- Importar datos desde Google Sheets (parseCSV)
- Geocodificación: prioridad Sheet lat/lng → gMapsAddr → direccion
- Campos de Sheet soportados: `Google Maps Address`, `Latitud`, `Longitud`

## Helpers JS importantes

```javascript
function _tsToDate(ts){if(!ts)return null;if(ts.toDate)return ts.toDate();if(ts.seconds)return new Date(ts.seconds*1000);return new Date(ts);}
function fmtDate(ts){...}  // formatea Timestamp o Date a "dd MMM yyyy"
function fmtM2Range(min,max){...}  // "600 – 1.000 m²"

// Drawer de Cuenta:
function cdrVal(id)          // leer input por id
function cdrToggleVal(field) // leer toggle activo
window.cdrToggle(btn)        // toggle exclusivo (data-field)

// Drawer de Contacto:
window.ctdrTogglePref(btn)   // toggle NO exclusivo para prefs de inversión
```

## Variables globales clave

```javascript
let user = null;              // usuario logueado (GSI)
let _crmDocs = [];            // cuentas cargadas
let _ctoDocs = [];            // contactos cargados
let _bldDocs = [];            // edificios
let _anDocs = [];             // descargas (analytics)
let _crmActiveTab = 'cuentas'; // tab activo del CRM
let _clientesCache = [];      // cache para selector de clientes en generator
```

## Firebase Config

```javascript
const FIREBASE_CONFIG = {
  apiKey: "AIzaSyDmV3KCBD0euDgtbw2nQ-ynw2aB_CDGq-A",
  projectId: "colliers-alternativas-1db71",
  // ... (ver index.html línea ~2413)
};
```

## Git

- **Feature branch activo**: `claude/update-dom-constant-8eiPY`
- **Push a main** = deploy automático en Vercel
- Siempre hacer push a ambos: `git push origin <branch>:main`

## Verificación de sintaxis JS

```bash
SCRIPT_START=$(grep -n "^<script>$" index.html | head -1 | cut -d: -f1)
SCRIPT_END=$(grep -n "^</script>" index.html | tail -1 | cut -d: -f1)
sed -n "$((SCRIPT_START+1)),$((SCRIPT_END-1))p" index.html > /tmp/check.mjs && node --check /tmp/check.mjs && echo "SYNTAX OK"
```

## Convenciones de código

- Sin comentarios salvo cuando el WHY es no obvio
- Sin abstracciones prematuras
- Sin manejo de errores para escenarios imposibles
- CSS inline en JS para elementos generados dinámicamente (template literals)
- Timestamps de Firestore: siempre usar `_tsToDate(ts)` para convertir, `firebase.firestore.Timestamp.now()` para crear
