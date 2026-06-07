/**
 * Sets the item input to the clicked menu item.
 */
function whichAnimationEvent() {
  // Detect supported animation iteration.
  var element = document.createElement("fakeelement");
  var animations = {
    animation: "animationiteration",
    OAnimation: "oAnimationIteration",
    MozAnimation: "animationiteration",
    WebkitAnimation: "webkitAnimationIteration",
  };
  for (let i in animations) {
    if (element.style[i] !== undefined) {
      return animations[i];
    }
  }
}

const itemInput = document.getElementById("user-item-input");
const countInput = document.getElementById("user-count-input");

itemInput.addEventListener(whichAnimationEvent(), function () {
  itemInput.classList.remove("animation-flash");
});

document.querySelectorAll(".menu-item").forEach((menuItem) => {
  menuItem.addEventListener("click", function () {
    itemName = menuItem.querySelector("img").alt;
    itemInput.value = itemName;
    itemInput.classList.add("animation-flash");
    countInput.value = "";
    countInput.focus();
  });
});
