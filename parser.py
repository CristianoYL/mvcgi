import os
import unicodedata
from collections import defaultdict

from csv import DictReader
from biothings.utils.dataload import open_anyfile

DATA_SCHEMA = ('chrom', 'start', 'end', 'ncer_percentile')
SOURCE_NAME = 'mvcgi'


def load_data(data_folder):

    input_file = os.path.join(data_folder, 'julia_data')
    assert os.path.exists(input_file), f'Cannot find input file {input_file}'
    with open_anyfile(input_file) as in_f:
        # field names
        fields = DATA_SCHEMA
        # Remove duplicated lines if any
        lines = set(list(in_f))
        reader = DictReader(lines, fieldnames=fields, delimiter='\t')

        results = defaultdict(list)
        for row in reader:
            # construct identifier (e.g. chr1:g.678900_679000)
            _id = f'{row["chrom"]}:g.{row["start"]}_{row["end"]}'
            variant = {k: unicodedata.normalize("NFKD", v) for k, v in row.items()}
            # variant = dict_sweep(variant, vals=['', 'null', 'N/A', None, [], {}])
            results[_id].append(variant)

        # Merge duplications
        for k, v in results.items():
            yield {
                '_id': k,
                SOURCE_NAME: v
            }
