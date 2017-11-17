#!/usr/bin/env python3

import argparse
import functools
import io
import json
import logging
import subprocess

import pandas as pd

def arguments():
    pass

def main():
    pass

def get_runinfo(query_string, database):

    query = ('esearch', '-db', database, '-query', query_string)

    query_result = subprocess.run(query,
                                  check=True,
                                  stdout=subprocess.PIPE)

    if database.lower() != 'sra':

        link = ('elink', '-target', 'sra')

        result = subprocess.run(link,
                                input=query_result.stdout,
                                check=True,
                                stdout=subprocess.PIPE)

    else:

        result = query_result

    fetch = ('efetch', '-format', 'runinfo')

    runinfo = subprocess.run(fetch,
                             input=result.stdout,
                             check=True,
                             stdout=subprocess.PIPE)

    return pd.read_csv(io.BytesIO(runinfo.stdout), header=0)


def build_runinfo_table(queries, database):


    runinfo_lines = (get_runinfo(query, database) for query in queries)

    runinfo_table = functools.reduce(pd.DataFrame.append, runinfo_lines)

    return runinfo_table


def download_genome(acc, outdir):

    fq_dump = ('fastq-dump', '--outdir', outdir, '--gzip', '--skip-technical',
               '--readids', '--read-filter', 'pass', '--dumpbase',
               '--split-files', '--clip', acc)

    subprocess.run(fq_dump, check=True, stdout=subprocess.DEVNULL)

if __name__ == '__main__':
    main()
