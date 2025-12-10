import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from folium import Choropleth
from streamlit_folium import folium_static
from shapely.geometry import Polygon, MultiPolygon

# --- Streamlit Page Configuration (Must be the first Streamlit command) ---
st.set_page_config(
    page_title="City Accessibility Score Calculator",
    layout="wide", # Use wide layout for better map visibility
    initial_sidebar_state="expanded"
)

st.title('🗺️ City Accessibility Score Calculator')
st.markdown("""
This application calculates an **15-minutes Accessibility Score** for different senior housings across Island of Montreal based on a weighted combination of various amenities. Adjust the weights in the  sidebar to see how the score and the map visualization change in real-time.
""")

# --- Data Loading (Assuming 'final_result.geojson' is available) ---
# Note: For deployment, ensure the GeoJSON file path is correct.
try:
    final_result = gpd.read_file('./final_result.geojson')
except Exception as e:
    st.error(f"Could not load GeoJSON file: {e}")
    st.stop()


if isinstance(final_result['geometry'].iloc[0], str):
    from shapely import wkt
    final_result['geometry'] = final_result['geometry'].apply(wkt.loads)

gdf = gpd.GeoDataFrame(final_result, geometry='geometry')


# --- Sidebar for Inputs (Improved UI) ---
with st.sidebar:
    st.header("⚖️ Weight Adjustments")
    st.markdown("Adjust the importance of each factor (0-100).")
    
    # Use a container or expander for better organization
    with st.expander("Adjust Amenity Weights", expanded=True):
        # Weight sliders
        amenity_weight = st.slider('Amenity', 0, 100, 20)
        bank_weight = st.slider('Bank', 0, 100, 20)
        food_weight = st.slider('Food', 0, 100, 20)
        health_weight = st.slider('Health center', 0, 100, 20)
        shop_weight = st.slider('Shop', 0, 100, 20)
        sport_weight = st.slider('Sport center', 0, 100, 20)
        transport_weight = st.slider('Transportation', 0, 100, 20)
        greenary_weight = st.slider('Greenery (Not used in calculation yet)', 0, 100, 0) # Added note since greenary isn't used

    st.markdown("---")
    st.info("The map will update automatically when you change the weights.")


# --- Calculation of Accessibility Score ---
weights = {
    'amenity': amenity_weight,
    'bank': bank_weight,
    'food': food_weight,
    'health': health_weight,
    'shop': shop_weight,
    'sport': sport_weight,
    'transport': transport_weight,
    'greenary': greenary_weight # Included, though not used in the score formula below
}

# Normalize weights to sum to 1
# IMPORTANT: Only sum the weights that are actually used in the calculation
used_weights = {k: weights[k] for k in ['amenity', 'bank', 'food', 'health', 'shop', 'sport', 'transport']}
total_weight = sum(used_weights.values())

# Handle the case where all used weights are 0 to prevent division by zero
if total_weight == 0:
    st.warning("All weights for the score calculation are currently set to 0. Please adjust the sliders.")
    # Set a default score or skip calculation if desired, here we just show 0
    gdf['accessibility_score'] = 0.0
else:
    normalized_weights = {key: value / total_weight for key, value in used_weights.items()}

    # Normalize each attribute to the range [0, 1]
    for col in used_weights.keys():
        col_min = gdf[col].min()
        col_max = gdf[col].max()
        if col_max == col_min:
            gdf[col + '_norm'] = 0.0 # Avoid division by zero if all values are the same
        else:
            gdf[col + '_norm'] = (gdf[col] - col_min) / (col_max - col_min)

    # Calculate the accessibility score out of 100
    gdf['accessibility_score'] = (
        gdf['amenity_norm'] * normalized_weights['amenity'] +
        gdf['bank_norm'] * normalized_weights['bank'] +
        gdf['food_norm'] * normalized_weights['food'] +
        gdf['health_norm'] * normalized_weights['health'] +
        gdf['shop_norm'] * normalized_weights['shop'] +
        gdf['sport_norm'] * normalized_weights['sport'] +
        gdf['transport_norm'] * normalized_weights['transport']
    ) * 100

# --- Map Visualization (Main Area) ---

# Use st.container for a clean main section
with st.container():
    st.subheader("Map Visualization: Accessibility Score by Zone")
    
    # Check if the dataframe is empty or missing required data
    if gdf.empty or 'accessibility_score' not in gdf.columns:
        st.error("No data available for mapping or score calculation failed.")
    else:
        # Create a Folium map
        # Use the mean centroid for a more dynamic initial map location
        mean_lat = gdf['geometry'].centroid.y.mean()
        mean_lon = gdf['geometry'].centroid.x.mean()
        
        m = folium.Map(location=[mean_lat, mean_lon], zoom_start=11, tiles='cartodb positron')

        # Add polygons with accessibility scores using a better color scheme
        Choropleth(
            geo_data=gdf,
            data=gdf,
            columns=['title', 'accessibility_score'],
            key_on='feature.properties.title',
            fill_color='RdYlGn', # A more professional-looking divergent color scale (Red-Yellow-Green)
            fill_opacity=0.8,
            line_opacity=0.3,
            legend_name='Accessibility Score (0-100)',
            highlight=True # Highlights the area on hover
        ).add_to(m)
        
        # Add a tooltip for score on hover (more interactive than static markers)
        style_function = lambda x: {'fillColor': '#ffffff', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.1, 
                                    'weight': 0.1}
        highlight_function = lambda x: {'fillColor': '#000000', 
                                        'color':'#000000', 
                                        'fillOpacity': 0.50, 
                                        'weight': 0.1}
        
        # Custom tooltip for GeoJSON layer
        folium.features.GeoJson(
            gdf,
            name='Accessibility Scores',
            style_function=style_function, 
            highlight_function=highlight_function,
            tooltip=folium.features.GeoJsonTooltip(
                fields=['title', 'accessibility_score'],
                aliases=['Zone:', 'Score:'],
                localize=True,
                sticky=False,
                labels=True,
                style="""
                    background-color: #F0EFEF;
                    border: 2px solid grey;
                    border-radius: 3px;
                    box-shadow: 3px;
                """
            )
        ).add_to(m)

        # Display the map in Streamlit
        # Removed the two-column layout as the sidebar handles the input
        folium_static(m, width=1000, height=600) # Explicitly setting size for consistency

    st.markdown("---")
    st.caption("Data is normalized between 0 and 1 before applying weights. Score is calculated out of 100.")