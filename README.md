# 🗺️ GeoJSON Layer Visualization using Folium

This project is a Python-based interactive web map built with [Folium](https://python-visualization.github.io/folium/latest/), designed to load and display multiple GeoJSON layers with customized colors, tooltips, and popups. The project dynamically renders layers like **State Boundaries**, **District Boundaries**, and **Gram Panchayat** over a base map with styled front-end controls.

## 📁 Folder Structure

```
├── GeoJson/
│   ├── State Boundary.geojson
│   ├── District Boudaries.geojson
│   └── Gram Panchayath.geojson
├── map_visualization.py
└── README.md
```

## 🚀 Features

* Renders multiple GeoJSON layers with individual styling.
* Dynamic coloring for each layer.
* Interactive tooltips and popups for each feature.
* Layer control to toggle visibility.
* Simple integration with new GeoJSON files.

## 🛠️ Requirements

Install the dependencies using pip:

```bash
pip install geopandas folium branca
```

## 📌 How to Run

1. Place your `.geojson` files in the `GeoJson` folder.
2. Open and run `map_visualization.py` (or the corresponding script).
3. The generated map will be saved as an `HTML` file.
4. Open the map in your browser to explore.





