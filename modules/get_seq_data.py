import prody
from Bio import pairwise2, SeqIO
from .find_gaps import find_gaps

def get_data(pdb_id, seq_TOTAL, struct_dir = '../ARCHIVOS/CRISTALES/PROT_CDK2_CHAINS/', tail_pdb = '_A.pdb'):

    '''Genera un alineamiento  partir de una estructura PDB y una secuencia de aminoácidos.'''
    structure = prody.parsePDB(struct_dir + pdb_id + tail_pdb).getHierView()["A"]
    seq_query = structure.getSequence()
    alignment = pairwise2.align.globalxs(seq_query, seq_TOTAL, 
                                            -10, -1, gap_char='-',
                                        one_alignment_only = True)[0]
    seq_alg = alignment[0]

    covertura = len(seq_query) / len(seq_TOTAL) *100
    gaps = find_gaps(alignment[0])
    num_gaps = gaps["num_gaps"]
    gap_lengths = gaps["gap_lengths"]
    gap_list = gaps["gap_list"]

    # Debería retornar un tuple con 3 elementos
    return(seq_alg, covertura, gaps)

# Ejemplo
# get_seq_data('1e9h', cdk2_P24941)

