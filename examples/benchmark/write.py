import aim


runs = 1000
metrics = 10
steps = 10

for r in range(runs):
    sess = aim.Session(experiment='uwrite')
    print('Run {}: {}'.format(r, sess.run_hash))

    sess.set_params({
        'test_param_1': 1,
        'test_param_2': 2,
        'test_param_3': 3,
    })

    for m in range(metrics):
        for s in range(steps):
            sess.track(s, name='metric_{}'.format(m))

    sess.close()
