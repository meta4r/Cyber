import sys
from PyQt5 import QtWidgets, QtGui
import exifread

class MetadataExtractorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Metadata Extractor")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        
        self.label = QtWidgets.QLabel("Please select an image file:", self)
        self.label.move(20, 20)
        
        self.file_select_button = QtWidgets.QPushButton("Select File", self)
        self.file_select_button.move(20, 50)
        self.file_select_button.clicked.connect(self.selectFile)
        
        self.file_path_label = QtWidgets.QLabel("", self)
        self.file_path_label.move(120, 50)
        self.file_path_label.setFixedWidth(200)
        
        self.metadata_text_edit = QtWidgets.QTextEdit(self)
        self.metadata_text_edit.setReadOnly(True)
        self.metadata_text_edit.setGeometry(20, 100, 300, 400)
        
        self.show()
    
    def selectFile(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Image File", "", "Images (*.jpg *.jpeg *.png);;All Files (*)", options=options)
        if file_name:
            self.file_path_label.setText(file_name)
            metadata = extract_metadata(file_name)
            self.displayMetadata(metadata)
    
    def displayMetadata(self, metadata):
        if metadata:
            self.metadata_text_edit.clear()
            for metadata_field, metadata_value in metadata.items():
                self.metadata_text_edit.append(f"{metadata_field}: {metadata_value}")
        else:
            self.metadata_text_edit.setPlainText("No metadata extracted.")

def extract_metadata(image_file_path):
    try:
        with open(image_file_path, "rb") as image_file:
            image_data = image_file.read()
            tags = exifread.process_file(image_file)
    except FileNotFoundError:
        return None
    except:
        return None
    
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
    gps_latitude = tags.get("GPS GPSLatitude")
    gps_latitude_ref = tags.get("GPS GPSLatitudeRef")
    gps_longitude = tags.get("GPS GPSLongitude")
    gps_longitude_ref = tags.get("GPS GPSLongitudeRef")
    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        extracted_metadata["Geolocation"] = f"{gps_latitude.values} {gps_latitude_ref.values}, {gps_longitude.values} {gps_longitude_ref.values}"
    
    return extracted_metadata

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MetadataExtractorWindow()
    sys.exit(app.exec_())

