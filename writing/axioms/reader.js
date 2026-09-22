const sidebar = document.querySelector(".reader-sidebar");
const mobileToggle = document.querySelector(".toc-mobile-toggle");
const toc = document.querySelector(".reader-toc");
if (sidebar && mobileToggle && toc) {
  mobileToggle.addEventListener("click", () => {
    const open = sidebar.classList.toggle("is-open");
    mobileToggle.setAttribute("aria-expanded", String(open));
  });
  for (const group of toc.querySelectorAll(".toc-group")) {
    const button = group.querySelector("button.toc-parent");
    if (!button) continue;
    button.addEventListener("click", () => {
      const open = group.classList.toggle("is-open");
      button.setAttribute("aria-expanded", String(open));
      group.querySelector(".toc-children").inert = !open;
      const target = document.getElementById(button.dataset.target);
      if (target) target.scrollIntoView({ behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth" });
      if (target) history.replaceState(null, "", "#" + target.id);
    });
  }
  const links = [...toc.querySelectorAll('a[href^="#"]')];
  const headings = [...document.querySelectorAll(".reader-prose h2[id], .reader-prose h3[id]")];
  if (location.hash) {
    const hashLink = links.find((link) => link.getAttribute("href") === location.hash);
    const group = hashLink?.closest(".toc-group");
    if (group?.querySelector("button.toc-parent")) {
      group.classList.add("is-open");
      group.querySelector("button.toc-parent").setAttribute("aria-expanded", "true");
      group.querySelector(".toc-children").inert = false;
    }
  }
  const updateActive = () => {
    if (!headings.length) return;
    let active = headings[0];
    for (const heading of headings) {
      if (heading.getBoundingClientRect().top <= 155) active = heading;
      else break;
    }
    for (const link of links) {
      const selected = link.getAttribute("href") === "#" + active.id;
      link.classList.toggle("is-active", selected);
      if (selected) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    }
    for (const group of toc.querySelectorAll(".toc-group")) {
      const parent = group.querySelector("button.toc-parent");
      if (parent) parent.classList.toggle("is-active", parent.dataset.target === active.id);
    }
  };
  let scheduled = false;
  window.addEventListener("scroll", () => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => { updateActive(); scheduled = false; });
  }, { passive: true });
  updateActive();
}
