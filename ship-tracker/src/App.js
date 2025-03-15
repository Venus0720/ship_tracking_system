import React, { useEffect, useState } from "react";
import MapView from "@arcgis/core/views/MapView";
import WebMap from "@arcgis/core/WebMap";
import Graphic from "@arcgis/core/Graphic";
import Point from "@arcgis/core/geometry/Point";
import SimpleMarkerSymbol from "@arcgis/core/symbols/SimpleMarkerSymbol";
import TextSymbol from "@arcgis/core/symbols/TextSymbol";
import PopupTemplate from "@arcgis/core/PopupTemplate";

const App = () => {
  const [mapView, setMapView] = useState(null);

  useEffect(() => {
    // Create the ArcGIS map
    const webmap = new WebMap({
      basemap: "streets-navigation-vector",
    });

    const view = new MapView({
      container: "mapDiv",
      map: webmap,
      center: [0, 0],
      zoom: 2,
    });

    setMapView(view);
  }, []);

  useEffect(() => {
    if (!mapView) return;

    // Connect to WebSocket Server
    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onopen = () => {
      console.log("WebSocket connected!");
    };

    ws.onmessage = (event) => {
      const shipData = JSON.parse(event.data);
      console.log("WebSocket message received:", event.data);

      // Log the coordinates and all ship data to check if they're valid
      console.log(`Speed: ${shipData.speed}, Heading: ${shipData.heading}`);
      console.log(
        `Timestamp: ${new Date(shipData.timestamp * 1000).toLocaleString()}`
      );

      // Check if we have valid data
      if (shipData.longitude && shipData.latitude) {
        // Create ship marker
        const point = new Point({
          longitude: shipData.longitude,
          latitude: shipData.latitude,
        });

        const symbol = new SimpleMarkerSymbol({
          color: "black", // Marker color
          size: 6, // Marker size (increase size for better visibility)
        });

        const graphic = new Graphic({
          geometry: point,
          symbol: symbol,
        });

        // Create a custom popup template with ship information
        const popupTemplate = new PopupTemplate({
          title: `Ship ID: ${shipData.ship_id}`,
          content: `
            <b>Latitude:</b> ${shipData.latitude} <br/>
            <b>Longitude:</b> ${shipData.longitude} <br/>
            <b>Speed:</b> ${shipData.speed} knots <br/>
            <b>Heading:</b> ${shipData.heading}° <br/>
            <b>Timestamp:</b> ${new Date(
              shipData.timestamp * 1000
            ).toLocaleString()} <br/>
          `,
        });

        // Attach the popup template to the graphic
        graphic.popupTemplate = popupTemplate;

        // Add the graphic to the map
        mapView.graphics.add(graphic);

        // Create and add label for the ship ID (Optional)
        const textSymbol = new TextSymbol({
          text: `${shipData.ship_id} | ${shipData.latitude.toFixed(
            2
          )}° N, ${shipData.longitude.toFixed(2)}° E`, // Ship ID and coordinates
          color: "white", // Label color
          font: {
            size: 8,
            family: "Arial",
            weight: "bold",
          },
        });

        const labelGraphic = new Graphic({
          geometry: point,
          symbol: textSymbol,
        });

        mapView.graphics.add(labelGraphic);

        // Center the map on the ship's position and set zoom level
        mapView.center = [shipData.longitude, shipData.latitude];
        mapView.zoom = 5;
      } else {
        console.error("Invalid ship data:", shipData);
      }
    };

    // Close the WebSocket connection when the component is unmounted
    return () => ws.close();
  }, [mapView]);

  return <div id="mapDiv" style={{ width: "100%", height: "100vh" }}></div>;
};

export default App;
