(async () => {
  const params = new URLSearchParams(window.location.search);
  const id = params.get('id');
  if (!id) return;
  async function update() {
    const res = await fetch(`/api/user/${id}`);
    if (!res.ok) return;
    const data = await res.json();
    document.getElementById('counter').innerText = `${data.balance.toFixed(2)} TRX`;
  }
  update();
  setInterval(update, 5000);
})();
