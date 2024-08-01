#
# px41cx_hex2bmp.py - read hex format screenshots from PX41CX serial log file and save
#                     to multiple BMP files
#
# Usage: px41cx_hex2bmp.py [-h] infile outfile
# 
# Extract screenshots from PX41CX terminal log file.
# 
# positional arguments:
#   infile      log of PX41CX serial connection containing hex encoded screenshots
#   outfile     BMP filename prefix, file count will be added as nn. Existing files will
#               be overwritten.
# 
# optional arguments:
#   -h, --help  show this help message and exit
# 

#
# Copyright (c) 2024 Darren Hosking @calculatorclique https://github.com/diemheych
# 
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.
#

import argparse
import sys
from microbmp import MicroBMP

def access_bit(data, num):
    base = int(num // 8)
    shift = int(num % 8)
    return (data[base] >> shift) & 0x1

def create_bmp(filename, hexdata, num):

    ba = bytearray.fromhex(hexdata.decode())
    bmp = MicroBMP(250,122,1)
    for y in range(122):
        for x in range(250):
            bit = 23 - 2 * (y % 12) - x % 2
            byte = 375 * (y // 12) + (x // 2) * 3 
            yy = y % 12
            if yy > 7:
                newy = y - 8
            elif yy < 4:
                newy = y + 8
            else:
                newy = y
            if newy > 121:
                newy = y
            bmp[x, newy] = access_bit(ba, byte * 8 + bit)
    bmpname = filename + "{:02d}".format(num) + ".bmp"
    print(bmpname)
    bmp.save(bmpname)

def main():

    parser = argparse.ArgumentParser(description='Extract screenshots from PX41CX terminal log file.')
    parser.add_argument('infile',help='log of PX41CX serial connection containing hex encoded screenshots')
    parser.add_argument('outfile',help='BMP filename prefix, file count will be added as nn. Existing files will be overwritten.')
    args = vars(parser.parse_args())
    counter = 0
    try:
        f = open(args['infile'], "rb")
    except:
        print("Error reading hex file:",args['infile'])
        exit(1)

    for line in f:
        if b'DISP' in line:
            counter += 1
            line = f.readline()
            create_bmp(args['outfile'],line, counter)

    f.close()
    return 0

if __name__ == '__main__':
    sys.exit(main())
