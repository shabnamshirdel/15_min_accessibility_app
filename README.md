# 🗺️ Accessibility Score Calculator Web Application

This is a Streamlit application designed to visualize and calculate an **15-minute Accessibility Score** for different senior housings based on the proximity and density of various key amenities.

Users can dynamically adjust the weight (importance) assigned to different amenity categories (like food, health, transport, etc.) and instantly see the resulting accessibility score reflected on an interactive map.

## ✨ Features

* **Interactive Map:** Displays geographical zones with a color-coded Choropleth map based on their calculated Accessibility Score.
* **Dynamic Weighting:** Uses a sidebar with sliders to allow real-time adjustment of weights for eight different amenity categories.
* **Data Normalization:** Normalizes all amenity counts to a 0-1 range before applying weights, ensuring a fair comparison between categories.
* **GeoData Integration:** Built on `geopandas` and `folium` to handle and visualize complex geographical data.

## ⚙️ Prerequisites

To run this application, you need to have **Python 3.7+** installed on your system.

### Required Files

Ensure the following files are in your project directory:

1.  `15_min_accessibility_app.py` (The main application script)
2.  `final_result.geojson` (The GeoJSON file containing the zonal boundaries and raw amenity count data. **This file is required to run the app.**)

## 💻 Local Installation and Setup

Follow these steps to set up and run the application on your local machine.

### 1. Clone or Download the Project

First, download the `15_min_accessibility_app.py` script and the required `final_result.geojson` file into a new project folder. 

Open the terminal and navigate to the newly created project folder.

### 2. Create a Virtual Environment (Recommended)

It's best practice to use a virtual environment to manage dependencies. In the terminal:

```bash
# Create the environment
python -m venv venv 

# Activate the environment (on macOS/Linux)
source venv/bin/activate

# Activate the environment (on Windows)
venv\Scripts\activate
```

### 3. Install Required Libraries

The application depends on several specific Python libraries. You can install them using pip. In the terminal:


```bash
pip install streamlit pandas geopandas folium streamlit-folium shapely
```


### 4. Run the Application

Once the dependencies are installed and your virtual environment is active, run the Streamlit app from your terminal using below command:

```bash
streamlit run 15_min_accessibility_app.py
```


### 5. Access the App

The command above will automatically open a new tab in your web browser, typically at the address: `http://localhost:8501`.

You can now interact with the sliders in the sidebar and observe the changes on the map.


