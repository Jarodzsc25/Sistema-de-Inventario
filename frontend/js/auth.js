// Asegúrate de que tu api.js está enlazado antes de auth.js en index.html y dashboard.html
// La función loginUser(username, password) debe estar definida en api.js.

// ===================================
// === LÓGICA DE LOGIN Y REDIRECCIÓN ===
// ===================================

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');

    // 1. Manejador de eventos para el formulario de Login (solo en index.html)
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // 2. Manejador de eventos para Logout (solo en dashboard.html)
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }

    // 3. Inicialización del Dashboard (Control de sesión y rol)
    // Se ejecuta al cargar dashboard.html para verificar la sesión.
    if (window.location.pathname.endsWith('dashboard.html')) {
        initializeDashboard();
    }
});


async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const errorMsg = document.getElementById('errorMsg');
    errorMsg.textContent = ''; // Limpiar mensajes de error previos

    try {
        // Asumiendo que loginUser existe en api.js
        const responseData = await loginUser(username, password);

        // Verifica si la API retornó un usuario válido Y EL TOKEN
        if (responseData && responseData.usuario && responseData.token) { // <--- MODIFICACIÓN CLAVE
            // Guarda el objeto completo del usuario.
            localStorage.setItem('user', JSON.stringify(responseData.usuario));

            // **CLAVE:** Guarda el token JWT para usarlo en futuras peticiones protegidas.
            localStorage.setItem('token', responseData.token); // <--- NUEVA LÍNEA

            // Redirigir al dashboard
            window.location.href = 'dashboard.html';

        } else {
            // Credenciales incorrectas o API devolvió error sin lanzar excepción
            errorMsg.textContent = 'Error: Credenciales inválidas. Intente de nuevo.';
        }

    } catch (error) {
        console.error('Error durante el login:', error);
        // Error de red, CORS, o API no encontrada (404/500)
        errorMsg.textContent = 'Error de conexión con el servidor. Verifique la API.';
    }
}

function handleLogout() {
    localStorage.removeItem('user');
    localStorage.removeItem('token'); // <--- ELIMINAR TAMBIÉN EL TOKEN
    window.location.href = 'index.html';
}

function initializeDashboard() {
    const userString = localStorage.getItem('user');

    if (userString) {
        const user = JSON.parse(userString);

        // 1. Mostrar nombre de usuario y rol en el navbar
        const userLabel = document.getElementById('userLabel');
        if (userLabel) {
            userLabel.textContent = `Usuario: ${user.username} (${user.rol_nombre || 'Sin Rol'})`;
        }

        // 2. Solución del problema de Rol: Mostrar/Ocultar menús de administrador
        const esAdministrador = user.rol_nombre === 'Administrador' || user.id_rol === 1;

        if (esAdministrador) {
          // Muestra los elementos que tienen la clase 'admin-only'
          document.querySelectorAll('.admin-only').forEach(el => {
            el.style.display = 'list-item'; // Mostrar como elemento de lista
          });
        }

    } else {
        // Si no hay sesión, redirigir al login
        window.location.href = 'index.html';
    }
}