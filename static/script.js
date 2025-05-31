// Obtener referencias a los elementos del DOM
const englishInput = document.getElementById("englishInput");
const phoneticOutput = document.getElementById("phoneticOutput");
const generateButton = document.getElementById("generateButton");
const copyButton = document.getElementById("copyButton");

// Funcionalidad del botón 'Generate'
generateButton.addEventListener("click", async () => {
  const text = englishInput.value.trim();
  if (!text) {
    phoneticOutput.value =
      "Por favor, introduce algún texto para obtener su pronunciación.";
    return;
  }

  generateButton.disabled = true; // Deshabilitar el botón mientras se procesa
  const originalGenerateButtonText =
    generateButton.querySelector(".truncate").textContent;
  generateButton.querySelector(".truncate").textContent = "Generando...";

  try {
    // Realizar la solicitud POST al backend
    const response = await fetch("/generate_pronunciation", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ english_text: text }),
    });

    const data = await response.json();

    if (response.ok) {
      phoneticOutput.value = data.pronunciation;
    } else {
      phoneticOutput.value = "Error: " + (data.error || "Algo salió mal.");
    }
  } catch (error) {
    console.error("Error al conectar con el servidor:", error);
    phoneticOutput.value = "Error de conexión. Intenta de nuevo más tarde.";
  } finally {
    generateButton.disabled = false; // Habilitar el botón de nuevo
    generateButton.querySelector(".truncate").textContent =
      originalGenerateButtonText;
  }
});

// Funcionalidad del botón 'Copy'
copyButton.addEventListener("click", () => {
  const textToCopy = phoneticOutput.value;
  if (
    !textToCopy ||
    textToCopy === "Phonetic Spanish" ||
    textToCopy.startsWith("Error")
  ) {
    alert("No hay texto válido para copiar.");
    return;
  }

  navigator.clipboard
    .writeText(textToCopy)
    .then(() => {
      const originalCopyButtonText =
        copyButton.querySelector(".truncate").textContent;
      copyButton.querySelector(".truncate").textContent = "¡Copiado!";
      setTimeout(() => {
        copyButton.querySelector(".truncate").textContent =
          originalCopyButtonText;
      }, 1500); // Vuelve al texto original después de 1.5 segundos
    })
    .catch((err) => {
      console.error("Error al copiar el texto: ", err);
      const originalCopyButtonText =
        copyButton.querySelector(".truncate").textContent;
      copyButton.querySelector(".truncate").textContent = "Error!";
      setTimeout(() => {
        copyButton.querySelector(".truncate").textContent =
          originalCopyButtonText;
      }, 2000);
    });
});

// Función para cargar los íconos SVG dinámicamente
function loadSvgIcons() {
  const iconContainers = document.querySelectorAll("[data-icon]"); // Busca elementos con el atributo data-icon

  iconContainers.forEach((container) => {
    const iconName = container.getAttribute("data-icon");
    const iconSize = container.getAttribute("data-size") || "24px"; // Tamaño por defecto
    const iconPath = iconPaths[iconName]; // Accede al objeto iconPaths definido en icons.js

    if (iconPath) {
      container.innerHTML = `
              <svg xmlns="http://www.w3.org/2000/svg" width="${iconSize}" height="${iconSize}" fill="currentColor" viewBox="0 0 256 256">
                  <path d="${iconPath}"></path>
              </svg>
          `;
    } else {
      console.warn(`Icono '${iconName}' no encontrado en iconPaths.`);
    }
  });
}

// Llama a la función para cargar los íconos cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", loadSvgIcons);
