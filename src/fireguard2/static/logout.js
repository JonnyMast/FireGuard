document.addEventListener("DOMContentLoaded", function () {
    const logoutButton = document.getElementById("logoutButton");

    if (logoutButton) {
        logoutButton.addEventListener("click", function () {
            localStorage.removeItem("jwt");
            window.location.href = "/";
        });
    } else {
        console.error("Logout button not found!");
    }
});