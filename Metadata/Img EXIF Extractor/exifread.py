import exifread

def extract_metadata(image_file_path):
    try:
        with open(image_file_path, "rb") as image_file:
            image_data = image_file.read()
            tags = exifread.process_file(image_file)
    except FileNotFoundError:
        print(f"Error: Image file '{image_file_path}' not found.")
        return
    except:
        print(f"Error: Unable to process image file '{image_file_path}'.")
        return
    
    extracted_metadata = {}
    
    # Extract make and model information
    make = tags.get("Image Make")
    model = tags.get("Image Model")
    if make and model:
        extracted_metadata["Make"] = make.values
        extracted_metadata["Model"] = model.values
    
    # Extract operating system information
    software = tags.get("Image Software")
    if software:
        extracted_metadata["Operating System"] = software.values
    
    # Extract software information
    software = tags.get("Image Software")
    if software:
        extracted_metadata["Software"] = software.values
    
    # Extract geolocation information
    latitude = tags.get("GPS GPSLatitude")
    latitude_ref = tags.get("GPS GPSLatitudeRef")
    longitude = tags.get("GPS GPSLongitude")
    longitude_ref = tags.get("GPS GPSLongitudeRef")
    if latitude and latitude_ref and longitude and longitude_ref:
        lat_value = convert_to_degrees(latitude.values)
        if latitude_ref.values == "S":
            lat_value = -lat_value
        lon_value = convert_to_degrees(longitude.values)
        if longitude_ref.values == "W":
            lon_value = -lon_value
        extracted_metadata["Geolocation"] = (lat_value, lon_value)
    
    return extracted_metadata

def convert_to_degrees(values):
    d = values[0].num
    m = values[1].num
    s = values[2].num
    return d + (m / 60.0) + (s / 3600.0)

image_file_path = "image.jpg"
metadata = extract_metadata(image_file_path)

if metadata:
    print("Metadata:")
    for metadata_field, metadata_value in metadata.items():
        print(f"{metadata_field}: {metadata_value}")
else:
    print("No metadata extracted.")
