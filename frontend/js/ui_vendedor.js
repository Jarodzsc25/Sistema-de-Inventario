// === MÓDULO VENDEDOR ===

// --- LECTURA DE PRODUCTOS ---
document.getElementById("menuProductos")?.addEventListener("click", async () => {
  try {
    const productos = await getProductos();
    const html = `
      <h4>Lista de Productos</h4>
      <table class="table table-bordered">
        <thead><tr><th>ID</th><th>Nombre</th><th>Distribuidor</th></tr></thead>
        <tbody>${productos
          .map(
            (p) =>
              `<tr><td>${p.id_producto}</td><td>${p.nombre}</td><td>${p.distribuidor_nombre}</td></tr>`
          )
          .join("")}</tbody>
      </table>`;
    document.getElementById("contentArea").innerHTML = html;
  } catch (error) {
    document.getElementById("contentArea").innerHTML = `<div class="alert alert-danger">Error al cargar productos: ${error.message}</div>`;
  }
});

// --- MOVIMIENTOS: LISTAR Y CREAR ---

/**
 * Muestra la lista de movimientos y el botón para crear uno nuevo.
 */
document.getElementById("menuMovimientos")?.addEventListener("click", async () => {
    try {
        const movs = await getMovimientos();
        const html = `
            <div class="d-flex justify-content-between align-items-center">
                <h4>Lista de Movimientos</h4>
                <button class="btn btn-success btn-sm" id="btnNuevoMovimiento">+ Nuevo Movimiento</button>
            </div>
            <table class="table table-striped mt-3">
                <thead><tr><th>ID</th><th>Tipo</th><th>Fecha</th><th>Glosa</th></tr></thead>
                <tbody>${movs
                    .map(
                        (m) =>
                            `<tr>
                                <td>${m.id_movimiento}</td>
                                <td class="${m.tipo === 'ENTRADA' ? 'text-success' : 'text-danger'}">${m.tipo}</td>
                                <td>${new Date(m.fecha).toLocaleDateString()}</td>
                                <td>${m.glosa}</td>
                            </tr>`
                    )
                    .join("")}</tbody>
            </table>`;
        document.getElementById("contentArea").innerHTML = html;

        // Añadir el manejador del botón de crear
        document.getElementById("btnNuevoMovimiento").addEventListener("click", renderVendedorMovimientoForm);
    } catch (error) {
        document.getElementById("contentArea").innerHTML = `<div class="alert alert-danger">Error al cargar movimientos: ${error.message}</div>`;
    }
});

/**
 * Renderiza el formulario simplificado para que el vendedor cree un Movimiento.
 * Solo permite crear (POST).
 */
async function renderVendedorMovimientoForm() {
    const content = document.getElementById("contentArea");
    content.innerHTML = `
        <h4>➕ Registrar Movimiento de Inventario</h4>
        <form id="vendedorMovimientoForm" class="mt-3">

            <div class="mb-3">
                <label for="tipoMovimiento" class="form-label">Tipo de Movimiento</label>
                <select class="form-select" id="tipoMovimiento" required>
                    <option value="">Seleccione...</option>
                    <option value="SALIDA">SALIDA (Venta/Consumo)</option>
                    <option value="ENTRADA">ENTRADA (Reposición)</option>
                </select>
            </div>

            <div class="mb-3">
                <label for="idProducto" class="form-label">Producto (ID)</label>
                <input type="number" class="form-control" id="idProducto" required min="1" placeholder="Ingrese el ID del producto">
            </div>

            <div class="mb-3">
                <label for="cantidad" class="form-label">Cantidad</label>
                <input type="number" class="form-control" id="cantidad" required min="1" placeholder="Cantidad a mover">
            </div>

            <div class="mb-3">
                <label for="glosa" class="form-label">Glosa/Descripción</label>
                <input type="text" class="form-control" id="glosa" required placeholder="Ej: Venta #123, Reposición matutina">
            </div>

            <button type="submit" class="btn btn-primary">Registrar Movimiento</button>
            <button type="button" class="btn btn-secondary" onclick="document.getElementById('menuMovimientos').click()">Cancelar</button>
        </form>`;

    // --- Lógica de envío del Formulario ---
    document.getElementById("vendedorMovimientoForm").addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = {
            tipo: document.getElementById("tipoMovimiento").value,
            id_producto: parseInt(document.getElementById("idProducto").value),
            cantidad: parseInt(document.getElementById("cantidad").value),
            glosa: document.getElementById("glosa").value,
        };

        try {
            // Asume que createMovimiento está definido en api.js
            await createMovimiento(data);
            alert("Movimiento registrado correctamente.");
            document.getElementById("menuMovimientos").click(); // Volver a la lista
        } catch (error) {
            console.error("Error al guardar movimiento:", error);
            alert(`Error al registrar el movimiento. Revisa la consola o los datos ingresados: ${error.message}`);
        }
    });
}