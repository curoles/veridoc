#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, markdown
from jinja2 import Template
import verilog_parser as parser


code = """
/* block
 * comment
 * 2
 *
 * ```verilog
 * module M()
 * ```
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

# Inspired by os.path.commonprefix
#
def common_space_prefix(m):
    """Given a list of strings,
        returns the longest common leading component with space characters"""

    if not m: return ''

    # start with a string that is first string in the input list,
    # we also are interested only in space characters
    prefix = re.findall(r'^\s+|$', m[0])[0]

    for item in m:
        if re.search(r'^\s*$', item):
            continue
        for i in range(len(prefix)):
            if prefix[:i+1] != item[:i+1]:
                prefix = prefix[:i]
                if i == 0:
                    return ''
                break
    return prefix

def convert_module_comment_md2html(md_text):
    common_prefix = common_space_prefix(md_text.splitlines())
    md_text = re.sub(r'^'+common_prefix, '', md_text, flags=re.MULTILINE)

    html = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])

    return html


module_html_template = '''
<h{{hdr_level}}>Module "{{ m.name }}"</h{{hdr_level}}>

<pre>
    Parameters:
    {%- for prm in m.generics %}
        {{'%-8s'|format(prm.name)}} {{'%-8s'|format(prm.mode)}} {{prm.data_type -}}
    {% endfor %}

    Portd:
    {%- for port in m.ports %}
        {{'%-8s'|format(port.name)}} {{'%-8s'|format(port.mode)}} {{port.data_type -}}
    {% endfor %}
</pre>

{{mdesc}}
'''

def render_html_doc_module(module):
    template = Template(module_html_template)

    mdesc = convert_module_comment_md2html(module.desc)

    params = {'hdr_level': '3', 'm': module, 'mdesc': mdesc}
    print(template.render(params))

def render_html_doc_file(modules):
    for m in modules:
        render_html_doc_module(m)

def parse_vlog(code):
    vlog = parser.VerilogExtractor()
    modules = vlog.extract_objects_from_source(code)
    return modules

modules = parse_vlog(code)
render_html_doc_file(modules)
