from src.Algorithms.String.z_algorithm import z_algorithm


def test_z_algorithm():
    S = "abcabc"
    assert z_algorithm(S) == [6, 0, 0, 3, 0, 0]

    S = "aaabaaaab"
    assert z_algorithm(S) == [9, 2, 1, 0, 3, 4, 2, 1, 0]

    S = "abcbcba"
    assert z_algorithm(S) == [7, 0, 0, 0, 0, 0, 1]

    S = "mississippi"
    assert z_algorithm(S) == [11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    S = "ababacaca"
    assert z_algorithm(S) == [9, 0, 3, 0, 1, 0, 1, 0, 1]

    S = "aaaaa"
    assert z_algorithm(S) == [5, 4, 3, 2, 1]
