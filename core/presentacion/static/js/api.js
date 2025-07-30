document.getElementById("form-registro").addEventListener("submit", async function(e) {
  e.preventDefault();

  const formData = new FormData(this);
  const data = {};
  formData.forEach((value, key) => data[key] = value);

  const res = await fetch("http://localhost:8000/api/registro/", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data)
  });

  const mensajeDiv = document.getElementById("mensaje");

  if (res.ok) {
    mensajeDiv.style.color = "green";
    mensajeDiv.textContent = "✅ Registro exitoso";
    this.reset();
  } else {
    const error = await res.json();
    mensajeDiv.style.color = "red";
    mensajeDiv.textContent = "❌ Error: " + Object.values(error).join(" | ");
  }
});
