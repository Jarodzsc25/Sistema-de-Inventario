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
    // Si la respuesta NO es OK (ej. 401, 403, 404, 500), lanza un error
    if (!res.ok) {
        // Intenta obtener el error del cuerpo JSON (si está disponible)
        const errorData = await res.json().catch(() => ({ message: res.statusText }));

        // Manejo específico para token expirado/inválido (401 en rutas protegidas)
        if (res.status === 401 && window.location.pathname.endsWith('dashboard.html')) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            // Redirigir para forzar el re-login
            window.location.href = 'index.html?expired=true';
        }

        // Lanza un error que será capturado por el bloque 'catch' en auth.js
        const errorMessage = errorData.message || errorData.msg || res.statusText;
        throw new Error(`API Error: ${res.status} - ${errorMessage}`);
    }
    // Si la respuesta es OK (2xx), devuelve el cuerpo en formato JSON
    return res.json();
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
// === API MOVIMIENTOS (PROTEGIDAS) ===
// ========================================
async function getMovimientos() {
  const res = await fetch(`${API_BASE}/movimiento`, {
    headers: getAuthHeaders()
  });
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