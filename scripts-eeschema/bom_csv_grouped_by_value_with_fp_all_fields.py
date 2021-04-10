# Modified from kicad
# To run: python "/home/nuclear/.kicad_plugins/bom_csv_grouped_by_value_with_fp_all_fields.py" "%I" "%O.csv"
#
# Example python script to generate a BOM from a KiCad generic netlist
#
# Example: Sorted and Grouped CSV BOM
#

"""
    @package
    Generate a Tab delimited list (csv file type).
    Components are sorted by ref and grouped by value with same footprint
    Fields are (if exist)
    'Ref', 'Qnty', 'Value', 'Cmp name', 'Footprint', 'Description', 'Vendor'

    Command line:
    python "pathToFile/bom_csv_grouped_by_value_with_fp.py" "%I" "%O.csv"
"""

# Import the KiCad python helper module and the csv formatter
import kicad_netlist_reader
import csv
import sys

# Generate an instance of a generic netlist, and load the netlist tree from
# the command line option. If the file doesn't exist, execution will stop
net = kicad_netlist_reader.netlist(sys.argv[1])
header_generated = 0
custom_fields = []

# Open a file to write to, if the file cannot be opened output to stdout
# instead
try:
    f = open(sys.argv[2], 'w')
except IOError:
    e = "Can't open output file for writing: " + sys.argv[2]
    print(__file__, ":", e, sys.stderr)
    f = sys.stdout

# Create a new csv writer object to use as the output formatter
out = csv.writer(f, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)

# Output a set of rows for a header providing general information
out.writerow(['Source:', net.getSource()])
out.writerow(['Date:', net.getDate()])
out.writerow(['Tool:', net.getTool()])
out.writerow( ['Generator:', sys.argv[0]] )
out.writerow(['Component Count:', len(net.components)])
#out.writerow()

# Get all of the components in groups of matching parts + values
# (see ky_generic_netlist_reader.py)
grouped = net.groupComponents()


# Output all of the component information
for group in grouped:
    refs = ""

    # Add the reference of every component in the group and keep a reference
    # to the component so that the other data can be filled in once per group
    for component in group:
        refs += component.getRef() + ", "
        c = component
        if (header_generated == 0):
            base_fields = ['Ref', 'Qnty', 'Value', 'Cmp name', 'Footprint', 'Description', 'Vendor']
            all_fields = base_fields
            custom_fields = c.getFieldNames()
            all_fields.extend(custom_fields)
            out.writerow(all_fields)
            header_generated = 1

    # Fill component common data
    row_data = [refs, len(group), c.getValue(), c.getPartName(), c.getFootprint(),
        c.getDescription(), c.getField("Vendor")]
    # Extract and append custom component fields
    for fieldname in custom_fields:
        row_data.append(c.getField(fieldname))
    # Add row
    out.writerow(row_data)


