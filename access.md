# Seattle Park Amenities Explorer

## About

The Seattle Park Amenities Explorer is a web-based tool that helps users find Seattle parks by name, address, ZIP code, and available features. It is designed for Seattle residents, families, students, and visitors who want to quickly compare parks without reading raw city datasets. The system uses public data from the City of Seattle Open Data program and displays it through a Streamlit map connected to a Flask API.

## Methodology

- Two Seattle Open Data datasets were used: park addresses and park features.
- The datasets were connected using `pmaid`, the shared park identifier.
- The joined data was compiled into `parks_compiled.json`, where each park includes its basic information and feature list.
- A `features_index.json` file supports the feature filter.
- The Flask API loads these static JSON files when the server starts.
- The Streamlit app requests data from the API and displays it in a searchable map and table.
- The data can be maintained by refreshing the source datasets and recompiling the JSON files.

## Access

- Users open the Streamlit web app.
- The app connects to the Flask API to retrieve park data.
- Users can search by park name or address.
- Users can filter by ZIP code.
- Users can select one or more features to narrow results.
- The map and table update based on the selected filters.
- Users can hover over park points to view name, address, ZIP code, PMAID, and features.
- Users do not need to access the raw datasets directly.

## Structure

## Structure

Each API response returns a JSON array of park objects. Each park object contains location information, identifying fields, coordinates, and a list of connected features.

| Field | Type | Description |
|---|---:|---|
| `address` | String | Street address or location description of the park |
| `feature_count` | Integer | Number of listed features connected to the park |
| `features` | Array/List | List of amenities or features available at the park |
| `has_features` | Boolean | Indicates whether the park has one or more listed features |
| `location_1` | Object | Nested coordinate object containing latitude and longitude |
| `location_1.latitude` | String | Latitude value from the source dataset |
| `location_1.longitude` | String | Longitude value from the source dataset |
| `locid` | String | Location identifier from the park address dataset |
| `name` | String | Park name |
| `pmaid` | String | Unique park identifier used to connect park and feature data |
| `x_coord` | String / Float | Longitude used for mapping |
| `y_coord` | String / Float | Latitude used for mapping |
| `zip_code` | String | ZIP code where the park is located |

## Example

### Example Request

```http
GET /parks/zip/98119
```
### Example Response
```
[
  {
    "address": "1200 W Howe St",
    "feature_count": 1,
    "features": [
      "Play Area"
    ],
    "has_features": true,
    "location_1": {
      "latitude": "47.636097",
      "longitude": "-122.372985"
    },
    "locid": "2545",
    "name": "12th and Howe Play Park",
    "pmaid": "281",
    "x_coord": "-122.372985",
    "y_coord": "47.636097",
    "zip_code": "98119"
  }
]
```