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

