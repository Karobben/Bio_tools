import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i','-I','--input')     
parser.add_argument('-o','-U','--output')     

args = parser.parse_args()
INPUT = args.input
OUTPUT = args.output

from Bio import PDB


def renumber_pdb(input_file, output_file, start_resi=1):
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure('PDB_structure', input_file)

    # Initialize the residue number
    new_resi = start_resi

    # Loop through all models, chains, and residues
    for model in structure:
        for chain in model:
            for residue in chain:
                # Change the residue ID to the new_resi
                residue.id = (' ', f"tmp_{new_resi}", ' ')
                new_resi += 1

    for model in structure:
        for chain in model:
            new_resi = start_resi
            for residue in chain:
                # Change the residue ID to the new_resi
                residue.id = (' ', new_resi, ' ')
                new_resi += 1


    # Save the modified structure to a new PDB file
    io = PDB.PDBIO()
    io.set_structure(structure)
    io.save(output_file)

renumber_pdb(INPUT, OUTPUT)
