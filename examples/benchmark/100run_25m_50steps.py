import aim


for r in range(100):
    sess = aim.Session(experiment='100run_25m_50steps')
    print('Run {}: {}'.format(r, sess.run_hash))

    sess.set_params({
        'test_param_1': 1,
        'test_param_2': 2,
        'test_param_3': 3,
    })

    for m in range(25):
        for s in range(50):
            sess.track(s, name='metric_{}'.format(m))

    sess.close()
