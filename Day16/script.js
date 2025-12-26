const TARGET_DATE = new Date("December 1, 2026 10:00:00").getTime();
const FACTS = [
    "Last year's festival served over 5,000 cups of hot cocoa! ☕",
    "The 2025 Ice Sculpture weighed 3 tons! 🧊",
    "It takes 50 volunteers to hang the main street lights. 💡",
    "The Yeti mascot is named 'Frostbite' by popular vote. 🥶",
    "The festival generates 100% of its power from renewable sources. ♻️"
];

function init() {
    // 1. Check Persistence
    if (localStorage.getItem('email_signed_up')) {
        document.getElementById('email-form').classList.add('hidden');
        document.getElementById('success-msg').classList.remove('hidden');
    }

    // 2. Start Loops
    setInterval(updateTimer, 1000);
    updateTimer(); 
    
    setInterval(rotateFacts, 5000);
    rotateFacts(); 
}

function updateTimer() {
    const now = new Date().getTime();
    const diff = TARGET_DATE - now;

    if (diff < 0) return; 

    const d = Math.floor(diff / (1000 * 60 * 60 * 24));
    const h = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const s = Math.floor((diff % (1000 * 60)) / 1000);

    document.getElementById('days').innerText = d;
    document.getElementById('hours').innerText = String(h).padStart(2, '0');
    document.getElementById('mins').innerText = String(m).padStart(2, '0');
    document.getElementById('secs').innerText = String(s).padStart(2, '0');
}

let factIndex = 0;
function rotateFacts() {
    const el = document.getElementById('fun-fact');
    el.style.opacity = 0;
    setTimeout(() => {
        el.innerText = FACTS[factIndex];
        el.style.opacity = 1;
        factIndex = (factIndex + 1) % FACTS.length;
    }, 500);
}

function handleForm(e) {
    e.preventDefault();
    localStorage.setItem('email_signed_up', 'true');
    document.getElementById('email-form').classList.add('hidden');
    document.getElementById('success-msg').classList.remove('hidden');
}

window.onload = init;
