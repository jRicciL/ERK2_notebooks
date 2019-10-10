
def _get_seq(ranges, x, sep = ' '):
	from itertools import chain
	lista = [list( range(valor[0], valor[1] + 1) ) for valor in ranges]
	# Se obtiene la lista de residuos, incluida en formato de cadena de texto
	seq_residues = list(chain.from_iterable(lista))
	seq_residues_str = sep.join(str(e) for e in seq_residues)
	if x == 'str':
		final_seq = seq_residues_str
	elif x == 'list':
		final_seq = seq_residues
	else: 
		final_seq = "Especifica el tipo de retorno: 'str' o 'list'"
	return(final_seq)


def get_pocket_residues(x='str', sep = ' '):
	# Pocket (4FKW y su ligando a 7 A): 8-19, 30-33, 64-65, 79-90, 129-134, 143-146
	# resid 8 to 19 30 to 33 64 65 79 to 90 129 to 134 143 to 146
	pocket_rangeResidues = [[8,19], [30,33], [64,65], [79,90], [129,134], [143,146]]
	final_seq = _get_seq(pocket_rangeResidues, x, sep)
	return(final_seq)

def get_pisani_residues(x='str', sep = ' '):
	pisiani_rangeResidues = [ [4,12], [17, 24], [29,34], [46,55], [66,71], [76,81],  
							[87,93], [101, 120], [121, 135], [140, 150], [182, 194], [277, 282]]
	final_seq = _get_seq(pisiani_rangeResidues, x, sep)
	return(final_seq)

