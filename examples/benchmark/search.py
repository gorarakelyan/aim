from pprint import pprint
import time

from aim.engine.repo.repo import AimRepo
from aim.ql.grammar.statement import Statement


if __name__ == '__main__':
    # Get repo
    s = time.time()
    repo = AimRepo.get_working_repo(mode='r')
    e = time.time()

    print('Found repo in {}ms'.format(e-s))

    query = 'metric_2, metric ' \
            ' if experiment is not None'

    s = time.time()
    parser = Statement()
    parsed_stmt = parser.parse(query)
    statement_select = parsed_stmt.node['select']
    statement_expr = parsed_stmt.node['expression']
    e = time.time()

    print('Parsed stmt in {}ms'.format(e-s))

    s = time.time()
    res = repo.select(statement_select, statement_expr)
    e = time.time()

    print('Searched for matched runs in {}ms'.format(e-s))

    s = time.time()
    runs_list = []
    for run in res.runs:
        runs_list.append(run.to_dict(include_only_selected_agg_metrics=True))
    e = time.time()

    print('Read runs params & configs in {}ms'.format(e-s))

    pprint(runs_list)
