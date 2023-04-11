#Import Libraries
from rasterio.plot import show
from rasterio.merge import merge
import rasterio as rio
from pathlib import Path

#Create Output Path for Merged Data
path = Path('data/')
Path('output').mkdir(parents=True, exist_ok=True)
output_path = 'output/mosaic_output.tif'

#Iterate over Raster tifs in folder to create list of files for merge/mosaic
raster_files = list(path.iterdir())
raster_to_mosiac = []

#Loop through raster files, open with rasterio, append them to created raster_to_mosaic list
for p in raster_files:
    raster = rio.open(p)
    raster_to_mosiac.append(raster)

#Use merge method from rasterio to combine files
mosaic, output = merge(raster_to_mosiac)

#Copy rasters metadata to and update to match height/width of mosaic
output_meta = raster.meta.copy()
output_meta.update(
    {"driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": output,
    }
)

#Write mosaiced file in local folder
with rio.open(output_path, 'w', **output_meta) as m:
    m.write(mosaic)