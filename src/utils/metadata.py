# src/utils/metadata.py

from PIL import Image
from io import BytesIO
import exiftool
import os


def extract_exif_from_bytes(image_bytes):
    temp_path = "temp_exif_image.jpg"

    # Save bytes to temporary file
    with open(temp_path, 'wb') as f:
        f.write(image_bytes)

    # Extract metadata
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(temp_path)

    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)

    return metadata
