def unique_in_order(sequence):
    
    if type(sequence) == str: sequence = sequence.split(" ")
    
    return list(sequence)


# sequence = 'AAAABBBCCDAABBB'
# a = unique_in_order(sequence)
# print(a)