(function () {
  const svg = document.getElementById("grafico-progreso");
  const datos = window.datosProgreso;
  if (!svg || !datos || datos.length === 0) return;

  const width = 600;
  const height = 300;
  const padding = 40;
  const ns = "http://www.w3.org/2000/svg";

  const pesos = datos.map((d) => d.peso);
  const min = Math.min(...pesos);
  const max = Math.max(...pesos);
  const rango = max - min || 1;

  const puntos = datos.map((d, i) => {
    const x = padding + (i * (width - 2 * padding)) / Math.max(datos.length - 1, 1);
    const y = height - padding - ((d.peso - min) / rango) * (height - 2 * padding);
    return [x, y];
  });

  const ejeX = document.createElementNS(ns, "line");
  ejeX.setAttribute("x1", padding);
  ejeX.setAttribute("y1", height - padding);
  ejeX.setAttribute("x2", width - padding);
  ejeX.setAttribute("y2", height - padding);
  ejeX.setAttribute("stroke", "#2a2a2a");
  svg.appendChild(ejeX);

  const linea = document.createElementNS(ns, "polyline");
  linea.setAttribute("points", puntos.map((p) => p.join(",")).join(" "));
  linea.setAttribute("fill", "none");
  linea.setAttribute("stroke", "#f5c400");
  linea.setAttribute("stroke-width", "2");
  svg.appendChild(linea);

  puntos.forEach(([x, y], i) => {
    const circulo = document.createElementNS(ns, "circle");
    circulo.setAttribute("cx", x);
    circulo.setAttribute("cy", y);
    circulo.setAttribute("r", "4");
    circulo.setAttribute("fill", "#f5c400");
    svg.appendChild(circulo);

    const etiqueta = document.createElementNS(ns, "text");
    etiqueta.setAttribute("x", x);
    etiqueta.setAttribute("y", height - padding + 16);
    etiqueta.setAttribute("fill", "#a3a3a3");
    etiqueta.setAttribute("font-size", "10");
    etiqueta.setAttribute("text-anchor", "middle");
    etiqueta.textContent = datos[i].fecha;
    svg.appendChild(etiqueta);
  });
})();
