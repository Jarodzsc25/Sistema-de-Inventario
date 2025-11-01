const API_BASE = "http://localhost:5000/api";


async function loginUser(username, password) {
  const res = await fetch(`${API_BASE}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  return res.json();
}

async function getProductos() {
  const res = await fetch(`${API_BASE}/producto`);
  return res.json();
}
async function getDistribuidores() {
  const res = await fetch(`${API_BASE}/distribuidor`);
  return res.json();
}
async function getMovimientos() {
  const res = await fetch(`${API_BASE}/movimiento`);
  return res.json();
}
// === API USUARIOS ===
async function getUsuarios() {
  const res = await fetch(`${API_BASE}/usuario/`);
  return res.json();
}

async function createUsuario(data) {
  const res = await fetch(`${API_BASE}/usuario/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

async function updateUsuario(id, data) {
  const res = await fetch(`${API_BASE}/usuario/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

async function deleteUsuario(id) {
  const res = await fetch(`${API_BASE}/usuario/${id}`, {
    method: "DELETE",
  });
  return res.json();
}
// === API ROLES ===
async function getRoles() {
  const res = await fetch(`${API_BASE}/rol/`);
  return res.json();
}

async function createRol(data) {
  const res = await fetch(`${API_BASE}/rol/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

async function updateRol(id, data) {
  const res = await fetch(`${API_BASE}/rol/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

async function deleteRol(id) {
  const res = await fetch(`${API_BASE}/rol/${id}`, {
    method: "DELETE",
  });
  return res.json();
}

// ===================================
// === API PERSONAS (NUEVO CÓDIGO) ===
// ===================================

async function getPersonas() {
  const res = await fetch(`${API_BASE}/persona/`);
  return res.json();
}

async function createPersona(data) {
  const res = await fetch(`${API_BASE}/persona/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

async function updatePersona(id, data) {
  const res = await fetch(`${API_BASE}/persona/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

async function deletePersona(id) {
  const res = await fetch(`${API_BASE}/persona/${id}`, {
    method: "DELETE",
  });
  return res.json();
}
// ======================================
// === API DISTRIBUIDORES (CRUD NUEVO) ===
// ======================================


async function createDistribuidor(data) {
  const res = await fetch(`${API_BASE}/distribuidor`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

async function updateDistribuidor(id, data) {
  const res = await fetch(`${API_BASE}/distribuidor/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

async function deleteDistribuidor(id) {
  const res = await fetch(`${API_BASE}/distribuidor/${id}`, {
    method: "DELETE",
  });
  return res.json();
}
// === PRODUCTOS ===


async function createProducto(data) {
  const res = await fetch(`${API_BASE}/producto/`, { // POST a /api/producto
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

async function updateProducto(id, data) {
  const res = await fetch(`${API_BASE}/producto/${id}`, { // PUT a /api/producto/<id>
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

async function deleteProducto(id) {
  const res = await fetch(`${API_BASE}/producto/${id}`, { // DELETE a /api/producto/<id>
    method: "DELETE",
  });
  return res.json();
}
