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
        function createLineChart(canvasId, label, data, color) {
        const canvas = document.getElementById(canvasId);

        if (!canvas || typeof Chart === "undefined") {
            return;
        }

        new Chart(canvas, {
            type: "line",
            data: {
                labels: window.stockChartLabels || [],
                datasets: [{
                    label: label,
                    data: data || [],
                    borderColor: color,
                    backgroundColor: color.replace("1)", "0.12)"),
                    borderWidth: 3,
                    tension: 0.35,
                    fill: true,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: "#f8fafc"
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: { color: "#94a3b8" },
                        grid: { color: "rgba(255,255,255,0.06)" }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: { color: "#94a3b8" },
                        grid: { color: "rgba(255,255,255,0.06)" }
                    }
                }
            }
        });
    }

    createLineChart(
        "importChart",
        "Quantité importée",
        window.stockChartEntrees,
        "rgba(16, 185, 129, 1)"
    );

    createLineChart(
        "exportChart",
        "Quantité exportée",
        window.stockChartSorties,
        "rgba(244, 63, 94, 1)"
    );
        const chartRows = document.querySelectorAll("#chart-data span");

    const labels = [];
    const entrees = [];
    const sorties = [];

    chartRows.forEach((row) => {
        labels.push(row.dataset.date);
        entrees.push(Number(row.dataset.entree) || 0);
        sorties.push(Number(row.dataset.sortie) || 0);
    });

    function createLineChart(canvasId, label, data, color) {
        const canvas = document.getElementById(canvasId);

        if (!canvas || typeof Chart === "undefined") {
            return;
        }

        new Chart(canvas, {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: data,
                    borderColor: color,
                    backgroundColor: color.replace("1)", "0.12)"),
                    borderWidth: 3,
                    tension: 0.35,
                    fill: true,
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        ticks: { color: "#94a3b8" },
                        grid: { color: "rgba(255,255,255,0.06)" }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: { color: "#94a3b8" },
                        grid: { color: "rgba(255,255,255,0.06)" }
                    }
                },
                plugins: {
                    legend: {
                        labels: { color: "#f8fafc" }
                    }
                }
            }
        });
    }

    createLineChart("importChart", "Quantité importée", entrees, "rgba(16, 185, 129, 1)");
    createLineChart("exportChart", "Quantité exportée", sorties, "rgba(244, 63, 94, 1)");


});
