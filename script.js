/* Slam Dunk Script */

const player = document.getElementById('player');
let isAnimating = false;

function startDunkSequence() {
    if (isAnimating) return;
    isAnimating = true;

    // Reset Position
    player.style.transition = 'none';
    player.style.left = '-150px';
    player.style.bottom = '40px';
    player.style.transform = 'none';
    player.className = 'sakuragi run'; // Start Running animation

    // Force reflow
    void player.offsetWidth;

    // 1. Run to Jump Point
    // It takes e.g. 2 seconds to reach the paint
    player.style.transition = 'left 2s linear';
    player.style.left = '450px'; // Near hoop

    // Schedule next steps
    setTimeout(() => {
        // 2. Prep/Crouch
        player.className = 'sakuragi prep';

        // Short pause for gathering strength
        setTimeout(() => {
            // 3. Jump Animation
            player.className = 'sakuragi jump-up';
            // Physics movement
            player.style.transition = 'left 0.5s linear, bottom 0.5s ease-out';
            player.style.left = '580px'; // Move closer to rim
            player.style.bottom = '200px'; // Fly up

            setTimeout(() => {
                // 4. Mid Air (peak)
                player.className = 'sakuragi mid-air';

                setTimeout(() => {
                    // 5. SLAM DUNK
                    player.className = 'sakuragi dunk';
                    player.style.transition = 'bottom 0.2s ease-in';
                    player.style.bottom = '180px'; // Slight drop/hang

                    // Shake effect?
                    document.querySelector('.court').style.animation = 'shake 0.2s';
                    setTimeout(() => document.querySelector('.court').style.animation = '', 200);

                    setTimeout(() => {
                        // 6. Land
                        player.style.transition = 'bottom 0.3s ease-in';
                        player.style.bottom = '40px'; // Floor
                        player.className = 'sakuragi land';

                        setTimeout(() => {
                            isAnimating = false; // Done
                            // Maybe walk away or stay posed
                        }, 1000);

                    }, 400); // Hang time

                }, 150); // Mid air duration

            }, 350); // Jump up duration

        }, 100); // Prep duration

    }, 2000); // Run duration
}

// Add shake keyframes dynamically
const styleSheet = document.createElement("style");
styleSheet.innerText = `
@keyframes shake {
    0% { transform: translate(1px, 1px) rotate(0deg); }
    10% { transform: translate(-1px, -2px) rotate(-1deg); }
    20% { transform: translate(-3px, 0px) rotate(1deg); }
    30% { transform: translate(3px, 2px) rotate(0deg); }
    40% { transform: translate(1px, -1px) rotate(1deg); }
    50% { transform: translate(-1px, 2px) rotate(-1deg); }
    60% { transform: translate(-3px, 1px) rotate(0deg); }
    70% { transform: translate(3px, 1px) rotate(-1deg); }
    80% { transform: translate(-1px, -1px) rotate(1deg); }
    90% { transform: translate(1px, 2px) rotate(0deg); }
    100% { transform: translate(1px, -2px) rotate(-1deg); }
}
`;
document.head.appendChild(styleSheet);

// Auto start on load
window.onload = () => {
    setTimeout(startDunkSequence, 500);
};
