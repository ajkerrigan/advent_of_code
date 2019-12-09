import pytest
from queue import Queue
from intcode import Program

SAMPLE1 = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
SAMPLE2 = '1102,34915192,34915192,7,4,7,99,0'
SAMPLE3 = '104,1125899906842624,99'

@pytest.fixture
def inq():
    return Queue()

@pytest.fixture
def outq():
    return Queue()

def test_sample1(inq, outq):
    Program(SAMPLE1).run(inq, outq)
    assert list(outq.queue) == [int(num) for num in SAMPLE1.split(',')]

def test_sample2(inq, outq):
    Program(SAMPLE2).run(inq, outq)
    assert len(str(outq.queue.pop())) == 16

def test_sample3(inq, outq):
    Program(SAMPLE3).run(inq, outq)
    assert len(str(outq.queue.pop())) >= 5
