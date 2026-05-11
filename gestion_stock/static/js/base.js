document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("toggleSidebar");
    const sidebar = document.querySelector(".sidebar");
    const main = document.querySelector(".main-wrapper");

    if (toggleBtn && sidebar && main) {
        toggleBtn.addEventListener("click", () => {
            const isClosed = sidebar.classList.contains("sidebar-closed");

            if (isClosed) {
                sidebar.classList.remove("sidebar-closed");
                sidebar.style.width = "var(--sidebar-width)";
                sidebar.style.overflow = "visible";
                main.style.marginLeft = "var(--sidebar-width)";
                main.style.width = "calc(100% - var(--sidebar-width))";
            } else {
                sidebar.classList.add("sidebar-closed");
                sidebar.style.width = "0";
                sidebar.style.overflow = "hidden";
                main.style.marginLeft = "0";
                main.style.width = "100%";
            }
        });
    }

    if (window.location.pathname.includes("dashboard")) {
        setTimeout(() => {
            console.log("Bienvenue dans votre espace Premium.");
        }, 1000);
    }
});
