document.addEventListener("DOMContentLoaded", () => {
    console.log("Stock UI chargé.");

    const rows = document.querySelectorAll(".stock-row");

    rows.forEach((row, index) => {
        row.style.opacity = "0";
        row.style.transform = "translateY(10px)";
        row.style.transition = "0.3s ease";

        setTimeout(() => {
            row.style.opacity = "1";
            row.style.transform = "translateY(0)";
        }, index * 60);
    });
});
