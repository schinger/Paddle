"""
CIFAR dataset: https://www.cs.toronto.edu/~kriz/cifar.html
"""
import cPickle
import itertools
import numpy
import paddle.v2.dataset.common
import tarfile

__all__ = ['train100', 'test100', 'train10', 'test10']

URL_PREFIX = 'https://www.cs.toronto.edu/~kriz/'
CIFAR10_URL = URL_PREFIX + 'cifar-10-python.tar.gz'
CIFAR10_MD5 = 'c58f30108f718f92721af3b95e74349a'
CIFAR100_URL = URL_PREFIX + 'cifar-100-python.tar.gz'
CIFAR100_MD5 = 'eb9058c3a382ffc7106e4002c42a8d85'


def reader_creator(filename, sub_name):
    def read_batch(batch):
        data = batch['data']
        labels = batch.get('labels', batch.get('fine_labels', None))
        assert labels is not None
        for sample, label in itertools.izip(data, labels):
            yield (sample / 255.0).astype(numpy.float32), int(label)

    def reader():
        with tarfile.open(filename, mode='r') as f:
            names = (each_item.name for each_item in f
                     if sub_name in each_item.name)

            for name in names:
                batch = cPickle.load(f.extractfile(name))
                for item in read_batch(batch):
                    yield item

    return reader


def train100():
    return reader_creator(
        paddle.v2.dataset.common.download(CIFAR100_URL, 'cifar', CIFAR100_MD5),
        'train')


def test100():
    return reader_creator(
        paddle.v2.dataset.common.download(CIFAR100_URL, 'cifar', CIFAR100_MD5),
        'test')


def train10():
    return reader_creator(
        paddle.v2.dataset.common.download(CIFAR10_URL, 'cifar', CIFAR10_MD5),
        'data_batch')


def test10():
    return reader_creator(
        paddle.v2.dataset.common.download(CIFAR10_URL, 'cifar', CIFAR10_MD5),
        'test_batch')
