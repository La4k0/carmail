const form = document.querySelector(".filter-grid");
const demoButton = document.querySelector(".btn-outline");

//if (form) {
//  form.addEventListener("submit", (event) => {
//    event.preventDefault();
//
//    const formData = new FormData(form);
//    const selectedData = Object.fromEntries(formData.entries());
//    selectedData.only_new_listings = formData.get("only_new_listings") ? "yes" : "no";
//
//    // Placeholder for Flask integration: send selected filters to backend endpoint.
//    console.log("Избрани критерии:", selectedData);
//    alert("Филтърът е записан. Свържи формата към Flask endpoint за реално запазване.");
//  });
//}

if (demoButton) {
  demoButton.addEventListener("click", () => {
    alert("Тук можеш да покажеш примерен Excel файл или premium upsell модал.");
  });
}

const brandSelect = document.getElementById("brand-select");
const modelSelect = document.getElementById("model-select");

brandSelect.addEventListener("change", async () => {
  const brand = brandSelect.value;

  // reset
  modelSelect.innerHTML = '<option value="">Зареждане...</option>';
  modelSelect.disabled = true;

  if (!brand) {
    modelSelect.innerHTML = '<option value="">Първо избери марка</option>';
    return;
  }

  try {
    const response = await fetch(`/models/${encodeURIComponent(brand)}`);
    const models = await response.json();

    modelSelect.innerHTML = '<option value="">Избери модел</option>';

    models.forEach(model => {
      const option = document.createElement("option");
      option.value = model;
      option.textContent = model;
      modelSelect.appendChild(option);
    });

    modelSelect.disabled = false;

  } catch (err) {
    console.error(err);
    modelSelect.innerHTML = '<option value="">Грешка при зареждане</option>';
  }
});
