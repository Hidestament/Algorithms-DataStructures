from src.DataStructures.BitVector.bit_vector_accumulate import BitVectorAcc as BitVector


def test_rank1():
    B = [1, 0, 0, 1, 1, 0, 1]
    bv = BitVector(B)

    assert bv.rank1(-1) == 0
    assert bv.rank1(0) == 0
    assert bv.rank1(1) == 1
    assert bv.rank1(2) == 1
    assert bv.rank1(3) == 1
    assert bv.rank1(4) == 2
    assert bv.rank1(5) == 3
    assert bv.rank1(6) == 3
    assert bv.rank1(7) == 4
    assert bv.rank1(8) == 4


def test_rank0():
    B = [1, 0, 0, 1, 1, 0, 1]
    bv = BitVector(B)

    assert bv.rank0(-1) == 0
    assert bv.rank0(0) == 0
    assert bv.rank0(1) == 0
    assert bv.rank0(2) == 1
    assert bv.rank0(3) == 2
    assert bv.rank0(4) == 2
    assert bv.rank0(5) == 2
    assert bv.rank0(6) == 3
    assert bv.rank0(7) == 3
    assert bv.rank0(8) == 3


def test_rank0_all():
    B = [1, 0, 0, 1, 1, 0, 1]
    bv = BitVector(B)

    assert bv.rank0_all() == 3


def test_rank1_all():
    B = [1, 0, 0, 1, 1, 0, 1]
    bv = BitVector(B)

    assert bv.rank1_all() == 4


def test_select0():
    B = [1, 0, 0, 1, 1, 0, 1]
    bv = BitVector(B)

    assert bv.select0(-1) is None
    assert bv.select0(0) is None
    assert bv.select0(1) == 1
    assert bv.select0(2) == 2
    assert bv.select0(3) == 5
    assert bv.select0(4) is None
    assert bv.select0(5) is None
    assert bv.select0(6) is None


def test_select1():
    B = [1, 0, 0, 1, 1, 0, 1]
    bv = BitVector(B)

    assert bv.select1(-1) is None
    assert bv.select1(0) is None
    assert bv.select1(1) == 0
    assert bv.select1(2) == 3
    assert bv.select1(3) == 4
    assert bv.select1(4) == 6
    assert bv.select1(5) is None
    assert bv.select1(6) is None
