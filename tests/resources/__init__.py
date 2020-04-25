import csv
import os

__all__ = ('MOLECULES', )

DIR_PATH = os.path.dirname(__file__)

with open(os.path.join(DIR_PATH, "molecules.tsv"), "r") as f:
    f.readline()  # ignore title line
    MOLECULES = [{'name': name,
                  'smiles': smiles,
                  'inchi': inchi,
                  'image': os.path.join(DIR_PATH, name + ".png"),
                  'svg': os.path.join(DIR_PATH, name + ".svg"),
                  } for name, smiles, inchi in csv.reader(f, delimiter='\t')]

