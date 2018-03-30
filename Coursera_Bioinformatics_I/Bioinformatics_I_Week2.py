import Bioinformatics_I_Week1 as bio1
from itertools import product

def minimum_skew(genome):
    """Returns position(s) in genome where the cumulative difference between the number of 
    G's and C's are minimized 
    Args: 
        genome(str): the DNA string to calculate GC skew
    Returns:
        str: The index in genome where the GC skew is mimimized     
    """
    skew_list =[]
    min_position = []
    count = 0
    for i in genome:
        if i == 'G':
            count = count + 1
            skew_list.append(count)
        elif i == 'C':
            count = count - 1
            skew_list.append(count)
        else:
            skew_list.append(count)
    for i in range(len(skew_list)):
        if skew_list[i] == min(skew_list):
            min_position.append(i+1)
    return min_position

def hamming_distance(string1, string2):
    """Returns the number of mismatches between string1 and string2
	Args:
		string1(str): the first string
		string2(str): the second string
	Returns:
		int: the number of mismatches between string 1 and string 2
    """
    count = 0
    for i in range(len(string1)):
        if string1[i] != string2[i]:
            count = count + 1
    return count 

def approximate_pattern_match(m, word, genome):
    """Returns index/indices of approximate matches of word in genome with number of mismatches allowed m
	Args:
		m(int): the number of mismatches allowed
		word(str): the string to use for searching
		genome(str): the string to be searched
	Returns:
		int: the index/indices of approximate matches of word to genome
    """
    match_return = []
    match_count = []
    for i in range(0, len(genome)-len(word)+1):
        match_list = []
        window = genome[i:i+len(word)]
        ham_dist = hamming_distance(window, word)
        if ham_dist <= m:
            match_return.append(str(i))
    formatted_list = ' '.join(match_return)
    return formatted_list

def approximate_pattern_count(text, pattern, d):
    """Returns the number of matches of pattern to text with mismatched allowed d
	Args:
		text(str): the string to be searched
		pattern(str): the pattern to use for searching
		genome(int): the number of mismatches allowed
	Returns:
		int: the number of approximate matches of pattern to text with at most d mismatches
    """
    count = 0
    for i in range(len(text)-len(pattern)+1):
        pat = text[i:i+len(pattern)]
        if hamming_distance(pat, pattern) <= d:
            count = count + 1
    return count


def list_kmer(k):
	"""Returns an lexigraphically sorted list of all kmers composed of A's, C's, T's, and G's in kmer of length k
	Args:
		k(int): the length of the kmers
	Returns:
		list: all the possible DNA kmers
	"""
	list = []
	str = ''
	for i in product('ACGT', repeat = k):
		list.append(i)
	formatted_list = []
	for letters in list:
		formatted_list.append(''.join(letters))	
	return formatted_list

def neighbors(kmer, d):
	"""Returns a list of all sequences that have at most d mismatches with kmer
	Args:
		kmer(str): the kmer to be mutated
	Returns:
		list: includes kmer and all mutated sequences with at most d mismatches with kmer
	"""


	legal_mutations =[]
	possibilities = list_kmer(len(kmer))
	for i in possibilities:
		if hamming_distance(i, kmer) <= d:
			legal_mutations.append(i)
	return legal_mutations

def frequent_words_with_mismatches(genome, k, d):
	"""Returns the most frequent kmer(s) of length k in genome with mismatches allowed d
	Args:
		genome(str): the genome to be searched
		k(int): the lenght of the frequent kmers
		d(int): the number of mismatches allowed between any kmer and genome
	Returns:
		list: the most frequent kmers with length k at at most d mismatches with genome
	"""

	given_kmers = set()
	neighbors_lists = []
	counts = []
	frequent_kmers = []
	for index in range(0, len(genome)-k+1):
		kmer = genome[index:index+k]
		given_kmers.add(kmer)
	
	for i in list(given_kmers):
		neighbors_lists.append(neighbors(i,d))
	flattened_neighbors = [val for sublist in neighbors_lists for val in sublist]
	neighbors_list = list(set(flattened_neighbors))
	for i in neighbors_list:
		counts.append(approximate_pattern_count(genome, i, d))
	highest_counts = [i for i, x in enumerate(counts) if x == max(counts)]
	for index in highest_counts:
		frequent_kmers.append(neighbors_list[index])
	return frequent_kmers

def frequent_words_with_mismatches_reverse_complement(genome, k, d):
	"""Returns the most frequent kmer(s) of length k in genome with mismatches allowed d.  
	kmers are searched through both the forward and reverse complement of genome 
	Args:
		genome(str): the genome to be searched
		k(int): the lenght of the frequent kmers
		d(int): the number of mismatches allowed between any kmer and genome
	Returns:
		list: the most frequent kmers with length k at at most d mismatches with genome
	"""
	given_kmers = set()
	neighbors_lists = []
	counts = []
	frequent_kmers = []
	for index in range(0, len(genome)-k+1):
		kmer = genome[index:index+k]
		given_kmers.add(kmer)
	for index in range(0, len(bio1.reverse_complement(genome))-k+1):
		kmer = genome[index:index+k]
		given_kmers.add(kmer)

	for i in list(given_kmers):
		neighbors_lists.append(neighbors(i,d))
	flattened_neighbors = [val for sublist in neighbors_lists for val in sublist]
	neighbors_list = list(set(flattened_neighbors))
	for i in neighbors_list:
		forward_count = approximate_pattern_count(genome, i, d)
		reverse_count = approximate_pattern_count(bio1.reverse_complement(genome), i, d)
		counts.append(forward_count + reverse_count)
	highest_counts = [i for i, x in enumerate(counts) if x == max(counts)]
	for index in highest_counts:
		frequent_kmers.append(neighbors_list[index])
	return frequent_kmers




