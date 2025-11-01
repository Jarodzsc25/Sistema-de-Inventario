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
      <fieldset>
        <legend class="h6">Datos de Usuario</legend>

        <div class="mb-3">
          <label class="form-label">ID Persona (¡Debe existir en la BD!)</label>
          <input type="number" class="form-control" id="idUsuario" placeholder="Ingrese el ID de la persona existente" value="${
            usuario?.id_usuario || ""
          }" required ${usuario ? 'readonly' : ''}>
        </div>

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
      </fieldset>

      <button type="submit" class="btn btn-primary mt-3">${
        usuario ? "Guardar Cambios" : "Crear Usuario"
      }</button>
      <button type="button" class="btn btn-secondary mt-3" id="btnCancelar">Cancelar</button>
    </form>
  `;
  document.getElementById("btnCancelar").addEventListener("click", () => {
    document.getElementById("menuUsuarios").click();
  });

  document.getElementById("formUsuario").addEventListener("submit", async (e) => {
    e.preventDefault();

    // Recolección de datos que coincide con tu API de Postman
    const data = {
      // Usamos idUsuario en el HTML, pero el backend lo espera como id_usuario
      id_usuario: document.getElementById("idUsuario").value,
      username: document.getElementById("username").value.trim(),
      password: document.getElementById("password").value.trim(),
      id_rol: document.getElementById("idRol").value
    };

    // La API de creación de usuario (POST) en tu backend espera estos 4 campos.

    if (usuario) {
      // Para editar, pasamos el ID de usuario y los datos
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
// =====================================
// === GESTIÓN DE DISTRIBUIDORES (CRUD) ===
// =====================================

document.getElementById("menuDistribuidores")?.addEventListener("click", async () => {
  const distribuidores = await getDistribuidores();

  let html = `
    <div class="d-flex justify-content-between align-items-center">
      <h4>Gestión de Distribuidores</h4>
      <button class="btn btn-success btn-sm" id="btnNuevoDistribuidor">+ Nuevo Distribuidor</button>
    </div>

    <table class="table table-striped mt-3">
      <thead>
        <tr>
          <th>ID</th>
          <th>NIT</th>
          <th>Nombre</th>
          <th>Contacto</th>
          <th>Teléfono</th>
          <th>Dirección</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        ${distribuidores.map(d => `
          <tr>
            <td>${d.id_distribuidor}</td>
            <td>${d.nit || ''}</td>
            <td>${d.nombre || ''}</td>
            <td>${d.contacto || ''}</td>
            <td>${d.telefono || ''}</td>
            <td>${d.direccion || ''}</td>
            <td>
              <button class="btn btn-primary btn-sm btn-edit-dist" data-id="${d.id_distribuidor}">Editar</button>
              <button class="btn btn-danger btn-sm btn-del-dist" data-id="${d.id_distribuidor}">Eliminar</button>
            </td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;

  document.getElementById("contentArea").innerHTML = html;

  // NUEVO DISTRIBUIDOR
  document.getElementById("btnNuevoDistribuidor").addEventListener("click", () =>
    mostrarFormularioDistribuidor(null)
  );

  // EDITAR DISTRIBUIDOR
  document.querySelectorAll(".btn-edit-dist").forEach(btn =>
    btn.addEventListener("click", (e) => {
      const id = e.target.dataset.id;
      const distribuidor = distribuidores.find(d => d.id_distribuidor == id);
      mostrarFormularioDistribuidor(distribuidor);
    })
  );

  // ELIMINAR DISTRIBUIDOR
  document.querySelectorAll(".btn-del-dist").forEach(btn =>
    btn.addEventListener("click", async (e) => {
      const id = e.target.dataset.id;
      if (confirm("¿Seguro que deseas eliminar este distribuidor?")) {
        await deleteDistribuidor(id);
        alert("Distribuidor eliminado");
        document.getElementById("menuDistribuidores").click();
      }
    })
  );
});

// === Formulario para crear o editar distribuidor ===
async function mostrarFormularioDistribuidor(distribuidor = null) {
  const content = document.getElementById("contentArea");
  content.innerHTML = `
    <h4>${distribuidor ? "Editar Distribuidor" : "Nuevo Distribuidor"}</h4>
    <form id="formDistribuidor" class="mt-3">
      <div class="row">
        <div class="col-md-4 mb-3">
          <label class="form-label">NIT</label>
          <input type="number" class="form-control" id="nitDist" value="${distribuidor?.nit || ""}" required>
        </div>
        <div class="col-md-8 mb-3">
          <label class="form-label">Nombre</label>
          <input type="text" class="form-control" id="nombreDist" value="${distribuidor?.nombre || ""}" required>
        </div>
      </div>

      <div class="row">
        <div class="col-md-6 mb-3">
          <label class="form-label">Contacto</label>
          <input type="text" class="form-control" id="contactoDist" value="${distribuidor?.contacto || ""}">
        </div>
        <div class="col-md-6 mb-3">
          <label class="form-label">Teléfono</label>
          <input type="text" class="form-control" id="telefonoDist" value="${distribuidor?.telefono || ""}">
        </div>
      </div>

      <div class="mb-3">
        <label class="form-label">Dirección</label>
        <input type="text" class="form-control" id="direccionDist" value="${distribuidor?.direccion || ""}">
      </div>

      <button type="submit" class="btn btn-primary">${distribuidor ? "Guardar Cambios" : "Crear Distribuidor"}</button>
      <button type="button" class="btn btn-secondary" id="btnCancelarDistribuidor">Cancelar</button>
    </form>
  `;

  document.getElementById("btnCancelarDistribuidor").addEventListener("click", () => {
    document.getElementById("menuDistribuidores").click();
  });

  document.getElementById("formDistribuidor").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
      nit: parseInt(document.getElementById("nitDist").value, 10),
      nombre: document.getElementById("nombreDist").value.trim(),
      contacto: document.getElementById("contactoDist").value.trim(),
      telefono: document.getElementById("telefonoDist").value.trim(),
      direccion: document.getElementById("direccionDist").value.trim(),
    };

    if (!data.nit || !data.nombre) {
      alert("El NIT y el nombre son obligatorios");
      return;
    }

    if (distribuidor) {
      await updateDistribuidor(distribuidor.id_distribuidor, data);
      alert("Distribuidor actualizado correctamente");
    } else {
      await createDistribuidor(data);
      alert("Distribuidor creado correctamente");
    }

    document.getElementById("menuDistribuidores").click();
  });
}
// =====================================
// === GESTIÓN DE PRODUCTOS (CRUD) ===
// =====================================

document.getElementById("menuProductos")?.addEventListener("click", async () => {
  const productos = await getProductos();
  const distribuidores = await getDistribuidores(); // Para seleccionar distribuidor al crear/editar

  let html = `
    <div class="d-flex justify-content-between align-items-center">
      <h4>Gestión de Productos</h4>
      <button class="btn btn-success btn-sm" id="btnNuevoProducto">+ Nuevo Producto</button>
    </div>

    <table class="table table-striped mt-3">
      <thead>
        <tr>
          <th>ID</th>
          <th>Código</th>
          <th>Nombre</th>
          <th>Descripción</th>
          <th>Unidad</th>
          <th>Distribuidor</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        ${productos.map(p => `
          <tr>
            <td>${p.id_producto}</td>
            <td>${p.codigo || ''}</td>
            <td>${p.nombre || ''}</td>
            <td>${p.descripcion || ''}</td>
            <td>${p.unidad || ''}</td>
            <td>${p.distribuidor_nombre || ''}</td>
            <td>
              <button class="btn btn-primary btn-sm btn-edit-prod" data-id="${p.id_producto}">Editar</button>
              <button class="btn btn-danger btn-sm btn-del-prod" data-id="${p.id_producto}">Eliminar</button>
            </td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;

  document.getElementById("contentArea").innerHTML = html;

  // NUEVO PRODUCTO
  document.getElementById("btnNuevoProducto").addEventListener("click", () =>
    mostrarFormularioProducto(null, distribuidores)
  );

  // EDITAR PRODUCTO
  document.querySelectorAll(".btn-edit-prod").forEach(btn =>
    btn.addEventListener("click", (e) => {
      const id = e.target.dataset.id;
      const producto = productos.find(p => p.id_producto == id);
      mostrarFormularioProducto(producto, distribuidores);
    })
  );

  // ELIMINAR PRODUCTO
  document.querySelectorAll(".btn-del-prod").forEach(btn =>
    btn.addEventListener("click", async (e) => {
      const id = e.target.dataset.id;
      if (confirm("¿Seguro que deseas eliminar este producto?")) {
        await deleteProducto(id);
        alert("Producto eliminado");
        document.getElementById("menuProductos").click();
      }
    })
  );
});

// === Formulario para crear o editar producto ===
async function mostrarFormularioProducto(producto = null, distribuidores = []) {
  const content = document.getElementById("contentArea");
  content.innerHTML = `
    <h4>${producto ? "Editar Producto" : "Nuevo Producto"}</h4>
    <form id="formProducto" class="mt-3">
      <div class="mb-3">
        <label class="form-label">Código</label>
        <input type="text" class="form-control" id="codigoProd" value="${producto?.codigo || ""}" required>
      </div>
      <div class="mb-3">
        <label class="form-label">Nombre</label>
        <input type="text" class="form-control" id="nombreProd" value="${producto?.nombre || ""}" required>
      </div>
      <div class="mb-3">
        <label class="form-label">Descripción</label>
        <input type="text" class="form-control" id="descripcionProd" value="${producto?.descripcion || ""}">
      </div>
      <div class="mb-3">
        <label class="form-label">Unidad</label>
        <input type="text" class="form-control" id="unidadProd" value="${producto?.unidad || ""}">
      </div>
      <div class="mb-3">
        <label class="form-label">Distribuidor</label>
        <select class="form-select" id="distribuidorProd" required>
          <option value="">Seleccione un distribuidor</option>
          ${distribuidores.map(d => `
            <option value="${d.id_distribuidor}" ${producto?.id_distribuidor === d.id_distribuidor ? "selected" : ""}>${d.nombre}</option>
          `).join("")}
        </select>
      </div>

      <button type="submit" class="btn btn-primary">${producto ? "Guardar Cambios" : "Crear Producto"}</button>
      <button type="button" class="btn btn-secondary" id="btnCancelarProducto">Cancelar</button>
    </form>
  `;

  document.getElementById("btnCancelarProducto").addEventListener("click", () => {
    document.getElementById("menuProductos").click();
  });

  document.getElementById("formProducto").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
      codigo: document.getElementById("codigoProd").value.trim(),
      nombre: document.getElementById("nombreProd").value.trim(),
      descripcion: document.getElementById("descripcionProd").value.trim(),
      unidad: document.getElementById("unidadProd").value.trim(),
      id_distribuidor: parseInt(document.getElementById("distribuidorProd").value, 10),
    };

    if (!data.codigo || !data.nombre || !data.id_distribuidor) {
      alert("Código, Nombre y Distribuidor son obligatorios");
      return;
    }

    if (producto) {
      await updateProducto(producto.id_producto, data);
      alert("Producto actualizado correctamente");
    } else {
      await createProducto(data);
      alert("Producto creado correctamente");
    }

    document.getElementById("menuProductos").click();
  });
}
