# qanda.py

### Installation

`python3 -m pip install git+https://github.com/dorbarker/qanda.git`

A simple tool for quering NCBI databases, downloading the results,
and assembling them using a modular assembler backend.

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
```

### External dependencies

- [NCBI Entrez Direct](https://www.ncbi.nlm.nih.gov/books/NBK179288/)
- [NCBI SRA Toolkit](https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?view=toolkit_doc&f=std)