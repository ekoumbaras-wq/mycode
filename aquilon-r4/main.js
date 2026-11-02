(() => {
  const landImg = document.getElementById("hero-land");
  const waterImg = document.getElementById("hero-water");
  const modeButtons = document.querySelectorAll("[data-mode]");
  const foldRange = document.getElementById("fold-range");
  const armGroup = document.getElementById("arm-group");
  const foldLabel = document.getElementById("fold-label");
  const foldSub = document.getElementById("fold-sub");

  function setMode(mode) {
    const isWater = mode === "water";
    landImg.classList.toggle("is-active", !isWater);
    waterImg.classList.toggle("is-active", isWater);
    modeButtons.forEach((btn) => {
      const active = btn.dataset.mode === mode;
      btn.setAttribute("aria-pressed", String(active));
      btn.classList.toggle("primary", active);
      btn.classList.toggle("ghost", !active);
    });
  }

  modeButtons.forEach((btn) => {
    btn.addEventListener("click", () => setMode(btn.dataset.mode));
  });

  function updateFold(value) {
    const t = Number(value) / 100;
    const angle = t * -78;
    armGroup.setAttribute("transform", `rotate(${angle} 180 200)`);
    if (t < 0.2) {
      foldLabel.textContent = "LAND — wheels deployed";
      foldSub.textContent = "Clearance ~320 mm · bay open";
    } else if (t < 0.8) {
      foldLabel.textContent = "TRANSITION — folding";
      foldSub.textContent = "Bay gasket inflating · jets arming";
    } else {
      foldLabel.textContent = "WATER — wheels stowed";
      foldSub.textContent = "Flush pockets · planing hull clear";
    }
  }

  foldRange.addEventListener("input", (e) => updateFold(e.target.value));
  updateFold(foldRange.value);

  // Gentle auto-demo of fold once when section enters view
  let demonstrated = false;
  const foldSection = document.getElementById("fold");
  if (foldSection && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting || demonstrated) return;
          if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
          demonstrated = true;
          let frame = 0;
          const steps = 48;
          const tick = () => {
            frame += 1;
            const v = Math.round((frame / steps) * 100);
            foldRange.value = String(v);
            updateFold(v);
            if (frame < steps) requestAnimationFrame(tick);
          };
          requestAnimationFrame(tick);
          io.disconnect();
        });
      },
      { threshold: 0.4 }
    );
    io.observe(foldSection);
  }
})();
