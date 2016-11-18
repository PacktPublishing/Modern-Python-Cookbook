"""Convert the CSV version of the Anscombe data
into a more useful JSON document.
"""
from pathlib import Path
import csv
from collections import defaultdict, OrderedDict
import json

if __name__ == "__main__":
    
    source_path = Path('anscombe_raw.csv')
    with source_path.open() as source_file:
        reader = csv.reader(source_file)
        h1 = next(reader)
        h2 = next(reader)
        series_data = defaultdict(list)
        for row in reader:
            for series, x_col, y_col in (
                ('I', 1, 2), ('II', 3, 4), ('III', 5, 6),
                ('IV', 7, 8)):
                series_data[series].append(
                    OrderedDict([
                        ('x', float(row[x_col])),
                        ('y', float(row[y_col]))]
                    )
                )

    document = [
        OrderedDict([('series', series), ('data', series_data[series])])
        for series in ('I', 'II', 'III', 'IV')
    ]

    print(json.dumps(document, indent=2))
