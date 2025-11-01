document.getElementById("menuProductos")?.addEventListener("click", async () => {
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
});


document.getElementById("menuMovimientos")?.addEventListener("click", async () => {
  const movs = await getMovimientos();
  const html = `
    <h4>Lista de Movimientos</h4>
    <table class="table table-striped">
      <thead><tr><th>ID</th><th>Tipo</th><th>Fecha</th><th>Glosa</th></tr></thead>
      <tbody>${movs
        .map(
          (m) =>
            `<tr><td>${m.id_movimiento}</td><td>${m.tipo}</td><td>${m.fecha}</td><td>${m.glosa}</td></tr>`
        )
        .join("")}</tbody>
    </table>`;
  document.getElementById("contentArea").innerHTML = html;
});
