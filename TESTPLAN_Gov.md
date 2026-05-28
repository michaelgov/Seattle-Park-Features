# Seattle Parks Features Map and API – Test Plan

## Purpose

This document outlines the testing strategy for ensuring the quality, accuracy, accessibility, and performance of the Seattle Parks API and Streamlit map system. The test plan serves as a reference during development, deployment, and maintenance. It is intended to help ensure that users can reliably access park information, search for parks, filter by ZIP code, and view connected amenity data through the API and map interface.

---

## System Overview

- **Frontend / Interface**: Streamlit map application
- **Backend**: Flask API running locally or exposed through ngrok
- **Data Source**: Static JSON files loaded when the Flask server starts
  - `parks_compiled.json`: Seattle park records with park ID, name, address, ZIP code, coordinates, and connected features
  - `features_index.json`: Feature list/index used to support feature filtering
- **Shared Key**: `pmaid`
- **Main Purpose**: Provide API-based access to Seattle park records and connected amenity information

### Current Endpoints

- `GET /`: Confirms the API is running
- `GET /parks`: Returns all parks with connected features
- `GET /parks/<pmaid>`: Returns one park by park ID
- `GET /parks/zip/<zip_code>`: Returns parks within a specific ZIP code
- `GET /parks/feature/<feature_name>`: Returns parks that include a selected feature
- `GET /parks/<pmaid>/full`: Returns one park with its connected features
- `GET /search?q=<term>`: Searches parks by name or address
- `GET /features`: Returns available feature options for the Streamlit filter

---

## Test Objectives

- Ensure that all API endpoints return the correct data and status codes
- Verify that park records and amenity records are correctly connected through `pmaid`
- Ensure the Streamlit map loads API data correctly and displays valid coordinates
- Confirm that search and ZIP filtering return expected results

---

## Functional Testing

| Test Case | Description | Method | Expected Result |
|-----------|-------------|--------|-----------------|
| API Health Check | Visit root endpoint | Browser or `requests.get("/")` | Returns `"Seattle Parks API is running!"` with status 200 |
| Return All Parks | Call `GET /parks` | Browser, Postman, or Python requests | Returns a JSON list of park records |
| Search by Park ID | Call `GET /parks/390` | Browser or Python requests | Returns the park record for matching `pmaid` |
| Missing Park ID | Call `GET /parks/99999999` | Browser or Python requests | Returns 404 with `{"error": "Park not found"}` |
| Filter by ZIP Code | Call `GET /parks/zip/98144` | Browser or Python requests | Returns only parks with ZIP code `98144` |
| Search by Name | Call `GET /search?q=Pratt` | Browser or Python requests | Returns parks with name or address matching `Pratt` |
| Filter by Feature | Call `GET /parks/feature/Basketball` | Browser or Python requests | Returns parks that include a basketball-related feature |
| Connected Features | Call `GET /parks/390/full` | Browser or Python requests | Returns park data and connected feature information |
| Parks Without Features | Call `/parks` or `/parks/<pmaid>` for a park with no features | Manual test | `features` field returns `"None"` or an empty feature list is handled clearly |
| Streamlit API Connection | Run Streamlit app while Flask is running | Manual UI test | Map loads using API data rather than directly reading files |
| Streamlit Search | Search for a park name in Streamlit | UI test | Map and data table update to matching parks |
| Streamlit ZIP Filter | Enter a ZIP code in Streamlit | UI test | Map and data table show only parks from that ZIP code |
| Tooltip Display | Hover over map point | UI test | Tooltip shows park name, address, ZIP, park ID, and features |
| Empty Results | Search for a term that does not exist | UI test | App shows a clear “No parks found” message instead of crashing |

---

---

## Data Quality Checks

The main data quality goal is to make sure the API returns park records that are usable for search, filtering, and mapping. Because the system depends on static JSON files, these checks should be run whenever the JSON files are changed or recompiled.

| Check | What to Look For | Action if It Fails |
|-------|------------------|--------------------|
| Required fields | Each park should have `pmaid`, `name`, `address`, `zip_code`, `x_coord`, and `y_coord` | Fix the source record or document the missing field |
| Valid coordinates | `x_coord` and `y_coord` should convert into map coordinates | Drop the record from the map or correct the coordinate |
| Valid ZIP codes | ZIP codes should be present and formatted consistently | Clean the value or note it as missing |
| Feature field | Each park should include `features` or clearly return `None` | Recompile the JSON or review feature matching by `pmaid` |
| Empty results | Search, ZIP, or feature filters may return no parks | Show a clear message instead of crashing |

---

## Performance Checks

The system only needs to support a small class project demo, so performance testing can stay lightweight. The API should respond quickly enough for the Streamlit map to feel usable.

| Test | Target |
|------|--------|
| Flask starts successfully | No file path or JSON loading errors |
| `/parks` loads | Returns in about 2 seconds locally |
| Search, ZIP, and feature filters load | Returns in about 1 second locally |
| Streamlit map renders | Map appears without timeout or `KeyError` |
| ngrok access works | Public URL returns the same type of JSON as the local API |

---

## Alarms and Actions

For this project, monitoring will mainly happen through Flask terminal logs, Streamlit error messages, browser testing, and short `requests.get()` checks.

| Problem | Alarm / Signal | Action |
|---------|----------------|--------|
| API is not running | `/` does not return 200 | Restart Flask and check the terminal |
| Endpoint is missing | Browser shows 404 | Check the route spelling and restart Flask |
| Server error | Flask shows 500 or traceback | Read the error, check JSON fields, and fix the route |
| Map crashes | Streamlit shows a missing column error | Confirm the API response includes coordinates and features |
| Filter returns no data | Empty map or table | Check the search term, ZIP code, or feature value |
| ngrok link fails | Public URL no longer opens | Restart ngrok and update the URL in Streamlit |

---

## Continuous Testing & Maintenance

1. Start Flask and confirm `GET /` works.
2. Test `/parks`, `/search?q=Pratt`, `/parks/zip/98144`, and `/parks/feature/Basketball`.
3. Start Streamlit and confirm the map loads.
4. Try one search, one ZIP filter, and one feature filter.
5. Hover over a map point and confirm the tooltip shows name, address, ZIP, park ID, and features.
6. Check Flask logs for unexpected 404 or 500 errors.
7. If using ngrok, confirm the public URL works before recording the video.

---

## Status Summary

| Area | Status |
|------|--------|
| Flask API endpoints | Implemented and manually tested |
| Streamlit map | Implemented |
| Search by name/address | Implemented |
| ZIP code filter | Implemented |
| Feature filter | Implemented |
| Data quality checks | Manual checks planned |
| Performance testing | Basic local testing only |
| Monitoring | Manual logs and browser checks |

---

## Team Responsibilities

| Task | Owner |
|------|-------|
| Flask API testing | Michael |
| Streamlit map testing | Michael |
| Data quality review | Michael |
| Demo/video check | Michael |

---

## Future Improvements

- Add a route that lists all available routes for debugging.
- Add JSON validation for required fields.
- Improve feature filtering so users can combine search, ZIP code, and feature filters at the same time.
- Use a permanent deployment instead of ngrok if the project continues beyond the assignment.
