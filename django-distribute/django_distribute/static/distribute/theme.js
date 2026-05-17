/**
 * Handles toggling of theme.
 */
const button = document.getElementById("theme-toggle");

button.addEventListener("click", function () {
  document.documentElement.classList.toggle("light-theme");
  const theme = document.documentElement.classList.contains("light-theme")
    ? "light"
    : "dark";
  localStorage.setItem("theme", theme);
});
