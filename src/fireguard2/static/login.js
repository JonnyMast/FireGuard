document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
    });

    if (response.ok) {
        const data = await response.json();
        const token = data.access_token;
        localStorage.setItem("token", token);

        // Fetch the map page securely
        const secureResponse = await fetch("/fire_risk_map", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (secureResponse.ok) {
            const html = await secureResponse.text();

            // Update URL bar manually to reflect actual route
            history.pushState(null, "", "/fire_risk_map");

            document.open();
            document.write(html);
            document.close();
        } else {
            alert("Failed to load fire risk map.");
        }
    } else {
        alert("Login failed.");
    }
});
