from abel.linalg.vector import Vector

a, b = Vector([1, 2]), Vector([3, 4])

def test_repr():
    assert a.__repr__() == '<Vector: [1, 2]>'

def test_str():
    assert str(a) == '<Vector: [1, 2]>'

def test_add():
    assert a + a == Vector([2, 4])
    assert a + b == Vector([4, 6])
    assert b + b == Vector([6, 8])

def test_scal_mult():
    assert a * 5 == Vector([5, 10])
    assert 5 * a == Vector([5, 10])

def test_matmul():
    assert a @ b == 11
    assert b @ a == a @ b
    assert a @ a == 5

def test_norm():
    assert a.norm() - 2.236 < 0.001
    assert b.norm() - 5 < 0.001

def test_angle():
    assert Vector.angle(a, a) < 0.001
    assert Vector.angle(a, b) - 0.1799 < 0.001
    assert Vector.angle(a, b) == Vector.angle(b, a)

def test_proj():
    assert Vector.proj(a, a) == a
    assert Vector.proj(a, b) == Vector([1.32, 1.76])
    assert Vector.proj(b, a) == Vector([2.2, 4.4])

def test_scalproj():
    assert Vector.scalproj(a, b) - 4.919 < 0.01
    assert Vector.scalproj(b, a) - 2.2 < 0.01
    assert Vector.scalproj(a, a) - 2.236 < 0.01
    assert Vector.scalproj(b, b) - 5 < 0.1

def test_cross():
    A, B = Vector([1, 2, 3]), Vector([4, 5, 6])
    assert Vector.cross(A, B) == Vector([-3, 6, -3])
