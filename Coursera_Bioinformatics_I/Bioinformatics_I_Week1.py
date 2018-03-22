def complement(dna):
	"""Returns the complement of a DNA string
	Args:
		dna (str): the DNA string
	Returns:
		str: the complement of the DNA string
	"""
	list_complement = []
	for i in dna:
		if i == 'A':
			list_complement.append('T')
		elif i == 'T':
			list_complement.append('A')
		elif i == 'G':
			list_complement.append('C')
		elif i == 'C':
			list_complement.append('G')
	complement = ''.join(list_complement)
	return complement

def reverse_complement(dna):
	"""Returns the reverse complement of dna
	Args:
		dna (str): the DNA string
	Returns:
		str: the reverse complement of the DNA string
	"""
	reverse = dna[::-1]
	return complement(reverse)

def pattern_count(text, pattern):
	"""Returns the incidence of pattern in text
	Args:
		text (str): the text to be searched
		pattern(str): the pattern to search for

	Returns:
		int: the count of pattern in text
	"""
	count = 0
	for i in range(len(text)-len(pattern)):
		if text[i:i+len(pattern)] == pattern:
			count = count + 1
	return count 

def pattern_match(text, pattern):
	"""Returns the indices that a specific pattern is found in text
	Args:
		text(str): the text to be searched
		pattern(str): the pattern to search for

	Returns:
		str: the indices of the matches (formatted for quiz submission)
	"""
	

	match_list = []
	for i in range(len(text)-len(pattern)):
		if text[i:i+len(pattern)] == pattern:
			match_list.append(str(i))
	formatted_list = ' '.join(match_list)
	return formatted_list

#Brute force solution of the frequent words problem
def frequent_words(text, k):
	"""Returns the most frequent kmer(s) of length k found in text
	Args:
		text (str): the text to be searched
		k (int): the length of the kmer

	Returns:
		set: the set of kmer(s)
	"""	
	frequent_patterns = set()
	count = []
	for i in range(len(text)-k):
		pattern = text[i:i+k]
		count.append(pattern_count(text, pattern))
	max_count = max(count)
	for i in range(len(text)-k):
		if count[i] == max_count:
			frequent_patterns.add(text[i:i+k])
	return frequent_patterns

#The following 4 functions provide a more efficient solution to the frequent words problem
def pattern_to_number(pattern):
    """Convert a sequence to an index in a lexigraphically sorted list of all possible kmers of length pattern
    The approach being taken amounts to converting a base 4 number to a base 10 number
	Args:
		pattern(str): the sequence to convert
	Returns:
		int: the index of pattern in the lexigraphically sorted list of all possible kmers of length pattern
    """
    count = 0
    d = {'A': 0, 'C': 1, 'G': 2, 'T':3}
    for index, base in enumerate(pattern):
        exponent = len(pattern) - index - 1
        base_int = d[base]
        base_4_digit = base_int*4**exponent
        count = count + base_4_digit
    return count

def number_to_reverse_pattern(index, k):
    """Returns the sequence (reversed) associated with the index of a lexigraphically sorted list of DNA sequences of length k
	Args:
		index(int): The index of a lexigraphically sorted list of DNA sequences of length k
		k(int): The length of the kmer
	Returns:
		str: The reverse of the DNA sequence associated with index
    """
    d = {0: 'A', 1: 'C', 2: 'G', 3: 'T'}
    print('assessing with index', index, 'and k =', k)
    if k == 1:
        print('base =', d[index])
        return d[index]
    prefix_index = index // 4
    print('quotient\t:', prefix_index)
    r = index % 4
    print('remainder\t:', r)
    symbol = d[r]
    print('base =', symbol)
    #Recursion meant I could only get the reverse of the answer
    pattern = number_to_pattern(prefix_index, k-1)
    concat = pattern + symbol
    return concat[::-1]

def number_to_pattern(index, k):
    """Returns the sequence associated with the index of a lexigraphically sorted list of DNA sequences of length k
	Args:
		index(int): The index of a lexigraphically sorted list of DNA sequences of length k
		k(int): The length of the kmer
	Returns:
		str: The DNA sequence associated with index
    """
    return number_to_reverse_pattern(index, k)[::-1] 

def finding_frequent_words_by_sorting(text, k):
    """Finds the most frequent words of length k in text with no nested for loops to increase efficiency 
	Args:
		text(str): The text to be searched for frequent words
		k(int): The length of the kmer words
	Returns:
		set: The most frequent words found in text
	
    """
    frequent_patterns = set()
    index = []
    count = []
    for i in range(len(text)-k+1):
        pattern = text[i:k+i]
        index.append(pattern_to_number(pattern))
        count.append(1)
    index.sort()
    for i in range(1, len(text)-k+1):
        if index[i] == index[i-1]:
            count[i] = count[i-1] + 1
    max_count = max(count)
    for i in range(0, len(text)-k+1):
        if count[i] == max_count:
            pattern = number_to_pattern(index[i], k)
            frequent_patterns.add(pattern)
    return frequent_patterns


def computing_frequencies(string, k):
    """Returns the number of lexigraphically ordered kmers of length k found in string
	Args:
		string(str): the string to be searched
		k(int): the length of the kmer to be searched
	Returns:
		None
    """
    #start with a n empty frequency array
    freq_array = [0]*4**k
    window = len(string)-k+1
    for base in range(window):
        pattern = string[base:base+k]
        index = pattern_to_number(pattern)
        freq_array[index] = freq_array[index] + 1
    print(*freq_array, sep=' ')
    return None

def cluster_finding(k, t, l, genome):
	"""Returns clusters of kmers of length k of incidence t in sliding windows of
	length l in string genome
	Args:
		k (int): length of kmer
		t (int): minimum incidence of kmer to be considered a clump
		l (int): the length of the sliding window
		genome (str): the DNA sequence to search through
	
	Returns:
		str: A formatted list of sequences that pass as clusters

	"""

	count = []
	clusters = set()
	for i in range(len(genome)-l+1):		
		pattern = genome[i:i+k]
		window = genome[i:i+l]
		count.append(pattern_count(window, pattern))
	for i in range(len(genome)-l+1):
		if count[i] >= t:
			clusters.add(genome[i:i+k])
	formatted_list = ' '.join(list(clusters))
	return formatted_list




