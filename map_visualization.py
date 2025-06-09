import geopandas as gpd
import folium
import os
from folium.features import GeoJsonTooltip, GeoJsonPopup

geojson_folder = "G:/GIS/GeoJson"

geojson_files = [
    "State Boundary.geojson",
    "District Boudaries.geojson",
    "Gram Panchayath.geojson"
]

sample_gdf = gpd.read_file(os.path.join(geojson_folder, geojson_files[2]))
if sample_gdf.crs != "EPSG:4326":
    sample_gdf = sample_gdf.to_crs(epsg=4326)
center = [sample_gdf.geometry.centroid.y.mean(), sample_gdf.geometry.centroid.x.mean()]

m = folium.Map(location=center, zoom_start=12, tiles=None)
folium.TileLayer('OpenStreetMap', name='OpenStreetMap', control=True).add_to(m)

default_styles = {
    "State Boundary.geojson": {"color": "#aef0ae", "opacity": 0.1, "weight": 3},
    "District Boudaries.geojson": {"color": "#BCEEE3", "opacity": 0.1, "weight": 1.25},
    "Gram Panchayath.geojson": {"color": "#c59fe4", "opacity": 0.6, "weight": 1}
}

layer_names = []

for file in geojson_files:
    filepath = os.path.join(geojson_folder, file)
    gdf = gpd.read_file(filepath)
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs(epsg=4326)

    tooltip_fields = [f for f in ["Dist_Name", "State_Name", "GP Name"] if f in gdf.columns]
    tooltip = folium.GeoJsonTooltip(
        fields=tooltip_fields,
        aliases=[f"{field.replace('_', ' ')}:" for field in tooltip_fields],
        sticky=True,
        labels=True
    ) if tooltip_fields else None

    popup = folium.GeoJsonPopup(
        fields=tooltip_fields,
        aliases=[f"{field.replace('_', ' ')}:" for field in tooltip_fields]
    ) if tooltip_fields else None

    style = default_styles.get(file, {"color": "#8FE2C9", "opacity": 0.25, "weight": 0.7})
    layer_name = os.path.splitext(file)[0].replace(" ", "_")

    layer_names.append(layer_name)

    gj = folium.GeoJson(
        gdf,
        name=layer_name,
        tooltip=tooltip,
        popup=popup,
        style_function=lambda feature, col=style["color"], op=style["opacity"], w=style["weight"]: {
            'fillColor': col,
            'color': 'white',
            'weight': w,
            'fillOpacity': op
        }
    )
    gj.add_to(m)

folium.LayerControl().add_to(m)

color_picker_html = """
<div id="style-controls" style="position: fixed; top: 10px; right: 10px; z-index:9999; background: white; padding: 10px; border: 2px solid #ccc; max-width: 280px;">
<h4>Customize Layer Styles</h4>
<form id="styleForm">
  <!-- Will be filled by JS -->
</form>
</div>

<script>
  // List of layer names from Python (must match folium layer names)
  const layers = {% layer_names_json %};

  // Map folium layer names to actual Leaflet layers
  let leafletLayers = {};

  // Wait until map is loaded
  document.addEventListener('DOMContentLoaded', function() {
    // Find layers by name in the map
    layers.forEach(function(name) {
      leafletLayers[name] = null;
      map.eachLayer(function(layer) {
        if(layer.options && layer.options.name === name){
          leafletLayers[name] = layer;
        }
      });
    });

    // Build UI form inputs dynamically
    const form = document.getElementById('styleForm');
    layers.forEach(function(name) {
      form.insertAdjacentHTML('beforeend', `
        <div style="margin-bottom:10px;">
          <strong>${name.replace('_', ' ')}</strong><br/>
          Color: <input type="color" id="color_${name}" value="#000000" style="width:70px;"/>
          Opacity: <input type="range" id="opacity_${name}" min="0" max="1" step="0.05" value="0.5" style="width:100px;"/>
          Weight: <input type="number" id="weight_${name}" min="0" max="10" step="0.5" value="1" style="width:50px;"/>
        </div>
      `);

      // Set default values from Python passed styles
      const defaultStyles = {% default_styles_json %};
      if(defaultStyles[name]){
        document.getElementById(`color_${name}`).value = defaultStyles[name]['color'];
        document.getElementById(`opacity_${name}`).value = defaultStyles[name]['opacity'];
        document.getElementById(`weight_${name}`).value = defaultStyles[name]['weight'];
      }
    });

    // Listen for changes and update styles
    layers.forEach(function(name) {
      ['color', 'opacity', 'weight'].forEach(function(prop) {
        document.getElementById(`${prop}_${name}`).addEventListener('input', function(){
          updateLayerStyle(name);
        });
      });
    });

    function updateLayerStyle(name){
      let color = document.getElementById(`color_${name}`).value;
      let opacity = parseFloat(document.getElementById(`opacity_${name}`).value);
      let weight = parseFloat(document.getElementById(`weight_${name}`).value);

      let layer = leafletLayers[name];
      if(!layer) return;

      layer.setStyle({
        fillColor: color,
        fillOpacity: opacity,
        weight: weight,
        color: 'white'
      });
    }
  });
</script>
"""

import json
color_picker_html = color_picker_html.replace(
    '{% layer_names_json %}', json.dumps(layer_names)
).replace(
    '{% default_styles_json %}', json.dumps({
        name.replace(" ", "_"): v for name, v in zip(geojson_files, [default_styles[f] for f in geojson_files])
    })
)

m.get_root().html.add_child(folium.Element(color_picker_html))

folium.LayerControl().add_to(m)

output_path = "G:/GIS/GeoJson/Result_1.html"
m.save(output_path)
print(f"Map saved to: {output_path}")
