document.addEventListener("DOMContentLoaded", () => {
    const body = document.body;
    const efeito = body.dataset.efeito;
    const critico = body.dataset.critico === "true";
    const venceu = body.dataset.venceu === "true";

    const bossCard = document.getElementById("boss-card");
    const playerCard = document.getElementById("player-card");
    const flash = document.getElementById("flash");

    if (efeito === "boss" && bossCard) {
        bossCard.classList.add("shake");
    }

    if (efeito === "jogador" && playerCard) {
        playerCard.classList.add("shake");
        flash.classList.add("damage-flash");
    }

    if (efeito === "cura" && playerCard) {
        playerCard.classList.add("heal-glow");
    }

    if (critico && bossCard) {
        bossCard.classList.add("shake");
    }

    if (venceu) {
        criarConfetes();
    }
});


function criarConfetes() {
    const container = document.getElementById("confetti");
    if (!container) return;

    const simbolos = ["🎉", "✨", "🏆", "⚡"];

    for (let i = 0; i < 34; i++) {
        const item = document.createElement("span");
        item.className = "confetti-piece";
        item.textContent = simbolos[Math.floor(Math.random() * simbolos.length)];
        item.style.left = `${Math.random() * 100}%`;
        item.style.animationDelay = `${Math.random() * 0.8}s`;
        item.style.animationDuration = `${1.7 + Math.random() * 1.6}s`;
        container.appendChild(item);
    }
}
