// Modal de confirmación para eliminar rodada
const deleteModal = document.getElementById("delete-roadtrip-modal");
const deleteRoadtripNameEl = document.getElementById("delete-roadtrip-name");
const deleteRoadtripIdInput = document.getElementById("delete-roadtrip-id");

document.querySelectorAll("[data-open-delete-modal]").forEach((btnEl) => {
    btnEl.addEventListener("click", () => {
        if (!deleteModal) return;

        const roadtripId = btnEl.getAttribute("data-roadtrip-id") || "";
        const roadtripName = btnEl.getAttribute("data-roadtrip-name") || "";

        if (deleteRoadtripNameEl) {
            deleteRoadtripNameEl.textContent = roadtripName;
        }

        if (deleteRoadtripIdInput) {
            deleteRoadtripIdInput.value = roadtripId;
        }

        deleteModal.classList.add("show");
        deleteModal.setAttribute("aria-hidden", "false");
    });
});

document.querySelectorAll("[data-close-delete-modal]").forEach((btnEl) => {
    btnEl.addEventListener("click", () => {
        if (!deleteModal) return;

        deleteModal.classList.remove("show");
        deleteModal.setAttribute("aria-hidden", "true");
    });
});

// Contador de caracteres del nombre de la rodada (máximo 120)
const displayNameInput = document.getElementById("roadtrip-display_name-field");
const displayNameCounter = document.getElementById("display-name-counter");

if (displayNameInput && displayNameCounter) {
    const updateCounter = () => {
        const length = displayNameInput.value.length;
        displayNameCounter.textContent = `${length} / 120`;
    };
    displayNameInput.addEventListener("input", updateCounter);
    updateCounter();
}

// Sincronización de fecha (calendario) y hora (reloj) -> ISO start_at
const dateInput = document.getElementById("roadtrip-start_date-field");
const timeInput = document.getElementById("roadtrip-start_time-field");
const startAtHiddenInput = document.getElementById("roadtrip-start_at-field");

if (dateInput && timeInput && startAtHiddenInput) {
    const syncStartAt = () => {
        if (dateInput.value && timeInput.value) {
            startAtHiddenInput.value = `${dateInput.value}T${timeInput.value}`;
        }
    };

    [dateInput, timeInput].forEach((el) => {
        el.addEventListener("input", syncStartAt);
        el.addEventListener("change", syncStartAt);
    });
}

// Selectores de ubicación con OpenStreetMap (Leaflet + Nominatim)
function initOsmLocationPicker(config) {
    const mapContainer = document.getElementById(config.mapElementId);
    if (!mapContainer || typeof L === "undefined") return;

    const nameInput = document.getElementById(config.nameInputId);
    const latInput = document.getElementById(config.latInputId);
    const lngInput = document.getElementById(config.lngInputId);
    const searchInput = document.getElementById(config.searchInputId);
    const searchBtn = document.getElementById(config.searchBtnId);

    // Coordenadas por defecto (Medellín, Antioquia)
    const defaultLat = 6.2442;
    const defaultLng = -75.5812;

    const existingLat = parseFloat(latInput?.value);
    const existingLng = parseFloat(lngInput?.value);
    const hasInitialCoords = !Number.isNaN(existingLat) && !Number.isNaN(existingLng);

    const initialLat = hasInitialCoords ? existingLat : defaultLat;
    const initialLng = hasInitialCoords ? existingLng : defaultLng;

    const map = L.map(config.mapElementId).setView([initialLat, initialLng], hasInitialCoords ? 15 : 12);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        maxZoom: 19,
    }).addTo(map);

    let marker = null;

    const updateCoordinatesInputs = (lat, lng) => {
        if (latInput) latInput.value = Number(lat).toFixed(6);
        if (lngInput) lngInput.value = Number(lng).toFixed(6);
    };

    const reverseGeocode = async (lat, lng) => {
        try {
            const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${encodeURIComponent(lat)}&lon=${encodeURIComponent(lng)}&accept-language=es`;

            const response = await fetch(url, {
                headers: { Accept: "application/json" },
            });
            if (!response.ok) return;

            const data = await response.json();
            if (data && data.display_name && nameInput) {
                nameInput.value = data.name || data.display_name.split(",").slice(0, 3).join(",").trim();
            }
        } catch (err) {
            console.warn("No se pudo obtener el nombre de la ubicación desde OSM:", err);
        }
    };

    const setMarkerPosition = (lat, lng, shouldReverseGeocode = true) => {
        updateCoordinatesInputs(lat, lng);

        if (!marker) {
            marker = L.marker([lat, lng], { draggable: true }).addTo(map);
            marker.on("dragend", (event) => {
                const pos = event.target.getLatLng();
                updateCoordinatesInputs(pos.lat, pos.lng);
                reverseGeocode(pos.lat, pos.lng);
            });
        } else {
            marker.setLatLng([lat, lng]);
        }

        if (shouldReverseGeocode) {
            reverseGeocode(lat, lng);
        }
    };

    if (hasInitialCoords) {
        setMarkerPosition(initialLat, initialLng, false);
    }

    map.on("click", (event) => {
        const { lat, lng } = event.latlng;
        setMarkerPosition(lat, lng, true);
    });

    const searchLocation = async () => {
        const query = searchInput?.value?.trim();
        if (!query) return;

        try {
            const url = `https://nominatim.openstreetmap.org/search?format=jsonv2&q=${encodeURIComponent(query)}&limit=1&accept-language=es`;

            const response = await fetch(url, { headers: { Accept: "application/json" } });
            if (!response.ok) return;

            const results = await response.json();
            if (Array.isArray(results) && results.length > 0) {
                const place = results[0];
                const lat = parseFloat(place.lat);
                const lng = parseFloat(place.lon);

                map.setView([lat, lng], 15);
                setMarkerPosition(lat, lng, false);

                if (nameInput) {
                    nameInput.value = place.name || place.display_name.split(",").slice(0, 3).join(",").trim();
                }
            }
        } catch (err) {
            console.warn("Error buscando ubicación en OSM:", err);
        }
    };

    if (searchBtn) {
        searchBtn.addEventListener("click", searchLocation);
    }

    if (searchInput) {
        searchInput.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                searchLocation();
            }
        });
    }
}

initOsmLocationPicker({
    mapElementId: "start-map",
    nameInputId: "roadtrip-start_location_name-field",
    latInputId: "roadtrip-start_latitude-field",
    lngInputId: "roadtrip-start_longitude-field",
    searchInputId: "start-map-search-input",
    searchBtnId: "start-map-search-btn",
});

initOsmLocationPicker({
    mapElementId: "end-map",
    nameInputId: "roadtrip-end_location_name-field",
    latInputId: "roadtrip-end_latitude-field",
    lngInputId: "roadtrip-end_longitude-field",
    searchInputId: "end-map-search-input",
    searchBtnId: "end-map-search-btn",
});
