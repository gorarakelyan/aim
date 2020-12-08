from pprint import pprint
import argparse
import time

from aim.engine.repo.repo import AimRepo
from aim.ql.grammar.statement import Statement
from aim.artifacts.metric import Metric as MetricArtifact


def scale_trace_steps(max_metric_len, max_steps):
    scaled_steps_len = max_steps
    if scaled_steps_len > max_metric_len:
        scaled_steps_len = max_metric_len
    if scaled_steps_len:
        scaled_steps = slice(0, max_metric_len,
                             max_metric_len // scaled_steps_len)
    else:
        scaled_steps = slice(0, 0)
    return scaled_steps


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', type=str,
                        default='metric_2, metric if experiment is not None')
    args = parser.parse_args()

    # Get repo
    s = time.time()
    repo = AimRepo.get_working_repo(mode='r')
    e = time.time()
    print('Found repo in {}ms'.format(e-s))

    s = time.time()
    parser = Statement()
    parsed_stmt = parser.parse(args.query)
    statement_select = parsed_stmt.node['select']
    statement_expr = parsed_stmt.node['expression']
    e = time.time()
    print('Parsed stmt in {}ms'.format(e-s))

    s = time.time()
    res = repo.select(statement_select, statement_expr)
    e = time.time()
    print('Searched for matched runs in {}ms'.format(e-s))

    s = time.time()
    max_num_records = 0
    for run in res.runs:
        run.open_storage()
        for metric in run.metrics.values():
            try:
                metric.open_artifact()
                for trace in metric.traces:
                    if trace.num_records > max_num_records:
                        max_num_records = trace.num_records
            except:
                pass
    e = time.time()
    print('Opened storage and got runs lengths in {}ms'.format(e-s))

    steps = scale_trace_steps(max_num_records, 50)

    s = time.time()
    for run in res.runs:
        for metric in run.metrics.values():
            try:
                # metric.open_artifact()
                for trace in metric.traces:
                    for r in trace.read_records(steps):
                        base, metric_record = MetricArtifact.deserialize_pb(r)
                        trace.append((
                            metric_record.value,  # 0 => value
                            base.step,  # 1 => step
                            (base.epoch if base.has_epoch else None),
                            # 2 => epoch
                            base.timestamp,  # 3 => time
                        ))
            except:
                pass
            finally:
                try:
                    metric.close_artifact()
                except:
                    pass
        run.close_storage()
    e = time.time()
    print('Read runs and closed storage in {}ms'.format(e-s))

    s = time.time()
    runs_list = []
    for run in res.runs:
        runs_list.append(run.to_dict(include_only_selected_agg_metrics=True))
    e = time.time()
    print('Serialized runs in {}ms'.format(e-s))

    # pprint(runs_list)
