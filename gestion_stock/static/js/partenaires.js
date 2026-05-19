function openModal() {
    const modal = document.getElementById("partnerModal");

    if (modal) {
        modal.style.display = "flex";
    }
}

function closeModal() {
    const modal = document.getElementById("partnerModal");

    if (modal) {
        modal.style.display = "none";
    }
}

function confirmDelete(typePartenaire) {
    return confirm(`Voulez-vous vraiment supprimer ${typePartenaire} ?`);
}

function normalizeText(value) {
    return (value || "")
        .toString()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase()
        .trim();
}

document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("partnerModal");
    const searchInput = document.getElementById("partnerSearch");
    const typeFilter = document.getElementById("partnerTypeFilter");
    const rows = Array.from(document.querySelectorAll(".partner-row"));
    const noResults = document.getElementById("noPartnerResults");

    function filterPartners() {
        const searchValue = normalizeText(searchInput ? searchInput.value : "");
        const typeValue = typeFilter ? typeFilter.value : "all";
        let visibleCount = 0;

        rows.forEach((row) => {
            const rowText = normalizeText(row.dataset.search);
            const rowType = row.dataset.type || "";
            const matchesSearch = !searchValue || rowText.includes(searchValue);
            const matchesType = typeValue === "all" || rowType === typeValue;
            const isVisible = matchesSearch && matchesType;

            row.style.display = isVisible ? "" : "none";

            if (isVisible) {
                visibleCount += 1;
            }
        });

        if (noResults) {
            noResults.style.display = visibleCount === 0 ? "table-row" : "none";
        }
    }

    if (searchInput) {
        searchInput.addEventListener("input", filterPartners);
    }

    if (typeFilter) {
        typeFilter.addEventListener("change", filterPartners);
    }

    window.addEventListener("click", (event) => {
        if (modal && event.target === modal) {
            closeModal();
        }
    });

    filterPartners();
});
