document.addEventListener('DOMContentLoaded', () => {
  const root = document.getElementById('profile-timeline');
  const skills = window.PROFILE_SKILLS || [];
  if (!root) return;
  const dated = skills.filter((s) => s.createdAt);
  if (!dated.length) {
    root.innerHTML = '<p class="pt-empty">Timeline data pending</p>';
    return;
  }
  const buckets = new Map();
  dated.forEach((s) => {
    const k = s.createdAt.slice(0, 7);
    if (!buckets.has(k)) buckets.set(k, []);
    buckets.get(k).push(s);
  });
  [...buckets.entries()].sort((a, b) => b[0].localeCompare(a[0])).forEach(([k, arr]) => {
    const d = new Date(`${k}-01T00:00:00Z`);
    const row = document.createElement('div'); row.className = 'pt-row';
    row.innerHTML = `<div class="pt-date">${d.toLocaleString('en-US',{month:'short',year:'numeric'})}</div><div class="pt-chips"></div>`;
    const chips = row.querySelector('.pt-chips');
    arr.sort((a,b)=>b.levelNum-a.levelNum).forEach((s) => {
      const chip = document.createElement('span');
      chip.className = `pt-chip pt-chip--${s.type}`;
      chip.title = `${s.name} · ${s.level} · ${s.type}`;
      chip.textContent = `${s.name} (${s.level})`;
      chips.appendChild(chip);
    });
    root.appendChild(row);
  });
  const io = new IntersectionObserver((entries)=>entries.forEach((e)=>{if(e.isIntersecting)e.target.classList.add('is-in');}),{threshold:0.1});
  root.querySelectorAll('.pt-row').forEach((r)=>io.observe(r));
});
