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
        // Llama a loginUser en api.js. Si falla (401), lanzará un error.
        const responseData = await loginUser(username, password);

        // Si llega aquí, la petición fue 200 OK (Manejo de éxito)
        if (responseData && responseData.usuario && responseData.token) {

            // Guarda el objeto completo del usuario y el token
            localStorage.setItem('user', JSON.stringify(responseData.usuario));
            localStorage.setItem('token', responseData.token);

            // Redirigir al dashboard
            window.location.href = 'dashboard.html';

        } else {
            // Este caso es muy improbable si api.js lanza errores correctamente,
            // pero lo dejamos como fallback.
            errorMsg.textContent = 'Error: Respuesta inesperada del servidor. Intente de nuevo.';
        }

    } catch (error) {
        // === 🛑 CORRECCIÓN CLAVE AQUÍ 🛑 ===

        console.error('Error durante el login:', error);

        // Verifica si el mensaje de error incluye el código 401
        if (error.message.includes('401')) {
            // Error específico de autenticación fallida (credenciales incorrectas)
            errorMsg.textContent = 'Credenciales inválidas. Verifique su usuario y contraseña.';
        } else {
            // Error de red, CORS, o API no encontrada (404/500), etc.
            errorMsg.textContent = 'Error de conexión con el servidor. Verifique que la API esté activa.';
        }
    }
}

function handleLogout() {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
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