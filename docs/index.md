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

`veridoc` takes one positional argument `<path>/OAI22.sv` as input file
and outputs generated HTML code to `stdout` that is redirected
to file `example1.html`. Option `-s` tells to generated complete
standalone HTML page.


See [HTML output example1.html](example1.html).
