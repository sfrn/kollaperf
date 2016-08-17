#from kollaperf.printer import MachinePrinter
#
#printer = MachinePrinter()
#printer.print('hey ;)')

from kollaperf.label import generate_label, print_filename

with open('foo.png', 'wb') as f:
    generate_label('Hello Safran Hello Safran Hello Safran Hello Safran Hello Safran Hello Safran Hello Safran Hallo Safran Frobilausens hey', f)

#print_filename('foo.png')
