#from kollaperf.printer import MachinePrinter
#
#printer = MachinePrinter()
#printer.print('hey ;)')

from kollaperf.label import generate_label, print_filename

with open('foo.png', 'wb') as f:
    generate_label('I wish the other @wmata lines had information booths like I saw at Ballston. Their wonderful employees Stanley&Lopez made my anxiety go away I wish the other @wmata lines had information booths like I saw at Ballston. Their wonderful employees Stanley&Lopez made my anxiety go away', f)

#print_filename('foo.png')
