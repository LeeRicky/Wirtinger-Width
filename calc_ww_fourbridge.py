from itertools import combinations

def process_gauss_code(raw_gauss_code):
    '''
    Formats input Gauss code for use in other functions.
    input:
        a sequence of characters or strings (which may contain commas) representing a Gauss code.

    output:
        a list of signed integers representing the Gauss code of a knot diagram.
    '''

    return [int(s.replace(',', '')) for s in raw_gauss_code]


def create_knot_dictionary(gauss_code):
    '''
    Creates a knot dictionary from a Gauss code.

    input:
        gauss_code - a list of ints representing the Gauss code of the knot.

    output:
        a dictionary representing the diagram of the Gauss code.

    The output knot dictionary is of the form

            d_k = {
                s_i: [(gauss_subseq), [c_1, c_2, . . ., c_n]]
                .
                .
                .
            },

    where s_i is the name of the strand, gauss_subseq is a tuple representing the subsequence of the Gauss code
    corresponding to the the strand, and the c_i represent the crossings that s_n are over.  The c_i are tuples
    (s_i_1, s_i_2), where s_i_1 and s_i_2 are the names of the strands that s_i is over.

    Warnings:
        This code will only run on standard Gauss code.
        This code does NOT check if the Gauss code is 'correct.'
        See readme.md for more details.

    '''

    strands_dict = find_strands(gauss_code)
    knot_dict = find_crossings(strands_dict, gauss_code)

    return knot_dict


def find_strands(gauss_code):
    '''
    Processes a Gauss code to find the strands of the knot diagram.

    inputs:
        gauss_code: a Gauss code (a list of signed integers) representing some knot diagram D.


    output:
        a dictionary whose keys are the strands of the knot diagram D.

    The output knot dictionary is of the form
                d_k = {
                    s_i: [(gauss_subseq), [c_1, c_2, . . ., c_n]]
                    .
                    .
                    .
                },

    where s_i is the name of the strand and gauss_subseq is a tuple representing the subsequence of the
    Gauss code corresponding to the the strand.  The empty list will be populated with crossing
    information in the find_crossings function.
    '''

    strand_set = set()

    i = 0
    while True:
        if gauss_code[i] < 0:
            beginning = i
            i = (i + 1) % len(gauss_code)
            while gauss_code[i] > 0:
                i = (i + 1) % len(gauss_code)
            if beginning > i:
                new_strand = gauss_code[beginning:]
                for k in range(i + 1):
                    new_strand.append(gauss_code[k])
                new_strand = tuple(new_strand)
            else:
                new_strand = tuple(gauss_code[beginning:i + 1])
            if new_strand not in strand_set:
                strand_set.add(new_strand)
            else:
                break
        else:
            i = (i + 1) % len(gauss_code)

    letter_list = list(map(chr, range(65, 91)))
    strands_dict = dict()
    for i, strand in enumerate(strand_set):
        strands_dict[letter_list[i]] = [strand, []]
    return strands_dict


def find_crossings(knot_dict, gauss_code):
    '''
    Takes a knot dictionary as output from the find_strands function and the corresponding Gauss code
    and populates the empty list in each key entry with the crossings that the strand is over.

    inputs:
        gauss_code: a Gauss code (a list of signed integers) representing some knot diagram D.
        knot_dict: a dictionary as output from find_strands.


    output:
        a dictionary whose keys are the strands of the knot diagram D.
    The output knot dictionary is of the form
                d_k = {
                    s_i: [(gauss_subseq), []]
                    .
                    .
                    .
                },
    where s_i is the name of the strand, gauss_subseq is a tuple representing the subsequence of the Gauss code
    corresponding to the the strand, and the c_i represent the crossings that s_n are over.  The c_i are tuples
    (s_i_1, s_i_2), where s_i_1 and s_i_2 are the names of the strands that s_i is over.
    '''

    for key_outer in knot_dict:
        for under in knot_dict[key_outer][0]:
            if under > 0:
                found1, found2 = False, False
                for key_inner in knot_dict:
                    if found1 and found2:
                        break
                    else:
                        if knot_dict[key_inner][0][0] == -under:
                            under1 = key_inner
                            found1 = True
                        if knot_dict[key_inner][0][-1] == -under:
                            under2 = key_inner
                            found2 = True
                knot_dict[key_outer][1].append((under1, under2))

    return knot_dict


def get_seeds(strands, length):
    '''
    input:
        strands: the list of strands in our knot diagram
        length: the desired number of seed strands to start out with
    output:
        An object list of tuples representing seed strands.
        ex: [('A','B'), ('A','C'), ('A','D'), ('B','C'),... ]
    '''
    seeds = combinations(strands, length)
    return seeds


def find_color(strand, strand_colors_dict):
    '''
    Finds the key in strand_colors_dict that contains a list containing strand. In other words, give it a strand and
    it will output what color it is. If the strand is uncolored, the empty character is returned
    Input:
        strand: A char representing a strand in a knot diagram
        strand_colors_dict: A dictionary whose keys are our seed strands and whose values are lists of strands which are 
            the same color as the key. Note each value contains a character representing its key. 
            Strand_color_dict is of the form
            d_k = {
                    A: ['A', ...]
                    B: ['B', ...]
                    .
                    .
                }, 
    Output:
        retruns either the color of the strand, (key in dictionary containing a list where strand is an element)
        or returns the empty character if no such key can be found
    '''
    for color in strand_colors_dict:
        if strand in strand_colors_dict[color]:
            return color
    return ''


def maximally_extend(seeds, knot_dict):
    '''
    input:
        seeds: a tuple of chars containing the strands that start out colored
        knot_dict: A dictionary with strands as keys and a list of crossings for which that key is an over strand, as 
            output from create_knot_dictionary
    output:
        strand_colors_dict: A dictionary whose keys are our seed strands and whos values are lists of strands which are 
            the same color as the key. Note each value contains a character representing its key. 
            Strand_color_dict is of the form
            d_k = {
                    A: ['A', ...]
                    B: ['B', ...]
                    .
                    .
                }, 
    '''
    strand_colors_dict = {}
    for strand in seeds:
        strand_colors_dict[strand] = []
    for seed in strand_colors_dict:
        strand_colors_dict[seed].append(seed)
    colored_strands = []
    for s in seeds:
        colored_strands.append(s)
    new_coloring = True
    while new_coloring:
        new_coloring = False
        for seed in strand_colors_dict:
            for strand in strand_colors_dict[seed]:
                for crossing in knot_dict[strand][1]:
                    if crossing[0] in colored_strands and crossing[1] not in colored_strands:
                        color = find_color(crossing[0], strand_colors_dict)
                        strand_colors_dict[color].append(crossing[1])
                        colored_strands.append(crossing[1])
                        new_coloring = True
                    elif crossing[0] not in colored_strands and crossing[1] in colored_strands:
                        color = find_color(crossing[1], strand_colors_dict)
                        strand_colors_dict[color].append(crossing[0])
                        colored_strands.append(crossing[0])
                        new_coloring = True
    return strand_colors_dict

def is_colored(strand, strand_colors_dict):
    '''
    Determines if a strand is currently colored.
    
    Input:
        strand: A char representing a strand in a knot diagram
        strand_colors_dict: A dictionary whose keys are our seed strands and whos values are lists of strands which are 
            the same color as the key. Note each value contains a character representing its key. 
            Strand_color_dict is of the form
            d_k = {
                    A: ['A', ...]
                    B: ['B', ...]
                    .
                    .
                },   
    '''
    for color in strand_colors_dict:
        if strand in strand_colors_dict[color]:
            return True
    return False


def count_multicolored_crossings(strand_colors_dict, knot_dict):
    '''
    Given two dictionaries, one of which represents a maximal extension of a set of seeds, this function counts the
    number of multicolored crossings resulting from the maximal extension
    Input:
        strand_colors_dict: A dictionary where the keys are seed strands and the values are a list of
            characters representing the strands that are the same color as the seed   
        knot_dict: A dictionary with strands as keys and a list of crossings for which that key is an over strand, as 
            output from create_knot_dictionary
    Output:
        n_multicolored_crossings: An integer representing the number of multicolored crossings in our maximal extension
    '''
    n_multicolored_crossings = 0
    for color in strand_colors_dict:
        for strand in strand_colors_dict[color]:
            for crossing in knot_dict[strand][1]:
                if is_colored(crossing[0], strand_colors_dict) and is_colored(crossing[1], strand_colors_dict):
                    if crossing[1] not in strand_colors_dict[find_color(crossing[0], strand_colors_dict)]:
                        n_multicolored_crossings += 1
    return n_multicolored_crossings


def calc(raw_gauss_code):
    '''
    Note this implementation depends on knowing before hand that the Gauss code is of a bridge number four knot. Moreover,
    the Gauss code represents a diagram that actuall realizes Wirtinger number four.
    
    input: 
        raw_gauss_code: A list of characters representing a Gauss code.
    
    output:
        An upper bound on the Gabai width
    '''
    gauss_code = process_gauss_code(raw_gauss_code)
    knot_dict = create_knot_dictionary(gauss_code)
    strands = []
    for s in knot_dict:
        strands.append(s)
    seeds_set = get_seeds(strands, 3)
    n_multicolored_crossings = 0
    for seeds in seeds_set:
        strand_colors_dict = maximally_extend(seeds, knot_dict)
        n_multicolored_crossings = count_multicolored_crossings(strand_colors_dict, knot_dict)
        if n_multicolored_crossings > 0:
            colored_set = []
            for keys in strand_colors_dict:
                for s in strand_colors_dict[keys]:
                    colored_set.append(s)
            for potential_seed in strands:
                if potential_seed not in colored_set:
                    seed_addition = (potential_seed,)
                    new_seeds = seeds + seed_addition
                    new_strand_colors_dict = maximally_extend(new_seeds, knot_dict)
                    new_colored_set = []
                    for new_keys in new_strand_colors_dict:
                        for t in new_strand_colors_dict[new_keys]:
                            new_colored_set.append(t)
                    if set(new_colored_set) == set(strands):
                        return '28'
        n_multicolored_crossings = 0
    return '32'



    