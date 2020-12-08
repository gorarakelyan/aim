import argparse
import aim


parser = argparse.ArgumentParser()
parser.add_argument('--runs', type=int, default=1000)
parser.add_argument('--params', type=int, default=100)
parser.add_argument('--metrics', type=int, default=100)
parser.add_argument('--steps', type=int, default=100)

args = parser.parse_args()

for r in range(args.runs):
    sess = aim.Session(experiment='runs{}_params{}_metrics{}_steps{}')
    print('Run {}: {}'.format(r, sess.run_hash))

    sess.set_params({'test_param_{}'.format(i): i for i in range(args.params)})

    for m in range(args.metrics):
        for s in range(args.steps):
            sess.track(s, name='metric_{}'.format(m))

    sess.close()
