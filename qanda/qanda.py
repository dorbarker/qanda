#!/usr/bin/env python3

import functools
import io
import json
import subprocess
from pathlib import Path
from typing import Dict, List, TypeVar

import pandas as pd


def arguments():
    pass


def main():
    pass


# type hints
assembler_dict = Dict[str, str]
PandasDataFrame = TypeVar('pandas.core.frame.DataFrame')


def get_runinfo(query: str, database: str) -> PandasDataFrame:

    search = ('esearch', '-db', database, '-query', query)

    search_result = subprocess.run(search,
                                   check=True,
                                   stdout=subprocess.PIPE)

    if database.lower() != 'sra':

        link = ('elink', '-target', 'sra')

        result = subprocess.run(link,
                                input=search_result.stdout,
                                check=True,
                                stdout=subprocess.PIPE)

    else:

        result = search_result

    fetch = ('efetch', '-format', 'runinfo')

    runinfo = subprocess.run(fetch,
                             input=result.stdout,
                             check=True,
                             stdout=subprocess.PIPE)

    return pd.read_csv(io.BytesIO(runinfo.stdout), header=0)


def build_runinfo_table(queries: List[str], database: str) -> PandasDataFrame:

    runinfo_lines = (get_runinfo(query, database) for query in queries)

    runinfo_table = functools.reduce(pd.DataFrame.append, runinfo_lines)

    return runinfo_table


def download_genome(acc: str, outdir: Path) -> None:

    out = str(outdir)
    fq_dump = ('fastq-dump', '--outdir', out, '--gzip', '--skip-technical',
               '--readids', '--read-filter', 'pass', '--dumpbase',
               '--split-files', '--clip', acc)

    subprocess.run(fq_dump, check=True, stdout=subprocess.DEVNULL)


def load_assembler(directory: Path, assembler: Path) -> assembler_dict:

    assembler_path = directory / assembler

    with assembler_path.open('r') as f:
        assembler_config = json.load(f)

    return assembler_config


def format_config(assembler_config: assembler_dict, options: Dict) -> assembler_dict:

    return {key: value.format(**options)
            for key, value in assembler_config.items()}


if __name__ == '__main__':
    main()
