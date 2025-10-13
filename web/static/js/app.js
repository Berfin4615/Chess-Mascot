let board, chess, data, idx = -1, timer = null;

async function loadAnalysis() {
  try {
    const res = await fetch("/api/analysis");
    const text = await res.text();
    console.log("🔍 API cevabı:", text);
    data = JSON.parse(text);
  } catch (e) {
    console.error("❌ Veri alınamadı:", e);
    document.getElementById("bubble-text").textContent = "Analiz verisi alınamadı.";
    return;
  }

  if (!data || !data.moves) {
    console.error("❌ API hatalı veri döndürdü:", data);
    document.getElementById("bubble-text").textContent = "Analiz boş veya hatalı.";
    return;
  }

  console.log("✅ Veri başarıyla alındı:", data);

  chess = new Chess(data.initial_fen);
  board = Chessboard('board', { position: data.initial_fen, draggable: false });

  const mvBox = document.getElementById("moves");
  mvBox.innerHTML = "";
  data.moves.forEach((m, i) => {
    const span = document.createElement("span");
    span.className = "mv";
    span.textContent = (i + 1) + ". " + m.san;
    span.addEventListener("click", () => goTo(i));
    mvBox.appendChild(span);
  });

  idx = -1;
  updateUI();
}

function updateUI() {
  if (!data || !data.moves) return; // 👈 koruma eklendi
  const bubble = document.getElementById("bubble-text");
  const evalVal = document.getElementById("eval-val");
  const evalType = document.getElementById("eval-type");
  const plyEl = document.getElementById("ply");

  if (idx < 0) {
    bubble.textContent = "Hazırım! ▶ Oynat'a bas, hamle hamle anlatayım ✨";
    evalVal.textContent = "-"; evalType.textContent = "-"; plyEl.textContent = "0";
    highlightMove(null);
    return;
  }

  const m = data.moves[idx];
  if (!m) return;

  board.position(m.fen_after, true);
  bubble.textContent = m.comment;
  evalType.textContent = m.eval.type;
  evalVal.textContent = m.eval.value;
  plyEl.textContent = (idx + 1);
  highlightMove(idx);
}

function highlightMove(i) {
  document.querySelectorAll(".mv").forEach((el, k) => {
    el.classList.toggle("active", k === i);
  });
}

function step(dir) {
  if (!data || !data.moves) return;
  const next = idx + dir;
  if (next < -1 || next >= data.moves.length) return;
  if (next === -1) {
    chess.reset();
    board.position(data.initial_fen, true);
    idx = -1;
    updateUI();
    return;
  }
  idx = next;
  updateUI();
}

function goTo(i) {
  if (!data || !data.moves) return;
  idx = i;
  updateUI();
}

function play() {
  if (!data || !data.moves) return;
  if (timer) {
    clearInterval(timer);
    timer = null;
    document.getElementById("btn-play").textContent = "▶ Oynat";
    return;
  }
  const speed = +document.getElementById("speed").value;
  document.getElementById("btn-play").textContent = "⏸ Durdur";
  timer = setInterval(() => {
    if (idx >= data.moves.length - 1) {
      play();
      return;
    }
    step(+1);
  }, speed);
}

document.addEventListener("DOMContentLoaded", async () => {
  document.getElementById("btn-start").onclick = () => { idx = -1; updateUI(); };
  document.getElementById("btn-prev").onclick = () => step(-1);
  document.getElementById("btn-next").onclick = () => step(+1);
  document.getElementById("btn-end").onclick = () => { idx = data?.moves?.length - 1; updateUI(); };
  document.getElementById("btn-play").onclick = play;

  await loadAnalysis(); // 👈 Artık tüm düğmelerden önce çağrılıyor
});
