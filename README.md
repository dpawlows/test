# test

This repository includes a simple parser for an ozone model input file.

## Usage

Create an input file named `input.ozone` with sections beginning with a `#`.
Example:

```
#TIME
07    start time
12.   end time

#TOPBOUNDARY
100
```

Run the parser:

```
python parser.py input.ozone
```
