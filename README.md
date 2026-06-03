# Seattle Parks Features Explorer

This project uses public park data from the City of Seattle to create an interactive park feature explorer. The app combines general park information with park feature data so users can search for parks, filter by ZIP code, and explore available amenities through an interactive map.

### Data sources:
[Seattle Park General Data](https://data.seattle.gov/Community-and-Culture/Seattle-Parks-And-Recreation-Park-Addresses/v5tj-kqhc/about_data)  
[Seattle Park Features Data](https://data.seattle.gov/Community-and-Culture/Park-Features-By-PMAID/xrnu-8eiq/about_data)


With this explorer, users can hover over parks around Seattle and view information such as park name, address, ZIP code, PMA ID, and available features or amenities.

## FAIR Principles

This project supports FAIR by making Seattle parks data easier to find, access, connect, and reuse. **(F)** Park records use `pmaid` as a shared identifier between location and feature data. **(A)** The data is retrievable through Flask API endpoints and public Seattle Open Data sources. **(I)** The structure uses JSON, a shared and readable format for web applications and APIs. **(R)** Each compiled park record includes useful attributes such as name, address, ZIP code, coordinates, and features, making the data reusable for future park discovery tools.

## How to open the explorer

#### 1. Access API for Improved Information Structure

[Watch The Video Here](https://youtu.be/8vuujcXPjyM)
```
flask --app endpoint run -p 5002
ngrok http http://localhost:5002
```
Test via endpoint.py and changing the URLs


### 2. Two Options:
#### Click on this streamlit link: 
https://michaelgov-seattle-park-features-app-81fgqh.streamlit.app
### or

### Run Locally

To run the app locally, use the following commands in your terminal:

```bash
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
