/**
 * Pastes clipboard contents.
 */
const textDest = document.getElementById("blueprint-input");
const pasteBtn = document.getElementById("paste-button");

function pasteFromClipboard() {
  navigator.clipboard.readText().then(function (e) {
    $(textDest).val(e);
  });
}

pasteBtn.addEventListener("click", pasteFromClipboard);
