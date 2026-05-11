document.addEventListener("DOMContentLoaded", () => {
    const togglePassword = document.getElementById("togglePassword");
    const passwordInput = document.getElementById("id_password");
    const loginForm = document.getElementById("loginForm");
    const loginBtn = document.getElementById("loginBtn");

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener("click", () => {
            const isPassword = passwordInput.type === "password";
            passwordInput.type = isPassword ? "text" : "password";
            togglePassword.textContent = isPassword ? "Masquer" : "Afficher";
        });
    }

    if (loginForm && loginBtn) {
        loginForm.addEventListener("submit", () => {
            loginBtn.classList.add("loading");
            loginBtn.textContent = "Connexion...";
        });
    }
});
