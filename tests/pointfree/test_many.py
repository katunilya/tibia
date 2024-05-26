from tibia.many import Many
from tibia.pointfree.many import join


def test_join():
    initial = [[1, 2, 3], [4, 5, 6]]
    joined = Many(initial).reduce_values_to(join, [])

    assert isinstance(joined, list)
    assert len(joined) == sum((len(x) for x in initial))
