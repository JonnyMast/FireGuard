document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("loginForm");

  if (!form) {
    console.error("Error: loginForm not found!");
    return;
  }

  form.addEventListener("submit", async function (event) {
    event.preventDefault();

    console.log("✅ Login form submitted!");

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/Login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: `username=${encodeURIComponent(
        username
      )}&password=${encodeURIComponent(password)}`,
    });

    console.log("Received response from server");

    const result = await response.json();

    console.log("Parsed JSON response:", result);

    if (result.access_token) {
      console.log("✅ Token received, storing in localStorage...");
      localStorage.setItem("jwt", result.access_token);

      // ✅ Instead of redirecting, manually fetch fire_risk_map
      loadFireRiskMap();
    } else {
      console.log("Login failed:", result.detail);
      document.getElementById("message").innerText = result.detail;
    }
  });

  // ✅ Function to request fire_risk_map with Authorization header
  async function loadFireRiskMap() {
    const token = localStorage.getItem("jwt");

    if (!token) {
      console.warn("❌ No token found! Redirecting to login...");
      window.location.href = "/";
      return;
    }

    console.log("📌 Requesting /fire_risk_map with Authorization header...");

    const response = await fetch("/fire_risk_map", {
      method: "GET",
      headers: { Authorization: `Bearer ${token}` },
    });

    if (response.status === 200) {
      console.log("✅ Successfully authenticated! Redirecting...");
      window.location.href = "/fire_risk_map";
    } else {
      console.error("❌ Authentication failed! Redirecting to login...");
      window.location.href = "/";
    }
  }

  // ✅ Load stored token if available
  const storedToken = localStorage.getItem("jwt");
  if (storedToken) {
    console.log("✅ Token found in localStorage. Attempting to load map...");
    loadFireRiskMap();
  }
});
