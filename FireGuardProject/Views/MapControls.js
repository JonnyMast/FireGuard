document.addEventListener("DOMContentLoaded", () => {
  const slider = document.getElementById("daysSlider");
  const daysValue = document.getElementById("daysValue");
  const updateButton = document.getElementById("updateButton");

  // Update display value when slider moves
  slider.addEventListener("input", () => {
    daysValue.textContent = `${slider.value} days`;
  });

  // Handle map update
  updateButton.addEventListener("click", async () => {
    const days = slider.value;
    const token = localStorage.getItem("jwt");

    try {
      const response = await fetch(`/fire_risk_map?num_days=${days}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        // Replace current page with updated map
        document.open();
        document.write(await response.text());
        document.close();
      } else {
        console.error("Failed to update map");
      }
    } catch (error) {
      console.error("Error updating map:", error);
    }
  });
});
