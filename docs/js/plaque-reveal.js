class PlaqueReveal {
  constructor() {
    this.createContainer();
  }

  createContainer() {
    this.container = document.createElement('div');
    this.container.className = 'plaque-reveal-container';
    
    this.container.innerHTML = `
      <div class="plaque-plate" id="plaquePlate">
        <img src="assets/marks/diamond-seal.svg" class="plaque-seal" alt="Diamond Seal">
        <div class="plaque-name" id="plaqueName"></div>
        <div class="plaque-handle" id="plaqueHandle"></div>
        <div class="plaque-stars" id="plaqueStars"></div>
        <div class="plaque-class" id="plaqueClass" style="opacity: 0"></div>
      </div>
    `;
    
    document.body.appendChild(this.container);
    
    // Close on click outside
    this.container.addEventListener('click', (e) => {
      if (e.target === this.container) {
        this.close();
      }
    });
  }

  async play(skillName, handle, stars, evidenceClass) {
    // Reset state
    document.getElementById('plaqueName').textContent = '';
    document.getElementById('plaqueHandle').textContent = '';
    document.getElementById('plaqueStars').innerHTML = '';
    document.getElementById('plaqueClass').textContent = `CLASS ${evidenceClass}`;
    document.getElementById('plaqueClass').style.opacity = '0';
    document.getElementById('plaquePlate').classList.remove('reveal-step-name');

    // Show container
    this.container.classList.add('active');

    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (reducedMotion) {
      document.getElementById('plaqueName').textContent = skillName;
      document.getElementById('plaqueHandle').textContent = handle;
      document.getElementById('plaqueStars').innerHTML = '★'.repeat(stars);
      document.getElementById('plaqueClass').style.opacity = '1';
      return;
    }

    // 4s Cinematic Timeline
    
    // t=0.8s: Plate emerges (handled by CSS transition on .active)
    await this.wait(800);
    
    // t=1.4s: Gold ink pours
    document.getElementById('plaqueName').textContent = skillName;
    document.getElementById('plaquePlate').classList.add('reveal-step-name');
    await this.wait(1000);

    // t=2.4s: Handle resolves
    document.getElementById('plaqueHandle').textContent = handle;
    await this.wait(400);

    // t=2.8s: Stars ignite
    const starsContainer = document.getElementById('plaqueStars');
    for (let i = 0; i < stars; i++) {
      const star = document.createElement('span');
      star.textContent = '★';
      star.style.opacity = '0';
      star.style.transform = 'scale(0)';
      star.style.transition = 'all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
      starsContainer.appendChild(star);
      
      // trigger reflow
      void star.offsetWidth;
      
      star.style.opacity = '1';
      star.style.transform = 'scale(1)';
      await this.wait(150); // slight delay between stars
    }

    // t=3.4s: Evidence class stamps
    await this.wait(400);
    const classBadge = document.getElementById('plaqueClass');
    classBadge.style.opacity = '1';
    classBadge.style.transform = 'scale(1.2)';
    classBadge.style.transition = 'all 0.15s ease-out';
    
    await this.wait(150);
    classBadge.style.transform = 'scale(1)';
  }

  close() {
    this.container.classList.remove('active');
  }

  wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

window.plaqueSystem = new PlaqueReveal();
