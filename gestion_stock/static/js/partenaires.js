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

window.addEventListener("click", (event) => {
    const modal = document.getElementById("partnerModal");

    if (modal && event.target === modal) {
        closeModal();
    }
    document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("partnerSearch");
    const typeFilter = document.getElementById("partnerTypeFilter");
    const rows = document.querySelectorAll(".partner-row");

    function filterPartners() {
        const searchValue = searchInput ? searchInput.value.toLowerCase().trim() : "";
        const typeValue = typeFilter ? typeFilter.value : "all";

        rows.forEach((row) => {
            const rowText = (row.dataset.search || "").toLowerCase();
            const rowType = row.dataset.type || "";

            const matchesSearch = rowText.includes(searchValue);
            const matchesType = typeValue === "all" || rowType === typeValue;

            row.style.display = matchesSearch && matchesType ? "" : "none";
        });
    }

    if (searchInput) {
        searchInput.addEventListener("input", filterPartners);
    }

    if (typeFilter) {
        typeFilter.addEventListener("change", filterPartners);
    }
});
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

window.addEventListener("click", (event) => {
    const modal = document.getElementById("partnerModal");

    if (modal && event.target === modal) {
        closeModal();
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("partnerSearch");
    const typeFilter = document.getElementById("partnerTypeFilter");
    const rows = document.querySelectorAll(".partner-row");
    const noResults = document.getElementById("noPartnerResults");

    function filterPartners() {
        const searchValue = searchInput ? searchInput.value.toLowerCase().trim() : "";
        const typeValue = typeFilter ? typeFilter.value : "all";
        let visibleCount = 0;

        rows.forEach((row) => {
            const rowText = (row.dataset.search || "").toLowerCase();
            const rowType = row.dataset.type || "";

            const matchesSearch = rowText.includes(searchValue);
            const matchesType = typeValue === "all" || rowType === typeValue;

            if (matchesSearch && matchesType) {
                row.style.display = "";
                visibleCount += 1;
            } else {
                row.style.display = "none";
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

    filterPartners();
});


});
