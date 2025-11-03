const API_BASE = "http://localhost:5000/api";

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
// -------------------------------------------------------------------

// NOTA: loginUser NO NECESITA el token (es la ruta para obtenerlo)
async function loginUser(username, password) {
  const res = await fetch(`${API_BASE}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  return res.json();
}

// === API PRODUCTOS ===
async function getProductos() {
  const res = await fetch(`${API_BASE}/producto`, { // Modificado
    headers: getAuthHeaders()
  });
  return res.json();
}
async function createProducto(data) {
  const res = await fetch(`${API_BASE}/producto/`, {
    method: "POST",
    headers: getAuthHeaders(), // Modificado
    body: JSON.stringify(data),
  });
  return res.json();
}

async function updateProducto(id, data) {
  const res = await fetch(`${API_BASE}/producto/${id}`, {
    method: "PUT",
    headers: getAuthHeaders(), // Modificado
    body: JSON.stringify(data),
  });
  return res.json();
}

async function deleteProducto(id) {
  const res = await fetch(`${API_BASE}/producto/${id}`, {
    method: "DELETE",
    headers: getAuthHeaders(null), // Modificado (DELETE no siempre requiere Content-Type)
  });
  return res.json();
}

// === API DISTRIBUIDORES ===
async function getDistribuidores() {
  const res = await fetch(`${API_BASE}/distribuidor`, { // Modificado
    headers: getAuthHeaders()
  });
  return res.json();
}

async function createDistribuidor(data) {
  const res = await fetch(`${API_BASE}/distribuidor`, {
    method: "POST",
    headers: getAuthHeaders(), // Modificado
    body: JSON.stringify(data),
  });
  return res.json();
}

async function updateDistribuidor(id, data) {
  const res = await fetch(`${API_BASE}/distribuidor/${id}`, {
    method: "PUT",
    headers: getAuthHeaders(), // Modificado
    body: JSON.stringify(data),
  });
  return res.json();
}

async function deleteDistribuidor(id) {
  const res = await fetch(`${API_BASE}/distribuidor/${id}`, {
    method: "DELETE",
    headers: getAuthHeaders(null), // Modificado
  });
  return res.json();
}

// === API MOVIMIENTOS ===
async function getMovimientos() {
  const res = await fetch(`${API_BASE}/movimiento`, { // Modificado
    headers: getAuthHeaders()
  });
  return res.json();
}

// === API USUARIOS ===
async function getUsuarios() {
  const res = await fetch(`${API_BASE}/usuario/`, { // Modificado
    headers: getAuthHeaders()
  });
  return res.json();
}

async function createUsuario(data) {
  const res = await fetch(`${API_BASE}/usuario/`, {
    method: "POST",
    headers: getAuthHeaders(), // Modificado
    body: JSON.stringify(data),
  });
  return res.json();
}

async function updateUsuario(id, data) {
  const res = await fetch(`${API_BASE}/usuario/${id}`, {
    method: "PUT",
    headers: getAuthHeaders(), // Modificado
    body: JSON.stringify(data),
  });
  return res.json();
}

async function deleteUsuario(id) {
  const res = await fetch(`${API_BASE}/usuario/${id}`, {
    method: "DELETE",
    headers: getAuthHeaders(null), // Modificado
  });
  return res.json();
}

// === API ROLES ===
async function getRoles() {
  const res = await fetch(`${API_BASE}/rol/`, { // Modificado
    headers: getAuthHeaders()
  });
  return res.json();
}

async function createRol(data) {
  const res = await fetch(`${API_BASE}/rol/`, {
    method: "POST",
    headers: getAuthHeaders(), // Modificado
    body: JSON.stringify(data),
  });
  return res.json();
}

async function updateRol(id, data) {
  const res = await fetch(`${API_BASE}/rol/${id}`, {
    method: "PUT",
    headers: getAuthHeaders(), // Modificado
    body: JSON.stringify(data),
  });
  return res.json();
}

async function deleteRol(id) {
  const res = await fetch(`${API_BASE}/rol/${id}`, {
    method: "DELETE",
    headers: getAuthHeaders(null), // Modificado
  });
  return res.json();
}

// === API PERSONAS ===
async function getPersonas() {
  const res = await fetch(`${API_BASE}/persona/`, { // Modificado
    headers: getAuthHeaders()
  });
  return res.json();
}

async function createPersona(data) {
  const res = await fetch(`${API_BASE}/persona/`, {
    method: "POST",
    headers: getAuthHeaders(), // Modificado
    body: JSON.stringify(data),
  });
  return res.json();
}

async function updatePersona(id, data) {
  const res = await fetch(`${API_BASE}/persona/${id}`, {
    method: "PUT",
    headers: getAuthHeaders(), // Modificado
    body: JSON.stringify(data),
  });
  return res.json();
}

async function deletePersona(id) {
  const res = await fetch(`${API_BASE}/persona/${id}`, {
    method: "DELETE",
    headers: getAuthHeaders(null), // Modificado
  });
  return res.json();
}