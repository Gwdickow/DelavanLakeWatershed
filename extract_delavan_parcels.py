import io
import zipfile
import tempfile
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests


OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

PARCEL_ZIP_URL = "https://web.s3.wisc.edu/parcels/v11_parcels/county/V1100_Wisconsin_Parcels_WALWORTH_SHP.zip"

WATERSHED_GEOJSON_URL = (
    "https://gisinfo.co.walworth.wi.us/arcgis/rest/services/"
    "OneView/WALCOZoning/MapServer/22/query"
    "?where=1%3D1&outFields=*&returnGeometry=true&f=geojson"
)


def download_walworth_parcels() -> gpd.GeoDataFrame:
    print("Downloading Walworth County parcel shapefile...")

    response = requests.get(PARCEL_ZIP_URL, timeout=180)
    response.raise_for_status()

    temp_dir = Path(tempfile.mkdtemp())

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
        zip_file.extractall(temp_dir)

    shapefiles = list(temp_dir.rglob("*.shp"))

    if not shapefiles:
        raise FileNotFoundError("No .shp file found in the downloaded parcel ZIP.")

    parcel_shp = shapefiles[0]
    print(f"Reading parcel shapefile: {parcel_shp}")

    parcels = gpd.read_file(parcel_shp)

    if parcels.empty:
        raise ValueError("Parcel file loaded, but it contains no records.")

    return parcels


def download_delavan_watershed() -> gpd.GeoDataFrame:
    print("Downloading Delavan Lake Watershed boundary...")

    watershed = gpd.read_file(WATERSHED_GEOJSON_URL)

    if watershed.empty:
        raise ValueError("Watershed layer loaded, but it contains no records.")

    return watershed


def main():
    parcels = download_walworth_parcels()
    watershed = download_delavan_watershed()

    print(f"Parcel records loaded: {len(parcels):,}")
    print(f"Watershed records loaded: {len(watershed):,}")

    # Make sure both layers use the same coordinate system.
    watershed = watershed.to_crs(parcels.crs)

    # Select parcels that touch or cross the Delavan Lake Watershed boundary.
    selected = gpd.sjoin(
        parcels,
        watershed[["geometry"]],
        predicate="intersects",
        how="inner",
    )

    selected = selected.drop(
        columns=[c for c in selected.columns if c.startswith("index_")],
        errors="ignore",
    )

    print(f"Parcels intersecting watershed: {len(selected):,}")

    preferred_columns = [
        "STATEID",
        "PARCELID",
        "TAXPARCELID",
        "OWNERNME1",
        "OWNERNME2",
        "SITEADRESS",
        "PSTLADRESS",
        "PROPCLASS",
        "LNDVALUE",
        "IMPVALUE",
        "ESTFMKVALUE",
        "GISACRES",
        "TAXROLLYEAR",
        "LATITUDE",
        "LONGITUDE",
    ]

    available_columns = [c for c in preferred_columns if c in selected.columns]

    output = selected[available_columns].copy()
    output.insert(0, "Selection_Rule", "Intersects Delavan Lake Watershed")

    output_file = OUTPUT_DIR / "delavan_lake_watershed_tax_parcels.xlsx"
    output.to_excel(output_file, index=False)

    print(f"Created output file: {output_file}")


if __name__ == "__main__":
    main()
