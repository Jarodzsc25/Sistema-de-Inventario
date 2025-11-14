// === MÓDULO ADMINISTRADOR ===

// --- CRUD USUARIOS ---
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
        ${usuarios.map(u => `
          <tr>
            <td>${u.id_usuario}</td>
            <td>${u.username}</td>
            <td>${u.rol_nombre}</td>
            <td>
              <button class="btn btn-primary btn-sm btn-edit" data-id="${u.id_usuario}">Editar</button>
              <button class="btn btn-danger btn-sm btn-del" data-id="${u.id_usuario}">Eliminar</button>
            </td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  `;
  document.getElementById("contentArea").innerHTML = html;

  document.getElementById("btnNuevoUsuario").addEventListener("click", () =>
    mostrarFormularioUsuario(null, roles)
  );

  document.querySelectorAll(".btn-edit").forEach(btn =>
    btn.addEventListener("click", e => {
      const id = e.target.dataset.id;
      const user = usuarios.find(u => u.id_usuario == id);
      mostrarFormularioUsuario(user, roles);
    })
  );

  document.querySelectorAll(".btn-del").forEach(btn =>
    btn.addEventListener("click", async e => {
      const id = e.target.dataset.id;
      if (confirm("¿Seguro que deseas eliminar este usuario?")) {
        await deleteUsuario(id);
        alert("Usuario eliminado");
        document.getElementById("menuUsuarios").click();
      }
    })
  );
});

async function mostrarFormularioUsuario(usuario = null, roles) {
  const content = document.getElementById("contentArea");
  content.innerHTML = `
    <h4>${usuario ? "Editar Usuario" : "Nuevo Usuario"}</h4>
    <form id="formUsuario" class="mt-3">
      <div class="mb-3">
        <label>ID Persona (Debe existir en la BD)</label>
        <input type="number" class="form-control" id="idUsuario" value="${usuario?.id_usuario || ''}" ${usuario ? 'readonly' : ''} required>
      </div>
      <div class="mb-3">
        <label>Username</label>
        <input type="text" class="form-control" id="username" value="${usuario?.username || ''}" required>
      </div>
      <div class="mb-3">
        <label>Contraseña ${usuario ? "(dejar en blanco si no cambia)" : ""}</label>
        <input type="password" class="form-control" id="password">
      </div>
      <div class="mb-3">
        <label>Rol</label>
        <select class="form-select" id="idRol" required>
          <option value="">Seleccione un rol</option>
          ${roles.map(r => `<option value="${r.id_rol}" ${usuario?.rol_nombre === r.nombre ? "selected" : ""}>${r.nombre}</option>`).join('')}
        </select>
      </div>
      <button type="submit" class="btn btn-primary">${usuario ? "Guardar Cambios" : "Crear Usuario"}</button>
      <button type="button" class="btn btn-secondary" id="btnCancelar">Cancelar</button>
    </form>
  `;
  document.getElementById("btnCancelar").addEventListener("click", () => document.getElementById("menuUsuarios").click());

  document.getElementById("formUsuario").addEventListener("submit", async e => {
    e.preventDefault();
    const data = {
      id_usuario: parseInt(document.getElementById("idUsuario").value, 10),
      username: document.getElementById("username").value.trim(),
      password: document.getElementById("password").value.trim(),
      id_rol: parseInt(document.getElementById("idRol").value, 10)
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

// --- CRUD PERSONAS ---
document.getElementById("menuPersonas")?.addEventListener("click", async () => {
  const personas = await getPersonas();
  let html = `
    <div class="d-flex justify-content-between align-items-center">
      <h4>Gestión de Personas</h4>
      <button class="btn btn-success btn-sm" id="btnNuevaPersona">+ Nueva Persona</button>
    </div>
    <table class="table table-striped mt-3">
      <thead>
        <tr><th>ID</th><th>Nombre Completo</th><th>CI</th><th>Teléfono</th><th>Cliente</th><th>Acciones</th></tr>
      </thead>
      <tbody>
        ${personas.map(p => `
          <tr>
            <td>${p.id_persona}</td>
            <td>${p.nombre} ${p.primer_apellido || ''} ${p.segundo_apellido || ''}</td>
            <td>${p.numero_ci || ''}${p.complemento_ci || ''}</td>
            <td>${p.telefono || ''}</td>
            <td>${p.es_cliente ? 'Sí' : 'No'}</td>
            <td>
              <button class="btn btn-primary btn-sm btn-edit-persona" data-id="${p.id_persona}">Editar</button>
              <button class="btn btn-danger btn-sm btn-del-persona" data-id="${p.id_persona}">Eliminar</button>
            </td>
          </tr>`).join('')}
      </tbody>
    </table>
  `;
  document.getElementById("contentArea").innerHTML = html;

  document.getElementById("btnNuevaPersona").addEventListener("click", () => mostrarFormularioPersona(null));
  document.querySelectorAll(".btn-edit-persona").forEach(btn => btn.addEventListener("click", e => {
    const id = e.target.dataset.id;
    const persona = personas.find(p => p.id_persona == id);
    mostrarFormularioPersona(persona);
  }));
  document.querySelectorAll(".btn-del-persona").forEach(btn => btn.addEventListener("click", async e => {
    const id = e.target.dataset.id;
    if (confirm("¿Seguro que deseas eliminar esta persona?")) {
      await deletePersona(id);
      alert("Persona eliminada");
      document.getElementById("menuPersonas").click();
    }
  }));
});

async function mostrarFormularioPersona(persona = null) {
  const content = document.getElementById("contentArea");
  content.innerHTML = `
    <h4>${persona ? "Editar Persona" : "Nueva Persona"}</h4>
    <form id="formPersona" class="mt-3">
      <div class="row">
        <div class="col-md-4 mb-3"><label>Nombre(s)</label><input type="text" class="form-control" id="nombre" value="${persona?.nombre || ''}" required></div>
        <div class="col-md-4 mb-3"><label>Primer Apellido</label><input type="text" class="form-control" id="primer_apellido" value="${persona?.primer_apellido || ''}"></div>
        <div class="col-md-4 mb-3"><label>Segundo Apellido</label><input type="text" class="form-control" id="segundo_apellido" value="${persona?.segundo_apellido || ''}"></div>
      </div>
      <div class="row">
        <div class="col-md-8 mb-3"><label>Número CI</label><input type="number" class="form-control" id="numero_ci" value="${persona?.numero_ci || ''}"></div>
        <div class="col-md-4 mb-3"><label>Expedido</label><input type="text" maxlength="2" class="form-control" id="expedido" value="${persona?.expedido || ''}"></div>
      </div>
      <div class="row">
        <div class="col-md-6 mb-3"><label>Correo</label><input type="email" class="form-control" id="correo" value="${persona?.correo || ''}"></div>
        <div class="col-md-6 mb-3"><label>Teléfono</label><input type="text" class="form-control" id="telefono" value="${persona?.telefono || ''}"></div>
      </div>
      <div class="mb-3"><label>Dirección</label><textarea class="form-control" id="direccion">${persona?.direccion || ''}</textarea></div>
      <div class="form-check mb-3"><input type="checkbox" class="form-check-input" id="esCliente" ${persona?.es_cliente ? "checked" : ""}><label class="form-check-label">Es Cliente</label></div>
      <button type="submit" class="btn btn-primary">${persona ? "Guardar Cambios" : "Crear Persona"}</button>
      <button type="button" class="btn btn-secondary" id="btnCancelarPersona">Cancelar</button>
    </form>
  `;
  document.getElementById("btnCancelarPersona").addEventListener("click", () => document.getElementById("menuPersonas").click());
  document.getElementById("formPersona").addEventListener("submit", async e => {
    e.preventDefault();
    const data = {
      nombre: document.getElementById("nombre").value.trim(),
      primer_apellido: document.getElementById("primer_apellido").value.trim() || null,
      segundo_apellido: document.getElementById("segundo_apellido").value.trim() || null,
      numero_ci: document.getElementById("numero_ci").value ? parseInt(document.getElementById("numero_ci").value, 10) : null,
      complemento_ci: document.getElementById("expedido").value.trim() || null,
      correo: document.getElementById("correo").value.trim() || null,
      telefono: document.getElementById("telefono").value.trim() || null,
      direccion: document.getElementById("direccion").value.trim() || null,
      es_cliente: document.getElementById("esCliente").checked
    };
    if (persona) {
      await updatePersona(persona.id_persona, data);
      alert("Persona actualizada");
    } else {
      await createPersona(data);
      alert("Persona creada correctamente");
    }
    document.getElementById("menuPersonas").click();
  });
}

// --- CRUD DISTRIBUIDORES ---
document.getElementById("menuDistribuidores")?.addEventListener("click", async () => {
  const distribuidores = await getDistribuidores();
  let html = `
    <div class="d-flex justify-content-between align-items-center">
      <h4>Gestión de Distribuidores</h4>
      <button class="btn btn-success btn-sm" id="btnNuevoDistribuidor">+ Nuevo Distribuidor</button>
    </div>
    <table class="table table-striped mt-3">
      <thead><tr><th>ID</th><th>NIT</th><th>Nombre</th><th>Contacto</th><th>Teléfono</th><th>Dirección</th><th>Acciones</th></tr></thead>
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
          </tr>`).join('')}
      </tbody>
    </table>
  `;
  document.getElementById("contentArea").innerHTML = html;

  document.getElementById("btnNuevoDistribuidor").addEventListener("click", () => mostrarFormularioDistribuidor(null));
  document.querySelectorAll(".btn-edit-dist").forEach(btn => btn.addEventListener("click", e => {
    const id = e.target.dataset.id;
    const distribuidor = distribuidores.find(d => d.id_distribuidor == id);
    mostrarFormularioDistribuidor(distribuidor);
  }));
  document.querySelectorAll(".btn-del-dist").forEach(btn => btn.addEventListener("click", async e => {
    const id = e.target.dataset.id;
    if (confirm("¿Seguro que deseas eliminar este distribuidor?")) {
      await deleteDistribuidor(id);
      alert("Distribuidor eliminado");
      document.getElementById("menuDistribuidores").click();
    }
  }));
});

async function mostrarFormularioDistribuidor(distribuidor = null) {
  const content = document.getElementById("contentArea");
  content.innerHTML = `
    <h4>${distribuidor ? "Editar Distribuidor" : "Nuevo Distribuidor"}</h4>
    <form id="formDistribuidor" class="mt-3">
      <div class="row">
        <div class="col-md-4 mb-3"><label>NIT</label><input type="number" class="form-control" id="nitDist" value="${distribuidor?.nit || ''}" required></div>
        <div class="col-md-8 mb-3"><label>Nombre</label><input type="text" class="form-control" id="nombreDist" value="${distribuidor?.nombre || ''}" required></div>
      </div>
      <div class="row">
        <div class="col-md-6 mb-3"><label>Contacto</label><input type="text" class="form-control" id="contactoDist" value="${distribuidor?.contacto || ''}"></div>
        <div class="col-md-6 mb-3"><label>Teléfono</label><input type="text" class="form-control" id="telefonoDist" value="${distribuidor?.telefono || ''}"></div>
      </div>
      <div class="mb-3"><label>Dirección</label><input type="text" class="form-control" id="direccionDist" value="${distribuidor?.direccion || ''}"></div>
      <button type="submit" class="btn btn-primary">${distribuidor ? "Guardar Cambios" : "Crear Distribuidor"}</button>
      <button type="button" class="btn btn-secondary" id="btnCancelarDistribuidor">Cancelar</button>
    </form>
  `;
  document.getElementById("btnCancelarDistribuidor").addEventListener("click", () => document.getElementById("menuDistribuidores").click());
  document.getElementById("formDistribuidor").addEventListener("submit", async e => {
    e.preventDefault();
    const data = {
      nit: parseInt(document.getElementById("nitDist").value, 10),
      nombre: document.getElementById("nombreDist").value.trim(),
      contacto: document.getElementById("contactoDist").value.trim(),
      telefono: document.getElementById("telefonoDist").value.trim(),
      direccion: document.getElementById("direccionDist").value.trim()
    };
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

// --- CRUD PRODUCTOS ---
document.getElementById("menuProductos")?.addEventListener("click", async () => {
  const productos = await getProductos();
  const distribuidores = await getDistribuidores();

  let html = `
    <div class="d-flex justify-content-between align-items-center">
      <h4>Gestión de Productos</h4>
      <button class="btn btn-success btn-sm" id="btnNuevoProducto">+ Nuevo Producto</button>
    </div>
    <table class="table table-striped mt-3">
      <thead>
        <tr><th>ID</th><th>Código</th><th>Nombre</th><th>Descripción</th><th>Unidad</th><th>Distribuidor</th><th>Acciones</th></tr>
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
          </tr>`).join('')}
      </tbody>
    </table>
  `;
  document.getElementById("contentArea").innerHTML = html;

  document.getElementById("btnNuevoProducto").addEventListener("click", () => mostrarFormularioProducto(null, distribuidores));
  document.querySelectorAll(".btn-edit-prod").forEach(btn => btn.addEventListener("click", e => {
    const id = e.target.dataset.id;
    const producto = productos.find(p => p.id_producto == id);
    mostrarFormularioProducto(producto, distribuidores);
  }));
  document.querySelectorAll(".btn-del-prod").forEach(btn => btn.addEventListener("click", async e => {
    const id = e.target.dataset.id;
    if (confirm("¿Seguro que deseas eliminar este producto?")) {
      await deleteProducto(id);
      alert("Producto eliminado");
      document.getElementById("menuProductos").click();
    }
  }));
});

async function mostrarFormularioProducto(producto = null, distribuidores = []) {
  const content = document.getElementById("contentArea");
  content.innerHTML = `
    <h4>${producto ? "Editar Producto" : "Nuevo Producto"}</h4>
    <form id="formProducto" class="mt-3">
      <div class="mb-3"><label>Código</label><input type="text" class="form-control" id="codigoProd" value="${producto?.codigo || ''}" required></div>
      <div class="mb-3"><label>Nombre</label><input type="text" class="form-control" id="nombreProd" value="${producto?.nombre || ''}" required></div>
      <div class="mb-3"><label>Descripción</label><input type="text" class="form-control" id="descripcionProd" value="${producto?.descripcion || ''}"></div>
      <div class="mb-3"><label>Unidad</label><input type="text" class="form-control" id="unidadProd" value="${producto?.unidad || ''}"></div>
      <div class="mb-3">
        <label>Distribuidor</label>
        <select class="form-select" id="distribuidorProd" required>
          <option value="">Seleccione un distribuidor</option>
          ${distribuidores.map(d => `<option value="${d.id_distribuidor}" ${producto?.id_distribuidor === d.id_distribuidor ? "selected" : ""}>${d.nombre}</option>`).join('')}
        </select>
      </div>
      <button type="submit" class="btn btn-primary">${producto ? "Guardar Cambios" : "Crear Producto"}</button>
      <button type="button" class="btn btn-secondary" id="btnCancelarProducto">Cancelar</button>
    </form>
  `;
  document.getElementById("btnCancelarProducto").addEventListener("click", () => document.getElementById("menuProductos").click());
  document.getElementById("formProducto").addEventListener("submit", async e => {
    e.preventDefault();
    const data = {
      codigo: document.getElementById("codigoProd").value.trim(),
      nombre: document.getElementById("nombreProd").value.trim(),
      descripcion: document.getElementById("descripcionProd").value.trim(),
      unidad: document.getElementById("unidadProd").value.trim(),
      id_distribuidor: parseInt(document.getElementById("distribuidorProd").value, 10)
    };
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

// --------------------------------------------------------------------
// === NUEVAS FUNCIONALIDADES: MOVIMIENTOS (CRUD) Y KARDEX (REPORTE) ===
// --------------------------------------------------------------------

// ====================================================================
// === LÓGICA DE GESTIÓN DE MOVIMIENTOS (CRUD) ===
// ====================================================================

/**
 * Manejador de clic en el menú "Movimientos" e Inicializa la vista de lista de movimientos.
 */
document.getElementById("menuMovimientos")?.addEventListener("click", async () => {
    renderMovimientoList();
});

/**
 * Renderiza la lista de movimientos con botones de CRUD.
 */
async function renderMovimientoList() {
    document.getElementById("contentArea").innerHTML = '<h4>Cargando Movimientos...</h4>';
    try {
        const movimientos = await getMovimientos();

        const html = `
            <h4>Gestión de Movimientos</h4>
            <button id="btnCrearMovimiento" class="btn btn-success mb-3">Crear Nuevo Movimiento</button>
            <table class="table table-bordered table-striped">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Tipo</th>
                  <th>Producto</th>
                  <th>Cantidad</th>
                  <th>Fecha</th>
                  <th>Glosa</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                ${movimientos
                  .map(
                    (m) =>
                      `<tr>
                        <td>${m.id_movimiento}</td>
                        <td class="${m.tipo === 'ENTRADA' ? 'text-success' : 'text-danger'}">${m.tipo}</td>
                        <td>${m.producto_nombre || 'N/A'}</td>
                        <td>${m.cantidad}</td>
                        <td>${new Date(m.fecha).toLocaleDateString()}</td>
                        <td>${m.glosa || ''}</td>
                        <td>
                          <button class="btn btn-sm btn-info btn-edit-mov" data-id="${m.id_movimiento}">Editar</button>
                          <button class="btn btn-sm btn-danger btn-delete-mov" data-id="${m.id_movimiento}">Eliminar</button>
                        </td>
                      </tr>`
                  )
                  .join("")}
              </tbody>
            </table>`;

        document.getElementById("contentArea").innerHTML = html;

        // --- Eventos de Botones de CRUD ---
        document.getElementById("btnCrearMovimiento").addEventListener("click", () => renderMovimientoForm());

        document.querySelectorAll(".btn-edit-mov").forEach(button => {
            button.addEventListener("click", async (e) => {
                const id = e.target.getAttribute("data-id");
                const movimiento = await getMovimiento(id);
                renderMovimientoForm(movimiento);
            });
        });

        document.querySelectorAll(".btn-delete-mov").forEach(button => {
            button.addEventListener("click", async (e) => {
                const id = e.target.getAttribute("data-id");
                if (confirm(`¿Seguro que deseas eliminar el movimiento ID ${id}? (Esta acción puede afectar el inventario)`)) {
                    await deleteMovimiento(id);
                    alert("Movimiento eliminado con éxito.");
                    renderMovimientoList();
                }
            });
        });

    } catch (error) {
        console.error("Error al cargar movimientos:", error);
        document.getElementById("contentArea").innerHTML = `<div class="alert alert-danger">Error al cargar movimientos: ${error.message}</div>`;
    }
}

/**
 * Renderiza el formulario de creación o edición de Movimiento.
 * @param {object} movimiento - Objeto movimiento si es edición, null si es creación.
 */
async function renderMovimientoForm(movimiento = null) {
    const isEdit = movimiento !== null;
    const title = isEdit ? `Editar Movimiento #${movimiento.id_movimiento}` : "➕ Crear Nuevo Movimiento";

    const htmlForm = `
        <h4>${title}</h4>
        <form id="movimientoForm">
            <input type="hidden" id="movimientoId" value="${isEdit ? movimiento.id_movimiento : ''}">

            <div class="mb-3">
                <label for="tipoMovimiento" class="form-label">Tipo de Movimiento</label>
                <select class="form-select" id="tipoMovimiento" required>
                    <option value="">Seleccione...</option>
                    <option value="ENTRADA" ${isEdit && movimiento.tipo === 'ENTRADA' ? 'selected' : ''}>ENTRADA</option>
                    <option value="SALIDA" ${isEdit && movimiento.tipo === 'SALIDA' ? 'selected' : ''}>SALIDA</option>
                </select>
            </div>

            <div class="mb-3">
                <label for="idProducto" class="form-label">Producto (ID)</label>
                <input type="number" class="form-control" id="idProducto" required min="1"
                       value="${isEdit ? movimiento.id_producto : ''}">
            </div>

            <div class="mb-3">
                <label for="cantidad" class="form-label">Cantidad</label>
                <input type="number" class="form-control" id="cantidad" required min="1"
                       value="${isEdit ? movimiento.cantidad : ''}">
            </div>

            <div class="mb-3">
                <label for="glosa" class="form-label">Glosa/Descripción</label>
                <input type="text" class="form-control" id="glosa" required
                       value="${isEdit ? movimiento.glosa : ''}">
            </div>

            <button type="submit" class="btn btn-primary">${isEdit ? 'Guardar Cambios' : 'Crear Movimiento'}</button>
            <button type="button" class="btn btn-secondary" onclick="renderMovimientoList()">Cancelar</button>
        </form>`;

    document.getElementById("contentArea").innerHTML = htmlForm;

    // --- Lógica de envío del Formulario ---
    document.getElementById("movimientoForm").addEventListener("submit", async (e) => {
        e.preventDefault();

        const id = document.getElementById("movimientoId").value;
        const data = {
            // Nota: Tu DB usa CHAR(1). Tu backend debe mapear 'ENTRADA' a 'C'/'E' y 'SALIDA' a 'V'/'S'
            tipo: document.getElementById("tipoMovimiento").value,
            id_producto: parseInt(document.getElementById("idProducto").value),
            cantidad: parseInt(document.getElementById("cantidad").value),
            glosa: document.getElementById("glosa").value,
        };

        try {
            if (id) {
                await updateMovimiento(id, data);
                alert("Movimiento actualizado correctamente.");
            } else {
                await createMovimiento(data);
                alert("Movimiento creado correctamente.");
            }
            renderMovimientoList(); // Volver a la lista
        } catch (error) {
            console.error("Error al guardar movimiento:", error);
            alert(`Error al guardar el movimiento. Revisa la consola o los datos ingresados: ${error.message}`);
        }
    });
}


// ====================================================================
// === LÓGICA DE VISUALIZACIÓN DE KARDEX (REPORTE/READ) - CONSOLIDADA ===
// ====================================================================

/**
 * Manejador de clic en el menú "Kardex" y Renderiza el reporte.
 * NOTA: Usa getKardex() de api.js
 */
document.getElementById("menuKardex")?.addEventListener("click", renderKardexReporte);


async function renderKardexReporte() {
    const content = document.getElementById("contentArea");
    content.innerHTML = `<h4>Reporte de Kardex</h4><div id="kardexTableContainer">Cargando reporte...</div>`;

    try {
        // Usar getKardex() (singular) de api.js
        const kardex = await getKardex();

        const html = `
            <p class="text-info">El reporte de Kardex muestra todos los movimientos de inventario por producto.</p>
            <table class="table table-bordered table-striped table-sm">
                <thead>
                    <tr>
                        <th>ID Mov.</th>
                        <th>Fecha</th>
                        <th>Producto</th>
                        <th>Glosa</th>
                        <th>Tipo</th>
                        <th class="text-success">ENTRADA</th>
                        <th class="text-danger">SALIDA</th>
                        <th>Saldo Final</th>
                        <th>Subtotal</th>
                    </tr>
                </thead>
                <tbody>
                    ${kardex
                        .map(
                            (k) =>
                                `<tr>
                                    <td>${k.id_movimiento}</td>
                                    <td>${new Date(k.fecha).toLocaleDateString()}</td>
                                    <td>${k.producto_nombre}</td>
                                    <td>${k.glosa}</td>
                                    <td>${k.tipo_movimiento}</td>
                                    <td class="text-success">${k.cantidad_entrada !== null ? k.cantidad_entrada : ''}</td>
                                    <td class="text-danger">${k.cantidad_salida !== null ? k.cantidad_salida : ''}</td>
                                    <td>${k.saldo_final !== null ? k.saldo_final : 'N/A'}</td>
                                    <td>${k.subtotal}</td>
                                </tr>`
                        )
                        .join("")}
                </tbody>
            </table>
        `;
        document.getElementById("kardexTableContainer").innerHTML = html;

    } catch (error) {
        console.error("Error al cargar Kardex:", error);
        // Mostrar un mensaje de error más útil, incluyendo el mensaje de la excepción de la API
        document.getElementById("kardexTableContainer").innerHTML = `<div class="alert alert-danger">Error al cargar el reporte de Kardex: ${error.message || 'Verifica el servidor o la consola para detalles.'}</div>`;
    }
}