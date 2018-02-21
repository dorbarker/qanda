# qanda.py

### Installation

`python3 -m pip install git+https://github.com/dorbarker/qanda.git`

A simple tool for querying NCBI databases, downloading the results,
and assembling them using a modular assembler backend all in a single command.

Qanda provides plugins for spades, shovill, and unicycler as
assembler backends. These plugins describe three commands which can be used to
handle setup, assembly, and cleanup. Any files matching
`~/.local/share/qanda/*.json` are available to Qanda.

```json
{
  "pre":     "Setup or preparation to be executed before assembly",
  "command": "Command controlling the actual call to the assembler",
  "post":    "Any post-assembly cleanup or modification"
}
```

The following variables are currently made available to the assembler plugins,
and can be accessed using Python's string formatting syntax:

```json
{
  "fwd":    "Path to the forward reads",
  "rev":    "Path to the reverse reads",
  "cores":  "Count of CPU cores to be used",
  "outdir": "Directory to which to write the results"
}
```

An example of this in use:

#### shovill.json
```json
{
  "pre": null,
  "command": "shovill --outdir {outdir} --R1 {fwd} --R2 {rev} --cpus {cores}",
  "post": null
}
```

### Usage

```
usage: qanda [-h] [--assembler {shovill,unicycler,spades}]
             [--database DATABASE] [--results RESULTS] [--cores CORES]
             queries [queries ...]

positional arguments:
  queries               NCBI queries

optional arguments:
  -h, --help            show this help message and exit
  --assembler {shovill,unicycler,spades}
                        Assembler backend [shovill]
  --database DATABASE   NCBI subject database [sra]
  --results RESULTS     Results directory ["."]
  --cores CORES         Number of CPU cores [1]
  --email EMAIL         Email address required by NCBI
```

```
qanda --assembler spades --results ~/Desktop/qanda_test/ --database biosample --cores 24 SAMN07646583 SAMN07646584
```

### Dependencies
Program versions listed below are merely minimum tested versions.
Other versions may work as well.

- Python 3.5
    - pandas 0.21.0
    - biopython 1.70
