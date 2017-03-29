#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Spectrum To Binfile
# Generated: Tue Mar 28 18:25:11 2017
##################################################


from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from optparse import OptionParser


class spectrum_to_binfile(gr.top_block):

    def __init__(self, options):
        gr.top_block.__init__(self, "Spectrum To Binfile")

        ##################################################
        # Parameters
        ##################################################
        self.filename = options.filename
        self.samp_rate = options.samp_rate
        self.central_freq = options.central_freq
        self.bandwidth = options.bandwidth
        self.gain = options.gain

        ##################################################
        # Variables
        ##################################################

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(('', "")),
            uhd.stream_args(
                cpu_format="fc32",
                channels=range(1),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_center_freq(self.central_freq, 0)
        self.uhd_usrp_source_0.set_gain(self.gain, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_bandwidth(self.bandwidth, 0)

        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, int(options.samp_rate * options.time))
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex, options.filename, False)
        self.blocks_file_sink_0.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_head_0, 0))


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option("-f", "--filename", type="string", default="iq.bin",
                     help="Output file with captured IQ samples [default=%default]")
    parser.add_option("-c", "--central-freq", type="intx", default=int(2.45e9),
                     help="Center Frequency [default=%default]")
    parser.add_option("-t", "--time", type="intx", default=5,
                     help="Capture duration in seconds [default=%default].")
    parser.add_option("-s", "--samp-rate", type="intx", default=int(4e6),
                     help="Sampling Rate [default=%default]")
    parser.add_option("-b", "--bandwidth", type="intx", default=int(4e6),
                     help="Bandwidth [default=%default]")
    parser.add_option("-g", "--gain", type="intx", default=1,
                     help="USRP gain [default=%default]")
    return parser


def main(top_block_cls=spectrum_to_binfile, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(options)
    tb.start()
    tb.wait()
    tb.stop()

if __name__ == '__main__':
    main()
