document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("loginForm");

  if (!form) {
    console.log("[ERROR] loginForm not found");
    return;
  }

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    console.log("[AUTH] Processing login request");

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
      const response = await fetch("/Login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `username=${encodeURIComponent(
          username
        )}&password=${encodeURIComponent(password)}`,
      });

      const result = await response.json();
      console.log("[AUTH] Server response received");

      if (result.access_token) {
        console.log("[AUTH] Token received");
        localStorage.setItem("jwt", result.access_token);
        await loadMapContent(); // Load map content directly
      } else {
        console.log("[ERROR] Login failed:", result.detail);
        document.getElementById("message").innerText = result.detail;
      }
    } catch (error) {
      console.error("[ERROR] Login request failed:", error);
      document.getElementById("message").innerText =
        "Login failed. Please try again.";
    }
  });

  async function loadMapContent() {
    const token = localStorage.getItem("jwt");
    if (!token) {
      console.log("[AUTH] No token found");
      window.location.href = "/";
      return;
    }

    try {
      const response = await fetch("/fire_risk_map", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: "text/html",
        },
      });

      if (response.ok) {
        const content = await response.text();
        document.open();
        document.write(content);

        document.close();
        console.log("[SUCCESS] Map loaded");
      } else {
        console.log("[ERROR] Failed to load map");
        localStorage.removeItem("jwt");
        window.location.href = "/";
      }
    } catch (error) {
      console.error("[ERROR] Map request failed:", error);
      window.location.href = "/";
    }
  }
});
