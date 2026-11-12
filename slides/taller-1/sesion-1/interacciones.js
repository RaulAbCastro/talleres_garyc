/* Local interactions for the Marginalia workshop. No state leaves the browser. */
(() => {
  "use strict";

  function initialize() {
    configureKeyboard();
    document.querySelectorAll(".quiz").forEach((quiz) => {
      if (quiz.dataset.initialized === "true") return;
      quiz.dataset.initialized = "true";

      let feedback = quiz.querySelector(".quiz-feedback");
      if (!feedback) {
        feedback = document.createElement("p");
        feedback.className = "quiz-feedback";
        quiz.append(feedback);
      }
      feedback.setAttribute("aria-live", "polite");
      feedback.setAttribute("aria-atomic", "true");

      const buttons = [...quiz.querySelectorAll("button[data-correct]")];
      buttons.forEach((button) => {
        button.type = "button";
        button.setAttribute("aria-pressed", "false");
        button.addEventListener("click", (event) => {
          event.stopPropagation();
          buttons.forEach((other) => {
            other.setAttribute("aria-pressed", String(other === button));
            other.classList.remove("is-correct", "is-incorrect");
          });
          const correct = button.dataset.correct === "true";
          button.classList.add(correct ? "is-correct" : "is-incorrect");
          const text = button.dataset.feedback || (correct
            ? "Correcto. Explica tu razonamiento al grupo."
            : "Revisa la interpretación e intenta de nuevo.");
          feedback.textContent = `${correct ? "Correcto. " : "Revisa. "}${text}`;
        });
      });
    });
  }

  // Reveal listens for keys on document. Stop bubbling while preserving the
  // editor's own key handlers, selections, shortcuts and native text input.
  const interactiveSelector = [
    "textarea", "input", "select", "button", "[contenteditable]",
    ".cm-editor", ".ace_editor", ".monaco-editor", ".quiz"
  ].join(",");

  function configureKeyboard() {
    if (!window.Reveal || typeof window.Reveal.configure !== "function") return;
    if (window.Reveal.__marginaliaKeyboardConfigured) return;
    const previous = typeof window.Reveal.getConfig === "function"
      ? window.Reveal.getConfig().keyboardCondition : null;
    window.Reveal.configure({
      keyboardCondition(event) {
        if (event.key !== "Escape" && event.target instanceof Element
            && event.target.closest(interactiveSelector)) return false;
        return typeof previous === "function" ? previous(event) : true;
      }
    });
    window.Reveal.__marginaliaKeyboardConfigured = true;
  }
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") return;
    if (event.target instanceof Element && event.target.closest(interactiveSelector)) {
      event.stopPropagation();
    }
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize, { once: true });
  } else {
    initialize();
  }
  if (window.Reveal && typeof window.Reveal.on === "function") {
    window.Reveal.on("ready", initialize);
  }
})();
