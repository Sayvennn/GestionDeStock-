function normalizeStockText(value) {
    return (value || "")
        .toString()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase()
        .trim();
}

document.addEventListener("DOMContentLoaded", () => {
    const rows = Array.from(document.querySelectorAll(".stock-row"));
    const searchInput = document.getElementById("stockSearch");
    const statusFilter = document.getElementById("stockStatusFilter");
    const typeButtons = Array.from(document.querySelectorAll("[data-stock-type]"));
    const noResults = document.getElementById("noStockResults");
    let activeType = "all";

    rows.forEach((row, index) => {
        row.style.opacity = "0";
        row.style.transform = "translateY(10px)";
        row.style.transition = "0.3s ease";

        setTimeout(() => {
            row.style.opacity = "1";
            row.style.transform = "translateY(0)";
        }, index * 60);
    });

    function filterOperations() {
        const searchValue = normalizeStockText(searchInput ? searchInput.value : "");
        const statusValue = statusFilter ? statusFilter.value : "all";
        let visibleCount = 0;

        rows.forEach((row) => {
            const rowText = normalizeStockText(row.dataset.search);
            const rowType = row.dataset.type || "";
            const rowStatus = row.dataset.status || "";
            const matchesSearch = !searchValue || rowText.includes(searchValue);
            const matchesType = activeType === "all" || rowType === activeType;
            const matchesStatus = statusValue === "all" || rowStatus === statusValue;
            const isVisible = matchesSearch && matchesType && matchesStatus;

            row.style.display = isVisible ? "" : "none";

            if (isVisible) {
                visibleCount += 1;
            }
        });

        if (noResults) {
            noResults.style.display = visibleCount === 0 ? "table-row" : "none";
        }
    }

    typeButtons.forEach((button) => {
        button.addEventListener("click", () => {
            activeType = button.dataset.stockType || "all";
            typeButtons.forEach((item) => item.classList.remove("active"));
            button.classList.add("active");
            filterOperations();
        });
    });

    if (searchInput) {
        searchInput.addEventListener("input", filterOperations);
    }

    if (statusFilter) {
        statusFilter.addEventListener("change", filterOperations);
    }

    filterOperations();
});
