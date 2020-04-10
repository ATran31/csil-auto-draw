import json
from qgis.core import QgsVectorLayer, QgsExpression, QgsFeatureRequest


class Digitizer:
    """
    Handles drawing of CSIL segments.
    """

    def __init__(self, log_mile_data):
        self.Feature_Collection = {
            "type": "FeatureCollection",
            "name": "CSIL_Segments",
            "crs": {
                "type": "name",
                "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"},
            },
            "features": [],
        }

        # list of segment IDs that failed auto drawing
        self.Failed_Segments = []

        self.log_mile_ref = QgsVectorLayer(
            "c:/users/an.tran***REMOVED***/desktop/tfad/mdot_log_miles.gpkg|layername=mdot_log_miles",
            "Log Mile Reference",
            "ogr",
        )

    @staticmethod
    def get_route_prefix(route: str) -> str:
        return route[:2]

    @staticmethod
    def get_route_num(route: str) -> int:
        return int(route[2:6])

    @staticmethod
    def get_route_suffix(route: str) -> str:
        # query using 'MP_SUFFIX' field
        # all MP_SUFFIX values are a 2 char string
        # fields can be either one letter and a space or two letters e.g. 'E ' or 'AA'
        # empty fields use  two spaces instead of Null
        if len(route) > 6:
            suffix = route[6:]
            if len(suffix) == 1:
                # add a space if the suffix is only one letter
                return f"{suffix} "
            else:
                return suffix
        return "  "

    def draw_segment(self, segment: dict):
        """
        Draws a given CSIL segment based on the provided parameters.
        """
        # select all points that fall within the desired mp range and add to point
        # sort points by ID_MP in ascending order
        mp_start = segment["MP_START"]
        mp_end = segment["MP_END"]
        county_num = segment["COUNTY"]
        route_name = segment["ROUTE"]
        route_prefix = self.get_route_prefix(route_name)
        route_number = self.get_route_num(route_name)
        route_suffix = self.get_route_suffix(route_name)

        vertices = []
        # https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/vector.html#creating-vector-layersS

        exp = QgsExpression(
            f"ID_PREFIX = '{route_prefix}' and ID_RTE_NO = {route_number} and MP_SUFFIX = '{route_suffix}' and COUNTY = {county_num} and ID_MP >= {mp_start} and ID_MP <= {mp_end}"
        )

        selection = QgsFeatureRequest(exp)

        selected_mile_points = sorted(
            self.log_mile_ref.getFeatures(selection), key=lambda f: f["ID_MP"]
        )

        for feature in selected_mile_points:
            vertices.append([feature["LONGITUDE"], feature["LATITUDE"]])

        # add a comment indicating discrepancy between segment descriptiong and log mile data
        if (
            mp_start != selected_mile_points[0]["ID_MP"]
            or mp_end != selected_mile_points[-1]["ID_MP"]
        ):
            segment[
                "COMMENT"
            ] = "Segment log mile description and reference log mile data do not agree."

        # generate a geojson
        g = {
            "type": "Feature",
            "properties": segment,
            "geometry": {"type": "LineString", "coordinates": vertices},
        }

        # add to feature collection
        self.Feature_Collection["features"].append(g)

    def mark_failed_segment(self, segment_id: int):
        """
        Adds segment_id to the list of that could not be automatically drawn.
        """
        self.Failed_Segments.append(segment_id)

    def save_features(self, out_file: str):
        """
        Persists all drawn features to disk.
        """
        # write output to file
        with open(out_file, "w",) as geojson_file:
            json.dump(self.Feature_Collection, geojson_file)

    def save_errors(self, out_file: str):
        """
        Persists list of segment IDs that failed to draw to disk.
        """
        if len(self.Failed_Segments) > 0:
            with open(out_file, "w",) as fails:
                for f in self.Failed_Segments:
                    fails.write(f"{f}\n")
