import camelot

lattice_tables = camelot.read_pdf(
    str('./output.pdf'), flavor='lattice', line_scale=110)
lattice_tables.export('output.csv', f='excel')
