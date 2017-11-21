# qanda.py

A simple tool for quering NCBI databases, downloading the results,
and assembling them using a modular assembler backend.

Qanda provides plugins for spades, shovill, and unicycler as
assembler backends.


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

