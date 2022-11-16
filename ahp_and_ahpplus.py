#  Laboratory work №2

def get_normalized_eigenvector_persons(main_table, c_array):
    normalized_eigenvector_persons = []
    for criterion in range(len(c_array[0])):
        eigenvector_person = []
        pcm = []
        for numerator in main_table:
            eigenvector = 1
            row_in_pcm = []
            for denominator in main_table:
                value = numerator[criterion] / denominator[criterion]
                eigenvector *= numerator[criterion] / denominator[criterion]
                row_in_pcm.append(value)
            pcm.append(row_in_pcm)
            eigenvector_person.append(eigenvector ** (1 / len(main_table)))
        normalized_eigenvector_persons.append([value / sum(eigenvector_person) for value in eigenvector_person])
        consistency_check(pcm, criterion)
    print()
    for counter_c, i in enumerate(normalized_eigenvector_persons):
        print(f'Values of priorities of candidates by с{counter_c + 1}:')
        for counter_candidate, candidate in enumerate(i):
            print(f'{counter_candidate + 1} candidate: {candidate}')
        print(f'Sum is {sum(i)}\n')
    return normalized_eigenvector_persons


def ahp(c_array, normalized_eigenvector_persons):
    print('AHP')
    weight_coefficients_of_all_variants = []
    for counter_variants, c in enumerate(c_array):
        print(f'Variant №{counter_variants + 1}')
        criteria_priority_values = []
        for numerator in c:
            eigenvector = 1
            for denominator in c:
                eigenvector *= numerator / denominator
            criteria_priority_values.append(eigenvector ** (1 / len(c)))

        normalized_eigenvector_criteria = []
        for value in criteria_priority_values:
            normalized_eigenvector_criteria.append(value / sum(criteria_priority_values))

        print(f'The normalized eigenvector of criteria is {normalized_eigenvector_criteria}\n'
              f'The sum of normalized criteria eigenvectors is equal to {sum(normalized_eigenvector_criteria)}')

        result = []
        for person in range(len(normalized_eigenvector_persons[0])):
            final_weight_vector = 0
            for counter_criterion, criterion in enumerate(normalized_eigenvector_criteria):
                final_weight_vector += criterion * normalized_eigenvector_persons[counter_criterion][person]
            result.append(final_weight_vector)

        print('Result:')
        for cntr, i in enumerate(result):
            print(f'The final weight vector of {cntr + 1} person is {i}')
        print(f'Sum result is {sum(result)}\n')
        weight_coefficients_of_all_variants.append(normalized_eigenvector_criteria)
    return weight_coefficients_of_all_variants


def ahp_plus(normalized_eigenvector_persons, weight_coefficient):
    print('AHP PLUS')
    all_normalized_alternatives = []
    for value in normalized_eigenvector_persons:
        normalized_alternative_by_criterion = []
        for cntr in range(len(value)):
            normalized_alternative = []
            for eigenvector_person in value:
                normalized_alternative.append(value[cntr] / (value[cntr] + eigenvector_person))
                normalized_alternative.append(eigenvector_person / (value[cntr] + eigenvector_person))
            normalized_alternative_by_criterion.append(normalized_alternative)
        all_normalized_alternatives.append(normalized_alternative_by_criterion)

    for number_c, values in enumerate(all_normalized_alternatives):
        print(f'Comparison of alternatives by c{number_c + 1}')
        for value in values:
            print(value)
        print()
    for counter_variants, variant in enumerate(weight_coefficient):
        print(f'Variant №{counter_variants + 1}')
        matrix = []
        row_matrix = []
        value_in_matrix = 0
        for row in range(len(all_normalized_alternatives[0])):
            for value in range(len(all_normalized_alternatives[0][row])):
                for number_table in range(len(variant)):
                    value_in_matrix += variant[number_table]*all_normalized_alternatives[number_table][row][value]
                row_matrix.append(value_in_matrix)
                value_in_matrix = 0
            matrix.append(row_matrix)
            row_matrix = []
        print('The resulting matrix:')
        for i in matrix:
            print(i)
        print('\nResult:')
        weight_vector = []
        value_person = 0
        for row in matrix:
            for value in range(0, len(row), 2):
                value_person += row[value]
            weight_vector.append(value_person)
            value_person = 0
        normalized_weight_vector = [i/sum(weight_vector) for i in weight_vector]
        for counter_persons, person in enumerate(normalized_weight_vector):
            print(f'The final weight vector of {counter_persons+1} is {person}')
        print(f'Sum result is {sum(normalized_weight_vector)}\n')


def consistency_check(matrix, number_c):
    import numpy as np
    from numpy import linalg as LA
    wa = LA.eigvals(np.array(matrix))
    lambda_max = round(max(wa).real)
    random_consistency = {3: 0.58,
                          4: 0.9}
    consistency_index = (lambda_max - len(matrix))/(len(matrix) - 1)
    consistency_relation = consistency_index/random_consistency[len(matrix)]
    if consistency_relation < 0.1:
        print(f'Paired comparison matrix by c{number_c+1} is consistency')
    else:
        print(f'Paired comparison matrix by c{number_c+1} is inconsistent')


if __name__ == '__main__':
    AHP = True
    AHP_PLUS = False
    if AHP:
        # AHP          C1 C2 C3
        main_table = [[4, 9, 1],  # П1
                      [5, 2, 2],  # П2
                      [8, 6, 6]]  # П3
        #           C1   C2   C3
        c_array = [[0.4, 0.2, 0.3],
                   [0.3, 0.3, 0.4],
                   [0.2, 0.5, 0.3]]
        normalized_eigenvector_persons = get_normalized_eigenvector_persons(main_table, c_array)
        ahp(c_array, normalized_eigenvector_persons)
    elif AHP_PLUS:
        # AHP +        C1 C2 C3
        main_table = [[4, 9, 1],  # П1
                      [5, 2, 2],  # П2
                      [8, 6, 6],  # П3
                      [6, 3, 7]]  # П4
        #           C1   C2   C3
        c_array = [[0.4, 0.2, 0.3],
                   [0.3, 0.3, 0.4],
                   [0.2, 0.5, 0.3]]
        normalized_eigenvector_persons = get_normalized_eigenvector_persons(main_table, c_array)
        weight_coefficient = ahp(c_array, normalized_eigenvector_persons)
        ahp_plus(normalized_eigenvector_persons, weight_coefficient)
