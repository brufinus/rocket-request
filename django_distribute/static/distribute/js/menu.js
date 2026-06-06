/**
 * Sets the item input to the clicked menu item.
 */
const itemInput = document.getElementById("user-item-input");
const countInput = document.getElementById("user-count-input");
document.querySelectorAll(".menu-item").forEach((menuItem) => {
  menuItem.addEventListener("click", function () {
    itemName = menuItem.querySelector("img").alt;
    itemInput.value = itemName;
    countInput.value = "";
    countInput.focus();
  });
});
