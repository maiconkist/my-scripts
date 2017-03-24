#!/usr/bin/python2
#!/usr/bin/env python
#
# Copyright 2005,2006,2011,2013 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr
from gnuradio.digital import ofdm_mod
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import threading
import numpy
import time


class SinkInputCounter(gr.sync_block):

    def __init__(self):
        gr.sync_block.__init__(self,
            name="sink",
            in_sig=[numpy.complex64],
            out_sig=None)

        self.tsamples = 0

    def reset(self):
        print "------------------------------"
        print '| Samples received: ' + str(self.tsamples)
        print "------------------------------"
        self.tsamples =0

    def work(self, input_items, output_items):
        in0 = input_items[0]
        for i in in0:
            print self.tsamples
            self.tsamples += 1

        return len(in0)

class my_top_block(gr.top_block):
    def __init__(self, options):
        gr.top_block.__init__(self)

        self.txpath = ofdm_mod(options, msgq_limit=1, pad_for_usrp=True)
        self.sp = SinkInputCounter()

        self.connect(self.txpath, self.sp)


# /////////////////////////////////////////////////////////////////////////////
#                                   main
# /////////////////////////////////////////////////////////////////////////////
def main(options):


    tb = my_top_block(options)
    tb.start(1)                       # start flow graph
    time.sleep(2)
    return tb

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, conflict_handler="resolve")
    parser.add_option("-p", "--pkt-size", type="intx", default=1000,
            help="Packet Size [default=%default]")
    parser.add_option("", "--verbose", action="store_true", default=False,
            help="Verbose [default=%default]")
    parser.add_option("", "--log", action="store_true", default=False,
            help="Log [default=%default]")
    parser.add_option("", "--burst", action="store_true",default=False,
            help="Burst mode [default=%default]")
    ofdm_mod.add_options(parser, parser)
    (options, args) = parser.parse_args()


    tb = main(options)

    import struct
    packet = struct.pack('!H', 0xaaaa) + "".join([chr(0xff & x) for x in range(options.pkt_size)])

    for i in range(5):
        print "Pkt " + str(i)
        tb.txpath.send_pkt( packet )

        if not options.burst:
            time.sleep(10)
            tb.sp.reset()

    if options.burst:
        time.sleep(1)
        tb.sp.reset()

    try:
       tb.wait()
    except KeyboardInterrupt:
       print "Closing ..."
