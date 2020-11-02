#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) Igor Lesik 2020

import sys, os, re, markdown, argparse
from jinja2 import Template
import verilog_parser as parser
import render_html

def parse_args():
    parser = argparse.ArgumentParser(description='Generate Verilog documentation.')
    parser.add_argument('inputs',
                        #dest='inputs',
                        metavar='FILE',
                        type=argparse.FileType('r'),
                        nargs='+',
                        help='Verilog file(s)')
    parser.add_argument('-o', '--output',
                        required=False,
                        dest='output',
                        nargs='?',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        metavar='FILE',
                        help='output file')
    parser.add_argument('-s', '--standalone',
                        dest='standalone',
                        required=False,
                        default=False,
                        action='store_true',
                        help='produce standalone HTML file')
    parser.add_argument('--inline',
                        dest='inline',
                        required=False,
                        default=False,
                        action='store_true',
                        help='embed Verilog source code')
    parser.add_argument('--toc-sidebar',
                        dest='toc_sidebar',
                        required=False,
                        default=False,
                        action='store_true',
                        help='show TOC in sidebar')


    args = parser.parse_args()

    return args



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
<h{{hdr_level}} id="module_{{m.name}}">
Module "{{ m.name }}"
</h{{hdr_level}}>

<pre>
Parameters:
{%- for prm in m.generics %}
    {{'%-8s'|format(prm.name)}} {{'%-8s'|format(prm.mode)}} {{prm.data_type -}}
{% endfor %}

Ports:
{%- for port in m.ports %}
    {{'%-8s'|format(port.name)}} {{'%-8s'|format(port.mode)}} {{port.data_type -}}
{% endfor %}
</pre>

{{mdesc}}

{%- if show_source %}
<p>Source code:</p>
<pre><code class="lang-verilog">{{ m.body }}</code></pre>
{% endif %}

<hr />
'''


def render_html_doc_module(output, module, show_source=False):
    template = Template(module_html_template)

    mdesc = convert_module_comment_md2html(module.desc)

    params = {'hdr_level': '3', 'm': module, 'mdesc': mdesc, 'show_source': show_source}
    output.write(template.render(params))

def render_html_doc_file(
    output,
    modules,
    standalone=False,
    show_source=False,
    toc_sidebar=False
):
    if standalone:
        render_html.render_html_file_prolog(output)
        if toc_sidebar:
            render_html.render_sidebar(output, modules)
            output.write('<div class="main">')

    for m in modules:
        render_html_doc_module(output, m, show_source)

    if standalone:
        if toc_sidebar:
            output.write('</div>')
        render_html.render_html_file_epilog(output)

def parse_vlog(code):
    vlog = parser.VerilogExtractor()
    modules = vlog.extract_objects_from_source(code)
    return modules

def main():
    args = parse_args()

    modules = []

    for vlog_file in args.inputs:
        #TODO if not is_verilog_file(vlog_file.name):
        #    continue
        code = vlog_file.read()
        new_modules = parse_vlog(code)
        #TODO for new_module in new_modules:
        #    new_module.path = vlog_file.name
        modules.extend(new_modules)

    if modules:
        render_html_doc_file(
            output=args.output,
            modules=modules,
            standalone=args.standalone,
            show_source=args.inline,
            toc_sidebar=args.toc_sidebar
        )
        args.output.flush()


if __name__ == "__main__":
    main()
