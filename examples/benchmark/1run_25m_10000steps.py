import aim


sess = aim.Session()

sess.set_params({
    'test_param_1': 1,
    'test_param_2': 2,
    'test_param_3': 3,
})

for m in range(25):
    for s in range(10000):
        sess.track(s, name='metric_{}'.format(m))
