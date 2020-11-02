from pygments.formatters import HtmlFormatter

veridoc_css = '''
p {font-family: Verdana, Geneva, sans-serif;}

 /* The sidebar menu */
.sidenav {
  height: 100%; /* Full-height: remove this if you want "auto" height */
  width: 10rem; /* Set the width of the sidebar */
  position: fixed; /* Fixed Sidebar (stay in place on scroll) */
  z-index: 1; /* Stay on top */
  top: 0; /* Stay at the top */
  left: 0;
  background-color: #f0f0f0;
  overflow-x: hidden; /* Disable horizontal scroll */
  padding-top: 1rem;
}

/* The navigation menu links */
.sidenav a {
  padding: 6px 8px 6px 0.5rem;
  text-decoration: none;
  font-size: 1rem;
  color: black;
  display: block;
}

/* When you mouse over the navigation links, change their color */
.sidenav a:hover {
  color: blue;
  background-color: #e0e0e0;
}

/* Active/current link */
.sidenav a:active {
  color: #e0e0e0;
  background-color: blue;
}

/* Style page content */
.main {
  margin-left: 10rem; /* Same as the width of the sidebar */
  padding: 0px 10px;
}

/* On smaller screens, where height is less than 450px,
 * change the style of the sidebar (less padding and a smaller font size)
 */
@media screen and (max-height: 450px) {
  .sidenav {padding-top: 0.5rem;}
  .sidenav a {font-size: 0.5rem;}
}
'''

html_prolog = f'''<!DOCTYPE html html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <title>Verilog documentation</title>

    <link rel="stylesheet" href="https://yarnpkg.com/en/package/normalize.css">

    <!-- see https://github.com/wavedrom/wavedrom -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/wavedrom/2.6.8/skins/default.js" type="text/javascript"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/wavedrom/2.6.8/wavedrom.min.js" type="text/javascript"></script>

    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.22.0/themes/prism.css" rel="stylesheet" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.22.0/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.22.0/plugins/autoloader/prism-autoloader.min.js"></script>

    <style>
    {HtmlFormatter(cssclass='codehilite', style='default').get_style_defs()}
    </style>

    <style>{veridoc_css}</style>
</head>

<body onload="WaveDrom.ProcessAll()">
'''

def render_html_file_prolog(output):
    output.write(html_prolog)

def render_html_file_epilog(output):
    output.write("\n</body></html>\n")

def render_sidebar(output, modules):
    output.write('<div class="sidenav">')
    for m in modules:
        output.write(f'    <a href="#module_{m.path}">{m.name}</a>');
    output.write('</div>')
