document.addEventListener('DOMContentLoaded', () => {
  let active = null;
  const close = () => { if (active) active.remove(); active = null; };

  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });
  document.addEventListener('click', (e) => { if (active && !active.contains(e.target)) close(); });

  document.querySelectorAll('.plaque__share-btn').forEach((btn) => {
    btn.addEventListener('click', async (e) => {
      e.stopPropagation();
      close();
      const card = btn.closest('article');
      const id = card?.dataset.skillId;
      if (!id) return;
      const pop = document.createElement('div');
      pop.className = 'share-popover';
      pop.innerHTML = '<button data-act="copy">Copy link</button><button data-act="download">Download card</button><button disabled title="Embeddable badge coming in a future release">Badge — coming soon</button>';
      btn.parentElement?.appendChild(pop);
      active = pop;
      pop.onclick = async (ev) => {
        const act = ev.target?.dataset?.act;
        if (act === 'copy') {
          await navigator.clipboard.writeText(`${location.href.split('#')[0]}#${id}`);
          close();
        }
        if (act === 'download') {
          const h = location.pathname.split('/').filter(Boolean).at(-2);
          const a = document.createElement('a');
          a.href = `../../og/${h}/${id.split('/').pop()}.svg`;
          a.download = `${id.split('/').pop()}.svg`;
          a.click();
          close();
        }
      };
    });
  });
});
