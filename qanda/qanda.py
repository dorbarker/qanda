#!/usr/bin/env python3

import argparse
import functools
import io
import json
import shlex
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, TypeVar

import pandas as pd

# type hints
assembler_dict = Dict[str, str]
PandasDataFrame = TypeVar('pandas.core.frame.DataFrame')

# constants
assembler_config_dir = Path.home() / '.local' / 'share' / 'qanda'


def arguments():

    def get_assembler_backends():

        return [p.stem for p in assembler_config_dir.glob('*.json')]

    parser = argparse.ArgumentParser()

    parser.add_argument('--assembler',
                        default='shovill',
                        choices=get_assembler_backends(),
                        help='Assembler backend [shovill]')

    parser.add_argument('--database',
                        default='sra',
                        help='NCBI subject database [sra]')

    parser.add_argument('--results',
                        default=Path().resolve(),
                        type=Path,
                        help='Results directory ["."]')

    parser.add_argument('--cores',
                        default=1,
                        type=int,
                        help='Number of CPU cores [1]')

    parser.add_argument('queries',
                        nargs='+',
                        help='NCBI queries')

    return parser.parse_args()


def main():

    args = arguments()

    qanda(args.queries, args.database, args.assembler, args.results, args.cores)


def qanda(queries: List[str], database: str, assembler: str, results: Path, cores: int):

    def setup_directories() -> Tuple[Path, Path, Path]:

        fastq = results / 'fastqs'
        assembly = results / 'assemblies'
        biosample = results / 'biosamples'

        fastq.mkdir(exist_ok=True)
        assembly.mkdir(exist_ok=True)
        biosample.mkdir(exist_ok=True)

        return fastq, assembly, biosample

    fastqs, assemblies, biosamples = setup_directories()

    assembler_config = load_assembler(assembler_config_dir, assembler)

    runinfo = build_runinfo_table(queries, database)

    runinfo.to_csv(results / 'runinfo.csv')

    # for acc in runinfo['Run']:
    #     download_genome(acc, fastqs)

    for acc in runinfo['Run']:
        assemble(acc, fastqs, assemblies, cores, assembler_config)


def get_metadata(query: str, database: str) -> PandasDataFrame:
    # TODO add biosample fetching

    search = ('esearch', '-db', database, '-query', query)

    search_result = subprocess.run(search,
                                   check=True,
                                   stdout=subprocess.PIPE)

    if database.lower() != 'sra':

        sra_link = ('elink', '-target', 'sra')

        sra = subprocess.run(sra_link,
                             input=search_result.stdout,
                             check=True,
                             stdout=subprocess.PIPE)

    else:

        sra = search_result

    fetch = ('efetch', '-format', 'runinfo')

    runinfo = subprocess.run(fetch,
                             input=sra.stdout,
                             check=True,
                             stdout=subprocess.PIPE)

    return pd.read_csv(io.BytesIO(runinfo.stdout), header=0)


def build_runinfo_table(queries: List[str], database: str) -> PandasDataFrame:

    runinfo_lines = (get_metadata(query, database) for query in queries)

    runinfo_table = functools.reduce(pd.DataFrame.append, runinfo_lines)

    return runinfo_table


def download_genome(acc: str, outdir: Path) -> None:

    out = str(outdir)
    fq_dump = ('fastq-dump', '--outdir', out, '--gzip', '--skip-technical',
               '--readids', '--read-filter', 'pass', '--dumpbase',
               '--origfmt', '--split-files', '--clip', acc)

    subprocess.run(fq_dump, check=True, stdout=subprocess.DEVNULL)


def load_assembler(directory: Path, assembler: str) -> assembler_dict:

    assembler_path = directory / assembler

    with assembler_path.with_suffix('.json').open('r') as f:
        assembler_config = json.load(f)

    return assembler_config


def assemble(accession: str, fastqs: Path, assemblies: Path, cores: int,
             assembler_config: assembler_dict):

    fastq_template = '{}_pass_{{}}.fastq.gz'.format(accession)

    options = {
        'fwd':      fastqs / fastq_template.format(1),
        'rev':      fastqs / fastq_template.format(2),
        'outdir':   assemblies / accession,
        'cores':    cores,
    }

    formatted_options = {key: value.format(**options)
                         for key, value in assembler_config.items()
                         if value}

    for cmd in formatted_options:

        subprocess.run(shlex.split(formatted_options[cmd]), check=True)


if __name__ == '__main__':
    main()
