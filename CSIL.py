from qgis.core import QgsApplication
from segment_loader import load_segments
from segment_digitizer import Digitizer

"""
To run this script, launch the OSGEO4W64 Shell. Then call python-qgis-ltr <script-name>.py
This ensures that the script is called from the same version of Python that runs in the
QGIS Desktop console, and includes all the required dependencies and enviornment variables.
"""

# Supply path to qgis install location
QgsApplication.setPrefixPath("C:/OSGEO4~1/apps/qgis-ltr", True)

# Create a reference to the QgsApplication.  Setting the
# second argument to False disables the GUI.
qgs = QgsApplication([], False)

# Load providers
qgs.initQgis()

filename = "Test Data"
filepath = f"c:/users/an.tran***REMOVED***/desktop/tfad/source data/{filename}.xlsx"

segments = load_segments(filepath)

digitizer = Digitizer(
    log_mile_data="c:/users/an.tran***REMOVED***/desktop/tfad/mdot_log_miles.gpkg|layername=mdot_log_miles"
)

for segment in segments:
    try:
        digitizer.draw_segment(segment)
    except Exception as E:
        digitizer.mark_failed_segment(segment["SID"])
        continue


# write output to file
digitizer.save_features(
    f"c:/users/an.tran***REMOVED***/desktop/tfad/drawn_segments/{filename}_auto_draw.geojson"
)

# write failures to file
digitizer.save_errors(
    f"c:/users/an.tran***REMOVED***/desktop/tfad/drawn_segments/{filename}_auto_draw_FAILED.txt"
)

# Finally, exitQgis() is called to remove the
# provider and layer registries from memory

qgs.exitQgis()
