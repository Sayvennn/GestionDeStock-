document.addEventListener("DOMContentLoaded", () => {
    const counters = document.querySelectorAll(".counter");
    const speed = 50;

    counters.forEach((counter) => {
        const updateCount = () => {
            const target = Number(counter.getAttribute("data-target")) || 0;
            const count = Number(counter.innerText) || 0;
            const inc = Math.max(target / speed, 1);

            if (count < target) {
                counter.innerText = Math.min(Math.ceil(count + inc), target);
                setTimeout(updateCount, 20);
            } else {
                counter.innerText = target;
            }
        };

        updateCount();
    });

    document.querySelectorAll(".stat-card").forEach((card, index) => {
        card.style.opacity = "0";
        card.style.transform = "translateY(20px)";

        setTimeout(() => {
            card.style.transition = "all 0.6s ease";
            card.style.opacity = "1";
            card.style.transform = "translateY(0)";
        }, 100 * index);
    });

    const chartRows = Array.from(document.querySelectorAll("#chart-data span"));
    const labels = chartRows.map((row) => row.dataset.date);
    const entrees = chartRows.map((row) => Number(row.dataset.entree) || 0);
    const sorties = chartRows.map((row) => Number(row.dataset.sortie) || 0);

    function drawLineChart(canvasId, title, data, color) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        const context = canvas.getContext("2d");
        const ratio = window.devicePixelRatio || 1;
        const rect = canvas.getBoundingClientRect();
        const width = Math.max(rect.width, 320);
        const height = Math.max(rect.height, 240);
        const padding = 34;

        canvas.width = width * ratio;
        canvas.height = height * ratio;
        context.setTransform(ratio, 0, 0, ratio, 0, 0);
        context.clearRect(0, 0, width, height);

        const values = data.length ? data : [0];
        const maxValue = Math.max(...values, 1);
        const points = values.map((value, index) => {
            const x = values.length === 1
                ? width / 2
                : padding + (index * (width - padding * 2)) / (values.length - 1);
            const y = height - padding - (value / maxValue) * (height - padding * 2);
            return { x, y, value };
        });

        context.strokeStyle = "rgba(148, 163, 184, 0.18)";
        context.lineWidth = 1;
        for (let i = 0; i < 4; i += 1) {
            const y = padding + (i * (height - padding * 2)) / 3;
            context.beginPath();
            context.moveTo(padding, y);
            context.lineTo(width - padding, y);
            context.stroke();
        }

        context.fillStyle = "#94a3b8";
        context.font = "12px Inter, sans-serif";
        context.fillText(title, padding, 18);
        context.fillText(String(maxValue), 8, padding + 4);
        context.fillText("0", 16, height - padding + 4);

        if (labels.length) {
            context.fillText(labels[0], padding, height - 8);
            context.textAlign = "right";
            context.fillText(labels[labels.length - 1], width - padding, height - 8);
            context.textAlign = "left";
        }

        const gradient = context.createLinearGradient(0, padding, 0, height - padding);
        gradient.addColorStop(0, color.replace("1)", "0.24)"));
        gradient.addColorStop(1, color.replace("1)", "0)"));

        context.beginPath();
        points.forEach((point, index) => {
            if (index === 0) {
                context.moveTo(point.x, point.y);
            } else {
                context.lineTo(point.x, point.y);
            }
        });
        context.lineTo(points[points.length - 1].x, height - padding);
        context.lineTo(points[0].x, height - padding);
        context.closePath();
        context.fillStyle = gradient;
        context.fill();

        context.beginPath();
        points.forEach((point, index) => {
            if (index === 0) {
                context.moveTo(point.x, point.y);
            } else {
                context.lineTo(point.x, point.y);
            }
        });
        context.strokeStyle = color;
        context.lineWidth = 3;
        context.lineJoin = "round";
        context.lineCap = "round";
        context.stroke();

        points.forEach((point) => {
            context.beginPath();
            context.arc(point.x, point.y, 4, 0, Math.PI * 2);
            context.fillStyle = "#0f172a";
            context.fill();
            context.strokeStyle = color;
            context.lineWidth = 2;
            context.stroke();
        });
    }

    drawLineChart("importChart", "Quantite importee", entrees, "rgba(16, 185, 129, 1)");
    drawLineChart("exportChart", "Quantite exportee", sorties, "rgba(244, 63, 94, 1)");

    window.addEventListener("resize", () => {
        drawLineChart("importChart", "Quantite importee", entrees, "rgba(16, 185, 129, 1)");
        drawLineChart("exportChart", "Quantite exportee", sorties, "rgba(244, 63, 94, 1)");
    });
});