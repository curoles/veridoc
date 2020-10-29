import verilog_parser as parser

vlog = parser.VerilogExtractor()

code = """
//# metaco
module igor
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

modules = vlog.extract_objects_from_source(code)

for m in modules:
    print(f'Module "{m.name}":')
    print(f'{m.desc}')

    print('\n    Parameters:')
    for prm in m.generics:
        print(f'        {prm.name:8} {prm.mode:8} {prm.data_type}')

    print('\n    Ports:')
    for port in m.ports:
        print(f'        {port.name:8} {port.mode:8} {port.data_type}')

    print(f'{m.sections}')
    #for bc in m.block_comment:
    #    print('bc')
