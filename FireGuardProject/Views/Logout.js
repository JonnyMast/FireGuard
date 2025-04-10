document.addEventListener("DOMContentLoaded", function () {
  const logoutButton = document.getElementById("logoutButton");

  if (logoutButton) {
    logoutButton.addEventListener("click", function () {
      console.log("Logging out...");

      // Remove the token from localStorage
      localStorage.removeItem("jwt");

      // Redirect to login page
      window.location.href = "/";
    });
  } else {
    console.error("Logout button not found!");
  }
});
