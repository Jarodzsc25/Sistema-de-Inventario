const API_BASE = "http://localhost:5000/api";

// ===================================
// === FUNCIÓN AUXILIAR DE CABECERAS ===
// ===================================
// 1. FUNCIÓN AUXILIAR: Obtiene el token y crea las cabeceras
function getAuthHeaders(contentType = "application/json") {
  const token = localStorage.getItem('token');
  const headers = {};

  if (contentType) {
    headers["Content-Type"] = contentType;
  }

  // Si hay token, lo adjunta en el formato 'Authorization: Bearer <token>'
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
}

// =====================================
// === FUNCIÓN AUXILIAR DE RESPUESTAS ===
// =====================================
// 2. FUNCIÓN AUXILIAR: Maneja la respuesta de la API (Éxito o Error)
async function handleResponse(res) {
    // 🛑 CORRECCIÓN CLAVE: Clona la respuesta para leer el cuerpo
    // sin afectar el flujo si res.json() falla.
    const clonedRes = res.clone();

    // 1. Manejo de Errores (4xx, 5xx)
    if (!res.ok) {
        // Intenta obtener el error del cuerpo JSON (si está disponible)
        // Usamos la respuesta CLONADA aquí
        const errorData = await clonedRes.json().catch(() => ({
            message: res.statusText || "Error desconocido del servidor"
        }));

        // Manejo específico para token expirado/inválido (401)
        if (res.status === 401 && window.location.pathname.endsWith('dashboard.html')) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            // Redirigir para forzar el re-login
            window.location.href = 'index.html?expired=true';
        }

        // Lanza un error con el mensaje de la API o el estado HTTP
        const errorMessage = errorData.detalle || errorData.error || errorData.message || errorData.msg || res.statusText;
        throw new Error(`API Error: ${res.status} - ${errorMessage}`);
    }

    // 2. Manejo de Éxito (2xx) - LÓGICA CORREGIDA
    try {
        // 🟢 LEE la respuesta como texto primero.
        const text = await res.text();
        // Si el texto NO está vacío, parsea a JSON. Si está vacío, devuelve lista vacía ([]).
        return text ? JSON.parse(text) : [];

    } catch (e) {
        // Esto captura errores si el cuerpo no es JSON.
        console.error("Error al parsear JSON en handleResponse:", e);
        // Devuelve una lista vacía para que el frontend pueda manejar la ausencia de datos
        return [];
    }
}

// ===================================
// === API AUTENTICACIÓN (PÚBLICA) ===
// ===================================

// Función corregida para manejar el error 401 en el login
async function loginUser(username, password) {
  const res = await fetch(`${API_BASE}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  // Usa el manejador de respuesta para verificar el 401
  return handleResponse(res);
}

// ========================================
// === API PRODUCTOS (PROTEGIDAS) ===
// ========================================
async function getProductos() {
  const res = await fetch(`${API_BASE}/producto`, {
    headers: getAuthHeaders()
  });
  return handleResponse(res);
}
async function createProducto(data) {
  const res = await fetch(`${API_BASE}/producto/`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });
  return handleResponse(res);
}
async function updateProducto(id, data) {
  const res = await fetch(`${API_BASE}/producto/${id}`, {
    method: "PUT",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });
  return handleResponse(res);
}
async function deleteProducto(id) {
  const res = await fetch(`${API_BASE}/producto/${id}`, {
    method: "DELETE",
    headers: getAuthHeaders(null),
  });
  return handleResponse(res);
}

// ========================================
// === API DISTRIBUIDORES (PROTEGIDAS) ===
// ========================================
async function getDistribuidores() {
  const res = await fetch(`${API_BASE}/distribuidor`, {
    headers: getAuthHeaders()
  });
  return handleResponse(res);
}
async function createDistribuidor(data) {
  const res = await fetch(`${API_BASE}/distribuidor`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });
  return handleResponse(res);
}
async function updateDistribuidor(id, data) {
  const res = await fetch(`${API_BASE}/distribuidor/${id}`, {
    method: "PUT",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });
  return handleResponse(res);
}
async function deleteDistribuidor(id) {
  const res = await fetch(`${API_BASE}/distribuidor/${id}`, {
    method: "DELETE",
    headers: getAuthHeaders(null),
  });
  return handleResponse(res);
}

// ========================================
// === API MOVIMIENTOS (PROTEGIDAS) - CRUD COMPLETO ===
// ========================================

/**
 * Obtiene todos los movimientos de inventario. (READ - List)
 * Asume endpoint GET /api/movimiento
 */
async function getMovimientos() {
  const res = await fetch(`${API_BASE}/movimiento`, {
    headers: getAuthHeaders()
  });
  return handleResponse(res);
}

/**
 * Obtiene un movimiento específico por ID. (READ - Single)
 * Asume endpoint GET /api/movimiento/{id}
 */
async function getMovimiento(id) {
  const res = await fetch(`${API_BASE}/movimiento/${id}`, {
    headers: getAuthHeaders()
  });
  return handleResponse(res);
}

/**
 * Crea un nuevo movimiento de inventario (Entrada o Salida). (CREATE)
 * Asume endpoint POST /api/movimiento
 */
async function createMovimiento(data) {
  const res = await fetch(`${API_BASE}/movimiento`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });
  return handleResponse(res);
}

/**
 * Actualiza un movimiento de inventario existente. (UPDATE)
 * Asume endpoint PUT /api/movimiento/{id}
 */
async function updateMovimiento(id, data) {
  const res = await fetch(`${API_BASE}/movimiento/${id}`, {
    method: "PUT",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });
  return handleResponse(res);
}

/**
 * Elimina un movimiento de inventario. (DELETE)
 * Asume endpoint DELETE /api/movimiento/{id}
 */
async function deleteMovimiento(id) {
  const res = await fetch(`${API_BASE}/movimiento/${id}`, {
    method: "DELETE",
    headers: getAuthHeaders(null),
  });
  return handleResponse(res);
}


// ========================================
// === API KARDEX (PROTEGIDAS) - SOLO LECTURA ===
// ========================================

/**
 * Obtiene todos los registros de Kardex (historial de inventario). (READ)
 * Asume endpoint GET /api/kardex
 */
async function getKardexs() {
  const res = await fetch(`${API_BASE}/kardex`, {
    headers: getAuthHeaders()
  });
  // Se deja esta función para compatibilidad con el código viejo
  return handleResponse(res);
}

/**
 * Obtiene el reporte completo de Kardex (solo para rol Administrador).
 * @returns {Promise<Array>} Lista de registros del Kardex.
 */
async function getKardex() {
  const url = `${API_BASE}/kardex/`;
  const res = await fetch(url, {
    method: "GET",
    headers: getAuthHeaders(),
  });
  // Esta función usa el manejador de respuesta corregido
  return handleResponse(res);
}


// ========================================
// === API USUARIOS (PROTEGIDAS) ===
// ========================================
async function getUsuarios() {
  const res = await fetch(`${API_BASE}/usuario/`, {
    headers: getAuthHeaders()
  });
  return handleResponse(res);
}
async function createUsuario(data) {
  const res = await fetch(`${API_BASE}/usuario/`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });
  return handleResponse(res);
}
async function updateUsuario(id, data) {
  const res = await fetch(`${API_BASE}/usuario/${id}`, {
    method: "PUT",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });
  return handleResponse(res);
}
async function deleteUsuario(id) {
  const res = await fetch(`${API_BASE}/usuario/${id}`, {
    method: "DELETE",
    headers: getAuthHeaders(null),
  });
  return handleResponse(res);
}

// ========================================
// === API ROLES (PROTEGIDAS) ===
// ========================================
async function getRoles() {
  const res = await fetch(`${API_BASE}/rol/`, {
    headers: getAuthHeaders()
  });
  return handleResponse(res);
}
async function createRol(data) {
  const res = await fetch(`${API_BASE}/rol/`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });
  return handleResponse(res);
}
async function updateRol(id, data) {
  const res = await fetch(`${API_BASE}/rol/${id}`, {
    method: "PUT",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });
  return handleResponse(res);
}
async function deleteRol(id) {
  const res = await fetch(`${API_BASE}/rol/${id}`, {
    method: "DELETE",
    headers: getAuthHeaders(null),
  });
  return handleResponse(res);
}

// ========================================
// === API PERSONAS (PROTEGIDAS) ===
// ========================================
async function getPersonas() {
  const res = await fetch(`${API_BASE}/persona/`, {
    headers: getAuthHeaders()
  });
  return handleResponse(res);
}
async function createPersona(data) {
  const res = await fetch(`${API_BASE}/persona/`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });
  return handleResponse(res);
}
async function updatePersona(id, data) {
  const res = await fetch(`${API_BASE}/persona/${id}`, {
    method: "PUT",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });
  return handleResponse(res);
}
async function deletePersona(id) {
  const res = await fetch(`${API_BASE}/persona/${id}`, {
    method: "DELETE",
    headers: getAuthHeaders(null),
  });
  return handleResponse(res);
}