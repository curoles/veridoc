---
layout: default
---

Veridoc - Verilog documentation generator
=========================================

*Veridoc* parses Verilog files and extracts information
about Verilog *modules*, including list of ports and parameters.
Block comment **immediately** above declaration of a *module* is treated
as a documentation of the module in Markdown.

Example 1 - Parse one Verilog file
----------------------------------

```terminal
veridoc -s <path>/OAI22.sv > example1.html
```

In this example `veridoc` takes one positional argument `<path>/OAI22.sv` as input file
and outputs generated HTML code to `stdout` that is redirected
to file `example1.html`. Option `-s` tells to generated complete
standalone HTML page.


See [HTML output example1.html](example1.html).

Example 2 - Two files, show source code
---------------------------------------

```terminal
veridoc -s --inline -o example2.html <path>/OAI22.sv <path>/Not.sv
```

- Two positional arguments `<path>/OAI22.sv` and `<path>/Not.sv` tell `veridoc`
  to parse two files.
- `-o example2.html` tells to save output to file `example2.html`.
- `--inline` tells that we want module source code to be embedded in to the
  generated documentation.
- `-s` tells to generate complete standalone HTML page.


See [HTML output example2.html](example2.html).

Example 3 - File with a list of Verilog files, TOC sidebar
----------------------------------------------------------

```terminal
veridoc -s --toc-sidebar -o example3.html -f ./rtl/rtl.flist
```

- instead of listing Verilog files one by one as positional
  arguments we use option `-f ./rtl/rtl.flist` where
  contents of `rtl.flist` is:
  ```
  ./rtl/lib/gates/cmos/Not.sv
  ./rtl/lib/gates/generic/OAI22.sv
  ./rtl/lib/parts/FullAdder.sv
  ./rtl/blocks/Incr3.sv
  ```
- option `--toc-sidebar` tells to show vertical sidebar
  with a list of all *modules*.


See [HTML output example3.html](example3.html).
