import validatePassword from "./passwordValidator.js";

// Rest of your existing code...
// Add this password validation function at the top of your file

document.addEventListener("DOMContentLoaded", () => {
  const registerForm = document.getElementById("registerForm");

  // Add form validation feedback elements
  const passwordInput = document.getElementById("password");
  const confirmPasswordInput = document.getElementById("confirmPassword");

  // Create feedback element for password strength
  const passwordFeedback = document.createElement("div");
  passwordFeedback.className = "password-feedback";
  passwordInput.parentNode.appendChild(passwordFeedback);

  // Real-time password validation
  function validatePasswordInput() {
    const validation = validatePassword(passwordInput.value);

    if (!validation.isValid) {
      passwordFeedback.innerHTML = validation.errors
        .map((error) => `<div class="error-message">${error}</div>`)
        .join("");
    } else {
      passwordFeedback.innerHTML =
        '<div class="success-message">Strong password</div>';
    }
  }

  // Add the event listener that calls the function
  passwordInput.addEventListener("input", validatePasswordInput);

  // Trigger validation on page load
  validatePasswordInput();

  // Visual password match validation
  confirmPasswordInput.addEventListener("input", () => {
    if (passwordInput.value !== confirmPasswordInput.value) {
      confirmPasswordInput.setCustomValidity("Passwords don't match");
    } else {
      confirmPasswordInput.setCustomValidity("");
    }
  });

  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Get form values
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    // Validate password strength before submission
    const validation = validatePassword(password);
    if (!validation.isValid) {
      alert(validation.errors.join("\n"));
      return;
    }

    // Check if passwords match
    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }

    // Disable form submission while processing
    const submitButton = registerForm.querySelector("button[type='submit']");
    submitButton.disabled = true;
    submitButton.textContent = "Registering...";

    try {
      // Send registration request to backend
      const response = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Registration failed");
      }

      const data = await response.json();

      // If registration successful, redirect to login page
      alert("Registration successful! Please log in.");
      window.location.href = "login.html";
    } catch (error) {
      console.error("Registration error:", error);
      alert(`Registration failed: ${error.message}`);

      // Re-enable the submit button on error
      submitButton.disabled = false;
      submitButton.textContent = "Register";
    }
  });
});
