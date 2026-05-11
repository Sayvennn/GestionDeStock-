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
