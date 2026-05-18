# Seattle Parks Amenities Explorer

This project involves utilizing data from the city of Seattle's public park data. Taking specifically by these datasets. 

[Seattle Park General Data](https://data.seattle.gov/Community-and-Culture/Seattle-Parks-And-Recreation-Park-Addresses/v5tj-kqhc/about_data)\
[Seattle Park Features Data](https://data.seattle.gov/Community-and-Culture/Park-Features-By-PMAID/xrnu-8eiq/about_data)

With this explorer, you can use the map to hover over parks around the Seattle area and find what available amenities each park features.

## How to open the explorer

Click on this streamlit link: \
https://michaelgov-seattle-park-features-app-81fgqh.streamlit.app
### or 
Copy these lines of codes into your terminal to start the app.

>py -m venv .venv 

>.venv\Scripts\activate
 
>streamlit run app.py

## How to access API endpoints

[Watch The Video Here](https://youtu.be/8vuujcXPjyM)

>flask --app flask_get run -p 5002

>ngrok http http://localhost:5002

> Test via testapi.py and changing the URL