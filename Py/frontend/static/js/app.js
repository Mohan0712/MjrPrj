let currentLat = null, currentLon = null;

// Get GPS Location
function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        currentLat = pos.coords.latitude;
        currentLon = pos.coords.longitude;
        document.getElementById("locationStatus").innerText =
          `📍 Location Captured: ${currentLat.toFixed(5)}, ${currentLon.toFixed(5)}`;
      },
      (err) => {
        alert("❌ Error getting location: " + err.message);
      }
    );
  } else {
    alert("Geolocation not supported.");
  }
}

// Report Emergency
async function reportEmergency() {
  if (!currentLat || !currentLon) {
    alert("⚠️ Please capture location first!");
    return;
  }

  const payload = {
    latitude: currentLat,
    longitude: currentLon,
    type: document.getElementById("emergencyType").value,
    severity: document.getElementById("severity").value,
    description: document.getElementById("description").value,
  };

  try {
    const res = await fetch("/nearest-hospitals", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    if (data.success) {
      const hospitals = data.hospitals;
      const container = document.getElementById("hospitalsContainer");
      container.innerHTML = "";

      hospitals.forEach(h => {
        const card = `
          <div class="card p-4 shadow hover:shadow-lg transition rounded">
            <h4 class="font-bold text-lg">${h.name}</h4>
            <p class="text-sm text-gray-600">📍 ${h.latitude}, ${h.longitude}</p>
            <p class="text-sm text-gray-500">Distance: ${h.distance.toFixed(2)} km</p>
            <p class="text-sm text-green-600">Specialties: ${h.specialties__001 || "General"}</p>
            <button class="btn btn-outline-primary w-full mt-2">Select Hospital</button>
          </div>`;
        container.innerHTML += card;
      });

      document.getElementById("hospitalList").classList.remove("hidden");
    } else {
      alert("❌ Error: " + data.message);
    }
  } catch (err) {
    console.error("Error:", err);
  }
}
