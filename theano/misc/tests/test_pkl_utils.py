import numpy
from numpy.testing import assert_allclose
from nose.plugins.skip import SkipTest

import theano
import theano.sandbox.cuda as cuda_ndarray

from theano.sandbox.cuda.type import CudaNdarrayType
from theano.sandbox.cuda.var import CudaNdarraySharedVariable
from theano.sandbox.rng_mrg import MRG_RandomStreams
from theano.misc.pkl_utils import dump, load


def test_dump_load():
    if not cuda_ndarray.cuda_enabled:
        raise SkipTest('Optional package cuda disabled')

    x = CudaNdarraySharedVariable('x', CudaNdarrayType((1, 1), name='x'),
                                  [[1]], False)

    with open('test', 'wb') as f:
        dump(x, f)

    with open('test', 'rb') as f:
        x = load(f)

    assert x.name == 'x'
    assert_allclose(x.get_value(), [[1]])


def test_dump_load_mrg():
    if not cuda_ndarray.cuda_enabled:
        raise SkipTest('Optional package cuda disabled')

    rng = MRG_RandomStreams(use_cuda=True)

    with open('test', 'wb') as f:
        dump(rng, f)

    with open('test', 'rb') as f:
        rng = load(f)

    assert type(rng) == MRG_RandomStreams


def test_dump_zip_names():
    foo_1 = theano.shared(0, name='foo')
    foo_2 = theano.shared(1, name='foo')
    with open('model.zip', 'wb') as f:
        dump((foo_1, foo_2, numpy.array(2)), f)
    keys = numpy.load('model.zip').keys()
    assert keys == ['foo', 'foo_2', 'array_0', 'pkl']
    foo = numpy.load('model.zip')['foo']
    assert foo == numpy.array(0)
    with open('model.zip', 'rb') as f:
        foo_1, foo_2, array = load(f)
    assert array == numpy.array(2)
