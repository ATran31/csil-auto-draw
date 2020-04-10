from openpyxl import load_workbook


def load_segments(in_file: str) -> list:
    """
    Parses an Excel file for CSIL segment definitions and returns a list of dicts.
    """
    wb = load_workbook(filename=in_file, read_only=True,)

    ws = wb.active

    segments = []

    for row in ws.rows:
        if row[0].value == "SID":
            # skip the first row of headers
            continue

        attrs = [
            "SID",
            "YEAR",
            "DISTRICT",
            "COUNTY",
            "MUNI",
            "ROUTE",
            "MP_START",
            "MP_END",
            "TOTAL_ACCIDENTS",
            "CONTROL_TYPE",
            "CSIS",
            "SEVERITY_INDEX",
        ]

        d = {}

        for attr in attrs:
            d[attr] = row[attrs.index(attr)].value

        segments.append(d)

    return segments
