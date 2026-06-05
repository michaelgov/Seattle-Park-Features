# Data Quality
According to Wang and Strong (1996), high-quality data should be intrinsically good,
contextually appropriate for the task, clearly represented, and accessible to the consumer. With the new structure, the project aims to make park data more accessible to consumers who want to explore around the Seattle area. This new integrated structure utilizes PMAID as a shared key between the Seattle Parks & Recreation Addresses dataset and the Seattle Park Features dataset, which allows the data and metadata of parks to be centralized in a single structure to be fully represented. This becomes easier to identify missing feature values and validate whether parks contain expected data such as coordinates and addresses. The JSON structure also supports hierarchical organization, making it easier to automate quality checks and detect malformed or incomplete records. Instead of storing park location and feature information in two separate data structures, each park record now contains its metadata, location fields, and a nested features list within one object, which improves clarity and usability preserves source metadata such as update
timestamps and original row IDs for future auditing and quality tracking.

# Information Security
For information security, the integrated structure makes it easier to track and manage changes because park information is stored in one standardized JSON format instead of separate structures. By preserving IDs and timestamps of updates, the structure supports auditing and helps identify outdated, missing, or unexpectedly changed records. As noted by the article by Exabeam, effective information security policies should “protect against vectors threatening data integrity, availability, and confidentiality.” The integrated structure supports this by making park data easier to validate, monitor, and manage through standardized fields and centralized records that are integrated as one.

## Existing Data Structure
### Seattle Parks & Recreation Addresses Example
```
{
    ":id": "row-4s2t~hkn2~jdqb",
    ":version": "rv-kdqp~twc4.bw38",
    ":created_at": "2024-05-29T20:55:28.891Z",
    ":updated_at": "2024-05-29T20:55:28.891Z",
    "pmaid": "281",
    "locid": "2545",
    "name": "12th and Howe Play Park",
    "address": "1200 W Howe St",
    "zip_code": "98119",
    "x_coord": "-122.372985",
    "y_coord": "47.636097",
    "location_1": {
        "latitude": 47.636097,
        "longitude": -122.372985
    }
}
```
### Seattle Park Features by PMAID Example
```
{
    ":id": "row-2qb2_npft~n5jp",
    ":version": "rv-bg8u_emue_xw6z",
    ":created_at": "2024-10-04T16:55:14.767Z",
    ":updated_at": "2024-10-04T16:55:14.767Z",
    "service_layer_id": "0",
    "feature_desc": "Adult Fitness Equipment",
    "pmaid": "345"
}
```

### Reformatted
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