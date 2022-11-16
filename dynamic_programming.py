from random import randint
#  Laboratory work №1

if __name__ == '__main__':
    length_genetic_code = 20
    genetic_code = [['A', 'G', 'T', 'C'][randint(0, 3)] for i in range(length_genetic_code)]
    print(f'genetic code is: {"".join(genetic_code)}')
    sequences = {}
    last_letter = genetic_code[0]
    length_sequence = 1
    sequence = genetic_code[0]

    for letter in range(1, len(genetic_code)):
        if genetic_code[letter] == last_letter:
            length_sequence += 1
            sequence += genetic_code[letter]
        else:
            sequences[length_sequence] = sequence
            length_sequence = 1
            sequence = genetic_code[letter]
        last_letter = genetic_code[letter]
        if letter == len(genetic_code)-1:
            sequences[length_sequence] = sequence
    print(f'subsequence of identical characters of maximum length is: {sequences.get(max(sequences))}')
