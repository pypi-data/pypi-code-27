from test_data import TestData


@TestData(
    tf_checkpoint_dir='/mnt/f/benchmark/benchmarks-master/resnet50v1_traindir',
    tf_values={
        'add': 'tower_0/v/cg/resnet_v10/add:0',
        'relu': 'tower_0/v/cg/resnet_v115/Relu:0'
    })
def test(test_data):
    print({k: type(v) for (k, v) in test_data.items()})


test()
