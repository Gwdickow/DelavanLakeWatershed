# DelavanLakeWatershed
Tax Parcel Based View of Properties under Land Management
Delavan Lake Watershed Tax Parcels — Source & Extraction Workbook							
							
Workbook created	2026-06-22						
Requested output	All tax parcels that lie inside the Delavan Lake Watershed boundary in Wisconsin.						
Status	Authoritative parcel and watershed data sources were identified and documented. The parcel rows are not populated because the working environment could not download ZIP/GeoJSON/JSON feature data from the GIS endpoints for spatial intersection.						
Recommended inclusion rule	Use Intersects as the default selection rule so parcels crossing the watershed boundary are included. For a stricter list, use Within to include only parcels wholly inside the boundary.						
Primary parcel source	Wisconsin Statewide Parcel Dataset V11 — Walworth County county extract, and/or Walworth County Tax Parcels REST layer.						
Primary watershed source	Walworth County GIS OneView Delavan Lake Watershed REST layer.						
Prepared for	Glenn Dickow						
							
How to use this workbook							
1	Open the Authoritative_Sources sheet for exact GIS sources and REST endpoints.						
2	Use the Extraction_Workflow sheet to reproduce the parcel selection in ArcGIS Pro, QGIS, or a Python GeoPandas environment with internet access.						
3	Populate Parcels_In_Watershed with the selected parcel records. Keep the source URL and selection rule columns for auditability.						
4	If you need parcels that only fully sit inside the watershed, change the spatial predicate from Intersects to Within before export.						
							
Important limitation							
I was able to verify the authoritative data layers but could not complete the spatial extraction inside this environment because direct downloads of the source ZIP and JSON/GeoJSON feature responses were blocked. This workbook therefore preserves the source-backed extraction setup rather than presenting an unverified parcel list.							
							
							
<img width="1671" height="693" alt="image" src="https://github.com/user-attachments/assets/9e3d86f7-977d-4213-aa0e-e8b9715699ad" />
