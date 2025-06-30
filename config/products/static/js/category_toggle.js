document.addEventListener("DOMContentLoaded", function () {
  const toggleBtn = document.getElementById("toggleBtn");
  const hiddenCategories = document.querySelectorAll(".hidden-category");
  let expanded = false;

if (toggleBtn) {

  toggleBtn.addEventListener("click", function () {
    expanded = !expanded;

    hiddenCategories.forEach(item => {
      item.style.display = expanded ? "block" : "none";
    });

    toggleBtn.textContent = expanded ? "View Less" : "View More";
  });

}
});
