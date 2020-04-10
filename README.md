# CSIL Auto Draw

This program automates drawing of Candidate Safety Improvement Locations (CSIL) segments based on a set of reference log mile points.

## Quick Start

1. Call `python-qgis-ltr CSIL.py` from the command line.

   - The `python-qgis-ltr` maps to a `.bat` file with the same name which sets all the environment variables required to make use of QGIS components. It is usually found at _C:\OSGeo4W64\bin_

2. It is also possible to call the same script from within the VSCode terminal or Code Runner extension by adding the configuration settings found in `.vscode/settings.json`.

**Do not try to call `python CSIL.py` directly to execute this program. This will result in various module and DLL import errors even if your PYTHONPATH is pointing to the QGIS Python interpreter.**

## Requirements

- [QGIS](https://qgis.org/en/site/forusers/download.html) must be installed on the executing machine.
- [OpenPyXL](https://openpyxl.readthedocs.io/en/stable/).

  **Dependencies should be installed to the QGIS version of Python**. Typically at _C:\OSGeo4W64\apps\Python37\lib\site-packages_

  1. Open the OSGEOW4 Shell
  2. Set appropriate QGIS Python 3 environment: `py3_env`
  3. Install the package: `pip install openpyxl`
  4. Confirm it has installed: `pip list`

## How it works

This program parses an input Excel file that defines one or more CSIL segments.
For each segment, it will execute a selection against the `mdot_log_mile.gpkg` dataset to find log mile points that match the route prefix, route number, route suffix and mile post range for that segment. The segment is then drawn using each selected log mile point's coordinates as a vertex of the line feature.

#### Drawing order

Segments are drawn South -> North and West -> East in ascending log mile order.

#### Error Handling

In some cases, there will be mismatch between the described segment's log mile post range and the results of the select operation. For example, a segment may be described as being between mile post 2.53 and 2.89 but the selected log mile points indicates the road ends at mile post 2.7. When this happens the program will still draw the segment based on the available reference log mile data. A note will be added to the segment's `COMMENT` attribute noting the discrepancy.

If for any reason the program is unable to draw a given segment, it will record the segment ID number that failed to draw. The list of failed segment IDs will be outputed to a text file.

### Input requirements

#### Segment definitions

The input Excel file requires the following column headers be present:

| SID | YEAR | DISTRICT | COUNTY | MUNI | ROUTE  | MP_START | MP_END | TOTAL_ACCIDENTS | CONTROL | CSIS | SEVERITY_INDEX |
| :-: | :--: | :------: | :----: | :--: | :----: | :------: | :----: | :-------------: | :-----: | :--: | :------------: |
|  1  | 2013 |    5     |   2    |  0   | IS0097 |    0     |  0.5   |        5        |   1U    |  P   |      124       |

#### Log mile point reference

The reference log mile data `mdot_log_mile.gpkg` is a modified version of what is available at [https://data.imap.maryland.gov/datasets/mdot-sha-mile-points-100th](https://data.imap.maryland.gov/datasets/mdot-sha-mile-points-100th)

The unmodified dataset has over 5 million features, many of which is not relevant to our needs. Changes were made to improve search performance and fix inaccurate/incorrect information.
Modifications include:

- Removing all non Interstate, US and State routes.
- Removing all mile points that do not accumulate in a S -> N and W -> E direction.
- Deleting unused attributes
- Fixed incorrect Latitude and Longitude values

### Outputs

- A `.geojson` file containing the CSIL segments that were successfully drawn.
- A `.txt` file listing the IDs of CSIL segments that failed to draw.
