/**
 * Handles toggling of theme.
 */
const button = document.getElementById("theme-toggle");

button.addEventListener("click", function () {
  document.documentElement.classList.toggle("dark-theme");
  const theme = document.documentElement.classList.contains("dark-theme")
    ? "dark"
    : "light";
  localStorage.setItem("theme", theme);
});
