document.addEventListener('DOMContentLoaded', () => {
  const hudToggleBtn = document.getElementById('hudToggleBtn');
  const canvas3d = document.getElementById('canvas3d');
  
  if (!hudToggleBtn || !canvas3d) return;

  let isHudMode = false;

  // Set ambient styling by default
  canvas3d.style.opacity = '0.18';
  canvas3d.style.filter = 'sepia(1) hue-rotate(5deg) saturate(3)'; // Muted gold tint

  hudToggleBtn.addEventListener('click', () => {
    isHudMode = !isHudMode;
    if (isHudMode) {
      hudToggleBtn.textContent = '⇄ View as 2D Graph';
      canvas3d.style.opacity = '1';
      canvas3d.style.filter = 'none'; // Restore original colors
      canvas3d.style.zIndex = '5'; // Bring to front
    } else {
      hudToggleBtn.textContent = '⇄ View as HUD';
      canvas3d.style.opacity = '0.18';
      canvas3d.style.filter = 'sepia(1) hue-rotate(5deg) saturate(3)';
      canvas3d.style.zIndex = '0'; // Send to back
    }
  });

  // Mobile fallback (disable 3D HUD if screen width < 768px)
  if (window.innerWidth < 768) {
    canvas3d.style.display = 'none';
  }
});
