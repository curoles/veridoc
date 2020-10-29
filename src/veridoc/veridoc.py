#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from jinja2 import Template
import verilog_parser as parser


code = """
/* block
 * comment
 * 2
 */
module Module1
#(
    parameter WIDTH = 64
)
(
    input wire clk, // clock signal
    input wire rst, //# {meta1}
    //# {meta2}
    input wire [WIDTH-1:0] a
)

endmodule
"""


module_html_template = '''
Module "{{ m.name }}":
{{m.desc}}

    Parameters:
    {%- for prm in m.generics %}
        {{'%-8s'|format(prm.name)}} {{'%-8s'|format(prm.mode)}} {{prm.data_type -}}
    {% endfor %}

    Portd:
    {%- for port in m.ports %}
        {{'%-8s'|format(port.name)}} {{'%-8s'|format(port.mode)}} {{port.data_type -}}
    {% endfor %}
'''

def render_html_doc_file(modules):
    template = Template(module_html_template)
 
    for m in modules:
        params = {'m': m}
        print(template.render(params))

def parse_vlog(code):
    vlog = parser.VerilogExtractor()
    modules = vlog.extract_objects_from_source(code)
    return modules

modules = parse_vlog(code)
render_html_doc_file(modules)
