// === MÓDULO ADMINISTRADOR ===

// Mostrar lista de usuarios
document.getElementById("menuUsuarios")?.addEventListener("click", async () => {
  const usuarios = await getUsuarios();
  const roles = await getRoles();

  let html = `
    <div class="d-flex justify-content-between align-items-center">
      <h4>Gestión de Usuarios</h4>
      <button class="btn btn-success btn-sm" id="btnNuevoUsuario">+ Nuevo Usuario</button>
    </div>
    <table class="table table-striped mt-3">
      <thead><tr><th>ID</th><th>Usuario</th><th>Rol</th><th>Acciones</th></tr></thead>
      <tbody>
        ${usuarios
          .map(
            (u) => `
          <tr>
            <td>${u.id_usuario}</td>
            <td>${u.username}</td>
            <td>${u.rol_nombre}</td>
            <td>
              <button class="btn btn-primary btn-sm btn-edit" data-id="${u.id_usuario}">Editar</button>
              <button class="btn btn-danger btn-sm btn-del" data-id="${u.id_usuario}">Eliminar</button>
            </td>
          </tr>`
          )
          .join("")}
      </tbody>
    </table>
  `;
  document.getElementById("contentArea").innerHTML = html;

  // Nuevo usuario
  document.getElementById("btnNuevoUsuario").addEventListener("click", () =>
    mostrarFormularioUsuario(null, roles)
  );
  // Botones editar y eliminar
  document.querySelectorAll(".btn-edit").forEach((btn) =>
    btn.addEventListener("click", async (e) => {
      const id = e.target.dataset.id;
      const user = usuarios.find((u) => u.id_usuario == id);
      mostrarFormularioUsuario(user, roles);
    })
  );
  document.querySelectorAll(".btn-del").forEach((btn) =>
    btn.addEventListener("click", async (e) => {
      const id = e.target.dataset.id;
      if (confirm("¿Seguro que deseas eliminar este usuario?")) {
        await deleteUsuario(id);
        alert("Usuario eliminado");
        document.getElementById("menuUsuarios").click();
      }
    })
  );
});

// Mostrar formulario Usuario (nuevo o editar)
async function mostrarFormularioUsuario(usuario = null, roles) {
  const content = document.getElementById("contentArea");
  content.innerHTML = `
    <h4>${usuario ? "Editar Usuario" : "Nuevo Usuario"}</h4>
    <form id="formUsuario" class="mt-3">
      <div class="mb-3">
        <label class="form-label">Username</label>
        <input type="text" class="form-control" id="username" value="${
          usuario?.username || ""
        }" required>
      </div>
      <div class="mb-3">
        <label class="form-label">Contraseña ${
          usuario ? "(dejar en blanco si no cambia)" : ""
        }</label>
        <input type="password" class="form-control" id="password">
      </div>
      <div class="mb-3">
        <label class="form-label">Rol</label>
        <select class="form-select" id="idRol" required>
          <option value="">Seleccione un rol</option>
          ${roles
            .map(
              (r) =>
                `<option value="${r.id_rol}" ${
                  usuario?.rol_nombre === r.nombre ? "selected" : ""
                }>${r.nombre}</option>`
            )
            .join("")}
        </select>
      </div>
      <div class="mb-3">
        <label class="form-label">ID Persona</label>
        <input type="number" class="form-control" id="idPersona" placeholder="Ingrese ID de persona existente" value="${
          usuario?.id_usuario || ""
        }" required>
      </div>
      <button type="submit" class="btn btn-primary">${
        usuario ? "Guardar Cambios" : "Crear Usuario"
      }</button>
      <button type="button" class="btn btn-secondary" id="btnCancelar">Cancelar</button>
    </form>
  `;
  document.getElementById("btnCancelar").addEventListener("click", () => {
    document.getElementById("menuUsuarios").click();
  });
  document.getElementById("formUsuario").addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = {
      username: document.getElementById("username").value.trim(),
      password: document.getElementById("password").value.trim(),
      id_rol: document.getElementById("idRol").value,
      id_persona: document.getElementById("idPersona").value,
    };

    if (usuario) {
      await updateUsuario(usuario.id_usuario, data);
      alert("Usuario actualizado");
    } else {
      await createUsuario(data);
      alert("Usuario creado correctamente");
    }

    document.getElementById("menuUsuarios").click();
  });
}


// =====================================
// === GESTIÓN DE PERSONAS (CORREGIDO) ===
// =====================================

// Mostrar lista de personas
document.getElementById("menuPersonas")?.addEventListener("click", async () => {
  const personas = await getPersonas();

  let html = `
    <div class="d-flex justify-content-between align-items-center">
      <h4>Gestión de Personas</h4>
      <button class="btn btn-success btn-sm" id="btnNuevaPersona">+ Nueva Persona</button>
    </div>
    <table class="table table-striped mt-3">
      <thead><tr><th>ID</th><th>Nombre Completo</th><th>CI</th><th>Teléfono</th><th>Acciones</th></tr></thead>
      <tbody>
        ${personas
          .map(
            (p) => `
          <tr>
            <td>${p.id_persona}</td>
            <td>${p.nombre} ${p.primer_apellido || ''} ${p.segundo_apellido || ''}</td>
            <td>${p.numero_ci || ''}${p.complemento_ci || ''}</td>
            <td>${p.telefono || ''}</td>
            <td>
              <button class="btn btn-primary btn-sm btn-edit-persona" data-id="${p.id_persona}">Editar</button>
              <button class="btn btn-danger btn-sm btn-del-persona" data-id="${p.id_persona}">Eliminar</button>
            </td>
          </tr>`
          )
          .join("")}
      </tbody>
    </table>
  `;
  document.getElementById("contentArea").innerHTML = html;

  // NUEVA PERSONA
  document.getElementById("btnNuevaPersona").addEventListener("click", () =>
    mostrarFormularioPersona(null)
  );

  // EDITAR PERSONA
  document.querySelectorAll(".btn-edit-persona").forEach((btn) =>
    btn.addEventListener("click", (e) => {
      const id = e.target.dataset.id;
      const persona = personas.find((p) => p.id_persona == id);
      mostrarFormularioPersona(persona);
    })
  );

  // ELIMINAR PERSONA
  document.querySelectorAll(".btn-del-persona").forEach((btn) =>
    btn.addEventListener("click", async (e) => {
      const id = e.target.dataset.id;
      if (confirm("¿Seguro que deseas eliminar esta persona?")) {
        await deletePersona(id);
        alert("Persona eliminada");
        document.getElementById("menuPersonas").click();
      }
    })
  );
});

// Mostrar formulario Persona (nuevo o editar) - BASADO EN TU DB SCHEMA
async function mostrarFormularioPersona(persona = null) {
  const content = document.getElementById("contentArea");
  content.innerHTML = `
    <h4>${persona ? "Editar Persona" : "Nueva Persona"}</h4>
    <form id="formPersona" class="mt-3">
      <div class="row">
        <div class="col-md-4 mb-3">
          <label class="form-label">Nombre(s)</label>
          <input type="text" class="form-control" id="nombre" value="${
            persona?.nombre || ""
          }" required>
        </div>
        <div class="col-md-4 mb-3">
          <label class="form-label">Primer Apellido</label>
          <input type="text" class="form-control" id="primer_apellido" value="${
            persona?.primer_apellido || ""
          }">
        </div>
        <div class="col-md-4 mb-3">
          <label class="form-label">Segundo Apellido</label>
          <input type="text" class="form-control" id="segundo_apellido" value="${
            persona?.segundo_apellido || ""
          }">
        </div>
      </div>

      <div class="row">
        <div class="col-md-8 mb-3">
          <label class="form-label">Número CI</label>
          <input type="number" class="form-control" id="numero_ci" value="${
            persona?.numero_ci || ""
          }">
        </div>
        <div class="col-md-4 mb-3">
          <label class="form-label">Complemento CI (Máx. 2 caracteres)</label>
          <input type="text" class="form-control" id="complemento_ci" maxlength="2" value="${
            persona?.complemento_ci || ""
          }">
        </div>
      </div>

      <div class="row">
        <div class="col-md-6 mb-3">
          <label class="form-label">Correo Electrónico (UNIQUE)</label>
          <input type="email" class="form-control" id="correo" value="${
            persona?.correo || ""
          }">
        </div>
        <div class="col-md-6 mb-3">
          <label class="form-label">Teléfono</label>
          <input type="text" class="form-control" id="telefono" value="${
            persona?.telefono || ""
          }">
        </div>
      </div>

      <div class="mb-3">
        <label class="form-label">Dirección</label>
        <textarea class="form-control" id="direccion">${
          persona?.direccion || ""
        }</textarea>
      </div>

      <button type="submit" class="btn btn-primary">${
        persona ? "Guardar Cambios" : "Crear Persona"
      }</button>
      <button type="button" class="btn btn-secondary" id="btnCancelarPersona">Cancelar</button>
    </form>
  `;

  document.getElementById("btnCancelarPersona").addEventListener("click", () => {
    document.getElementById("menuPersonas").click();
  });

  document.getElementById("formPersona").addEventListener("submit", async (e) => {
    e.preventDefault();

    // Extracción de datos según la nueva estructura de la DB
    const data = {
      nombre: document.getElementById("nombre").value.trim(),
      primer_apellido: document.getElementById("primer_apellido").value.trim() || null,
      segundo_apellido: document.getElementById("segundo_apellido").value.trim() || null,
      // Los campos numéricos se convierten a null si están vacíos, y a INT si tienen valor.
      numero_ci: document.getElementById("numero_ci").value ? parseInt(document.getElementById("numero_ci").value, 10) : null,
      complemento_ci: document.getElementById("complemento_ci").value.trim() || null,
      correo: document.getElementById("correo").value.trim() || null,
      telefono: document.getElementById("telefono").value.trim() || null,
      direccion: document.getElementById("direccion").value.trim() || null,
    };

    // Validación básica: Nombre es NOT NULL en la DB
    if (!data.nombre) {
        alert("El campo Nombre es obligatorio.");
        return;
    }

    // Manejo de la API (updatePersona y createPersona)
    if (persona) {
      await updatePersona(persona.id_persona, data);
      alert("Persona actualizada");
    } else {
      await createPersona(data);
      alert("Persona creada correctamente");
    }

    document.getElementById("menuPersonas").click(); // Recargar la lista
  });
}