document.addEventListener("DOMContentLoaded", () => {
    const counters = document.querySelectorAll(".counter");
    const speed = 50;

    counters.forEach((counter) => {
        const updateCount = () => {
            const target = Number(counter.getAttribute("data-target")) || 0;
            const count = Number(counter.innerText) || 0;
            const inc = target / speed;

            if (count < target) {
                counter.innerText = Math.ceil(count + inc);
                setTimeout(updateCount, 20);
            } else {
                counter.innerText = target;
            }
        };

        updateCount();
    });

    const currentTime = document.getElementById("current-time");

    function updateClock() {
        if (!currentTime) return;

        const now = new Date();
        currentTime.innerText = now.toLocaleTimeString("fr-FR");
    }

    setInterval(updateClock, 1000);
    updateClock();

    const cards = document.querySelectorAll(".stat-card");

    cards.forEach((card, index) => {
        card.style.opacity = "0";
        card.style.transform = "translateY(20px)";

        setTimeout(() => {
            card.style.transition = "all 0.6s ease";
            card.style.opacity = "1";
            card.style.transform = "translateY(0)";
        }, 100 * index);
    });
});
