document.addEventListener("DOMContentLoaded", () => {
    const rows = document.querySelectorAll(".catalogue-row, .product-row");

    rows.forEach((row, index) => {
        row.style.opacity = "0";
        row.style.transform = "translateY(15px)";
        row.style.transition = "all 0.4s cubic-bezier(0.4, 0, 0.2, 1)";

        setTimeout(() => {
            row.style.opacity = "1";
            row.style.transform = "translateY(0)";
        }, index * 80);
    });
});
