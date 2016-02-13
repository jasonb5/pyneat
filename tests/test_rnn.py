from ml.ann import RecurrentNeuralNetwork as RNN

def test_creation():
    rnn = RNN((2, 5, 3))

    assert rnn.dh.shape == (5, 1)
    assert rnn.do.shape == (3, 1)
    assert rnn.wb.shape == (5, 3)
    assert rnn.wh.shape == (5, 5)
    assert rnn.wi.shape == (5, 2)
    assert rnn.wo.shape == (3, 7)

def test_add_link():
    rnn = RNN((2, 2, 2))

    assert not rnn.add_link(0, 0, 1.1)
    assert rnn.add_link(0, 2, 1.2)
    assert rnn.add_link(0, 4, 1.3)
    assert not rnn.add_link(2, 0, 1.4)
    assert rnn.add_link(2, 3, 1.5)
    assert rnn.add_link(2, 4, 1.6)
    assert not rnn.add_link(4, 0, 1.7)
    assert not rnn.add_link(4, 5, 1.8)
    assert rnn.add_link(4, 2, 1.9)

    assert rnn.wi[0, 0] == 1.2
    assert rnn.wo[0, 0] == 1.3
    assert rnn.wh[0, 1] == 1.5
    assert rnn.wo[0, 2] == 1.6
    assert rnn.wb[0, 0] == 1.9

def test_activate():
    rnn = RNN((2, 2, 1))

    rnn.add_link(0, 2)
    rnn.add_link(0, 3)
    rnn.add_link(1, 2)
    rnn.add_link(1, 3)
    rnn.add_link(2, 4)
    rnn.add_link(3, 4)

    res = rnn.activate((1.0, 1.0))

    assert res == 4.0
