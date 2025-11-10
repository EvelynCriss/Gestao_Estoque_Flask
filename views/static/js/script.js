//header
document.addEventListener("DOMContentLoaded", () => {
  const headerContainer = document.getElementById("header");

  fetch("header.html")
    .then(response => response.text())
    .then(data => {
      headerContainer.innerHTML = data;
    })
    .catch(err => console.error("Erro ao carregar o header:", err));
});
