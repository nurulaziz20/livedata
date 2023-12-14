document.addEventListener('DOMContentLoaded', function () {
  // Initialize the Leaflet map
  const map = L.map('map').setView([-6.14534, 106.720995], 15); // Set the initial view to the first coordinates

  // Add a tile layer to the map (you can choose different tile layers)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

  // Create a marker for the user's position
  const marker = L.marker([0, 0]).addTo(map);

  // Create separate layer groups for flood-prone and non-flood-prone features
  const floodProneGroup = L.layerGroup();
  const nonFloodProneGroup = L.layerGroup();

  // Function to update the marker and coordinate display with the user's location
  function updateLocation(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    marker.setLatLng([latitude, longitude]);
    map.setView([latitude, longitude], 15);

    document.getElementById('coordinates').innerHTML = `Latitude: ${latitude.toFixed(6)}<br>Longitude: ${longitude.toFixed(6)}`;

    // Check if the user's location falls within any of the flood-prone or non-flood-prone polygons
    const userLocation = turf.point([longitude, latitude]);

    // Check if the user's location is in the flood-prone or non-flood-prone area
    const inFloodProneArea = turf.booleanPointInPolygon(userLocation, floodProneGroup.toGeoJSON());
    const inNonFloodProneArea = turf.booleanPointInPolygon(userLocation, nonFloodProneGroup.toGeoJSON());

    let message = "anda dilokasi "; // Default message if the location is not within any polygon

    if (inFloodProneArea) {
      message = "You are in a flood-prone area (Area Rawan Banjir)";
    } else if (inNonFloodProneArea) {
      message = "You are in a non-flood-prone area (Area Tidak Rawan Banjir)";
    }

    // Display the message using Bootstrap alert component
    const messageElement = document.getElementById('polygonMessage');
    messageElement.innerHTML = message;
    messageElement.className = inFloodProneArea ? "alert alert-danger" : inNonFloodProneArea ? "alert alert-success" : "alert alert-info";
    messageElement.style.display = "block";
  }

  // Function to handle errors when getting the user's location
  function errorHandler(err) {
    alert(`Error getting location: ${err.message}`);
  }

  // Function to generate the user's location and update the map
  function generateUserLocation() {
    // Check if geolocation is available in the browser
    if ('geolocation' in navigator) {
      // Get the user's current position and update the map
      navigator.geolocation.getCurrentPosition(updateLocation, errorHandler);
    } else {
      alert('Geolocation is not available in this browser.');
    }
  }

  // Handle the click event on the "Generate Coordinate" button
  const generateCoordinateBtn = document.getElementById('generateCoordinateBtn');
  generateCoordinateBtn.addEventListener('click', generateUserLocation);

  // Function to style the GeoJSON features based on the "FLOODPRONE" property
  function styleGeoJSON(feature) {
    const floodProne = feature.properties.FLOODPRONE;
    let fillColor = "green"; // Default color for non-flood-prone areas
    let layerGroup = nonFloodProneGroup;
    let borderWeight = 1; 

    if (floodProne === "YES") {
      fillColor = "red"; // Red color for flood-prone areas
      layerGroup = floodProneGroup;
      
    }

    const layer = L.geoJSON(feature, {
      style: {
        fillColor: fillColor,
        color: "black",
        weight: borderWeight,
        fillOpacity: 0.5
      },
      onEachFeature: onEachFeature // Add the popup for each feature
    });

    layerGroup.addLayer(layer);

    return layer;
  }

  // Function to create a popup with feature information
  function onEachFeature(feature, layer) {
    if (feature.properties) {
      const popupContent = `
        <b>Kabupaten/Kota:</b> ${feature.properties.KAB_NAME}<br>
        <b>Kecamatan:</b> ${feature.properties.KEC_NAME}<br>
        <b>Kelurahan:</b> ${feature.properties.KEL_NAME}<br>
        <b>RW:</b> ${feature.properties.RW}<br>
        <b>Rawan Banjir:</b> ${feature.properties.FLOODPRONE}
      `;

      layer.bindPopup(popupContent);
    }
  }

  // Load the GeoJSON data from the external file
  fetch('static/banjir.geojson') // Replace 'flood_data.geojson' with the path to your new GeoJSON file
    .then(response => response.json())
    
    .then(geojsonData => {
      // Add the GeoJSON features to their respective layer groups
      L.geoJSON(geojsonData, {
        style: styleGeoJSON
      }).addTo(map);

      // Add the layer groups to the map as overlays
      L.control.layers(null, {
        "Area Rawan Banjir": floodProneGroup,
        "Area Tidak Rawan Banjir": nonFloodProneGroup
      }).addTo(map);
    })
    .catch(error => {
      console.error('Error loading GeoJSON data:', error);
    });
});
