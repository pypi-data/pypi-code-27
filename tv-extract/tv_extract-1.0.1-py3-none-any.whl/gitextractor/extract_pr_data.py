import csv
import logging
import os

from datetime import datetime

from tv_extract.util import cli, cd
from tv_extract.data import Revision, PullRequest, RevisionGraph
from tv_extract.gitextractor import extract_revision_graph


def extract_pr_data(row_processor, graph: RevisionGraph):
    '''
    Given a revision graph, collect information on Pull Requests to master.

    :param row_processor: function to receive the callback
    :return: None
    '''

    for rev in graph.master_revs:
        revision = graph.revisions[rev]
        if revision.is_a_pr:
            branch_rev: Revision = graph.revisions[revision.branch_parent]
            delta = datetime.utcfromtimestamp(revision.stamp) - datetime.utcfromtimestamp(branch_rev.stamp)
            if delta.total_seconds() < 0:
                # This is happening due to time drift on developers laptops
                logging.debug(f"Unexpected. Negative duration: {rev}")
                row_processor(PullRequest(revision.stamp, revision.hash, revision.author,
                                          graph.linkage[rev], revision.branch_parent, rev, -delta))
            else:
                row_processor(PullRequest(revision.stamp, revision.hash, revision.author,
                                          graph.linkage[rev], revision.branch_parent, rev, delta))


if __name__ == "__main__":
    conf, paths, outputpath = cli.get_cli()
    begin, end = cli.get_begin_end_timestamps(conf)
    with open(outputpath, 'w', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(['repo', 'hash', 'stamp', 'masterRev', 'branchRev', 'prMergeDuration', 'prMergeDurationHr'])

        for path in paths:
            repo_name = os.path.split(path)[1]
            with (cd.cd(path)):
                graph = extract_revision_graph()

                def row_processor(row: PullRequest):
                    if row.stamp >= begin and row.stamp <= end:
                        writer.writerow([repo_name, row.hash, row.stamp, row.master_rev, row.branch_rev, row.duration.total_seconds(), row.duration])
                extract_pr_data(row_processor, graph)
