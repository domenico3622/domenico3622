const scoreEl = document.getElementById('score');
const statusEl = document.getElementById('status');
const imgEl = document.getElementById('sakuragi-img');
const barEl = document.getElementById('energy-bar');
const btn = document.getElementById('action-btn');

let score = 0;
const DUNK_THRESHOLD = 20;

// Load assets preload
const img1 = new Image(); img1.src = 'assets/step1.png';
const img2 = new Image(); img2.src = 'assets/step2.png';
const img3 = new Image(); img3.src = 'assets/step3.png';

btn.addEventListener('click', () => {
    score++;
    updateGame();
    animateBtn();
});

function updateGame() {
    scoreEl.innerText = score;
    
    // Update Energy Bar
    let percentage = Math.min((score / DUNK_THRESHOLD) * 100, 100);
    barEl.style.width = percentage + '%';

    // Game Logic
    if (score < 10) {
        statusEl.innerText = "DRIBBLING...";
        statusEl.style.color = "#fff";
        imgEl.src = 'assets/step1.png';
        imgEl.className = "bounce"; 
    } else if (score < DUNK_THRESHOLD) {
        statusEl.innerText = "CHARGING...";
        statusEl.style.color = "#ffd700";
        imgEl.src = 'assets/step2.png';
        imgEl.classList.remove("bounce");
    } else if (score === DUNK_THRESHOLD) {
        performDunk();
    }
}

function performDunk() {
    statusEl.innerText = "SLAM DUNK!!!";
    statusEl.style.color = "#ff3e3e";
    imgEl.src = 'assets/step3.png';
    imgEl.className = "dunk-anim";
    
    // Effects
    createConfetti();
    
    // Reset after delay
    setTimeout(() => {
        score = 0;
        updateGame();
        imgEl.classList.remove("dunk-anim");
        // Reset image to step1
        imgEl.src = 'assets/step1.png';
        statusEl.innerText = "WAITING...";
        statusEl.style.color = "#fff";
    }, 3000);
}

function animateBtn() {
    btn.style.transform = 'scale(0.95)';
    setTimeout(() => btn.style.transform = 'scale(1)', 100);
}

function createConfetti() {
    for(let i=0; i<30; i++) {
        const basket = document.createElement('div');
        basket.innerText = '🏀';
        basket.classList.add('basket');
        basket.style.left = Math.random() * 100 + 'vw';
        basket.style.animationDuration = Math.random() * 2 + 1 + 's';
        document.body.appendChild(basket);
        setTimeout(() => basket.remove(), 3000);
    }
}

// Initial state
updateGame();
