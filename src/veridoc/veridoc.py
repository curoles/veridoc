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
                        nargs='*',
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
    parser.add_argument('-f',
                        dest='flist',
                        metavar='FILE',
                        type=argparse.FileType('r'),
                        nargs='+',
                        help='Verilog files list from file')
    parser.add_argument('-F',
                        dest='Flist',
                        metavar='FILE',
                        type=argparse.FileType('r'),
                        nargs='+',
                        help='relative path Verilog files list from file')


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
<h{{hdr_level}} id="module_{{m.path}}">
Module "{{ m.name }}", {{m.path}}
</h{{hdr_level}}>

<h4>Parameters:</h4>
<ul>
{%- for prm in m.generics %}
    <li>
    {{prm.name}}
    {%- if prm.desc %}
    // {{prm.desc}}
    {%- endif %}
    </li>
{% endfor %}
</ul>

<h4>Ports:</h4>
<table style="width:100%">
    <th>Name</th> <th>Direction</th> <th>Type</th> <th>Description</th>
{%- for port in m.ports %}
    <tr>
    <td>{{port.name}}</td> <td>{{port.mode}}</td> <td>{{port.data_type}}</td>
    <td>
    {%- if port.desc %}
    {{port.desc}}
    {%- endif %}
    </td>
    </tr>
{% endfor %}
</table>

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

def normalize_path(modules):
    paths = [os.path.dirname(m.path) for m in modules]
    common_prefix = os.path.commonprefix(paths)
    for m in modules:
        m.path = m.path.replace(common_prefix, '')

    modules.sort(key=lambda m: m.path, reverse=False)

def handle_vlog_file(vlog_file):
    #TODO if not is_verilog_file(vlog_file.name):
    #    return []
    code = vlog_file.read()
    new_modules = parse_vlog(code)
    for new_module in new_modules:
        new_module.path = vlog_file.name

    return new_modules

def process_filelist(args, relative):
    modules = []
    flist = args.Flist if relative else args.flist
    for fl in flist:
        fnames = fl.readlines()
        for fname in fnames:
            #FIXME TODO expand $VAR, $(VAR), ${VAR}
            fpath = fname.rstrip('\n')
            if relative:
                fpath = os.path.join(os.path.dirname(fl.name), fpath)
            with open(fpath, 'r') as vlog_file:
                new_modules = handle_vlog_file(vlog_file)
                modules.extend(new_modules)

    return modules

def main():
    args = parse_args()

    modules = []

    if args.inputs:
        for vlog_file in args.inputs:
            new_modules = handle_vlog_file(vlog_file)
            modules.extend(new_modules)

    if args.flist:
        modules.extend(process_filelist(args, False))

    if args.Flist:
        modules.extend(process_filelist(args, True))

    normalize_path(modules)

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
