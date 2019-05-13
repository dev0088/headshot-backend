
parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument(
    '--font',
    '-f',
    default='Courier',
    help='Select a font (True Type format) by its full path')
parser.add_argument(
    '--font-size',
    '-s',
    type=float,
    default=10.0,
    help='Size of the font')
parser.add_argument(
    '--extra-vertical-space',
    '-v',
    type=float,
    default=0.0,
    help='Extra vertical space between lines')
parser.add_argument(
    '--kerning',
    '-k',
    type=float,
    default=0.0,
    help='Extra horizontal space between characters')
parser.add_argument(
    '--media',
    '-m',
    default='A4',
    help='Select the size of the page (A4, A3, etc.)')
parser.add_argument(
    '--minimum-page-length',
    '-M',
    type=int,
    default=10,
    help='The minimum number of lines before a form feed character will change the page')
parser.add_argument(
    '--landscape',
    '-l',
    action="store_true",
    default=False,
    help='Select landscape mode')
parser.add_argument(
    '--margin-left',
    '-L',
    type=float,
    default=2.0,
    help='Left margin (in cm unit)')
parser.add_argument(
    '--margin-right',
    '-R',
    type=float,
    default=2.0,
    help='Right margin (in cm unit)')
parser.add_argument(
    '--margin-top',
    '-T',
    type=float,
    default=2.0,
    help='Top margin (in cm unit)')
parser.add_argument(
    '--margin-bottom',
    '-B',
    type=float,
    default=2.0,
    help='Bottom margin (in cm unit)')
parser.add_argument(
    '--output',
    '-o',
    default='output.pdf',
    help='Output file')
parser.add_argument(
    '--author',
    default='',
    help='Author of the PDF document')
parser.add_argument(
    '--title',
    default='',
    help='Title of the PDF document')
parser.add_argument(
    '--quiet',
    '-q',
    action='store_true',
    default=False,
    help='Hide detailed information')
parser.add_argument('--subject',default='',help='Subject of the PDF document')
parser.add_argument('--keywords',default='',help='Keywords of the PDF document')
parser.add_argument(
    '--break-on-blanks',
    '-b',
    action='store_true',
    default=False,
    help='Only break page on blank lines')
parser.add_argument(
    '--encoding',
    '-e',
    type=str,
    default='utf8',
    help='Input encoding')
parser.add_argument(
    '--page-numbers',
    '-n',
    action='store_true',
    help='Add page numbers')
parser.add_argument(
    '--line-numbers',
    action='store_true',
    help='Add line numbers')

args = parser.parse_args()

PDFCreator(args, Margins(
    args.margin_right,
    args.margin_left,
    args.margin_top,
    args.margin_bottom)).generate()