#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Ansible Hydra Lora Side1
# Generated: Fri Mar  1 16:34:55 2019
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from optparse import OptionParser
import hydra
import lora
import math
import threading


class ansible_hydra_lora_side1(gr.top_block):

    def __init__(self, ansibleFreqRx=0, ansibleFreqTx=0, ansibleHostIP='192.168.5.134', ansibleID='0', ansibleServerIP='192.168.5.134', bw=250e3, offset=-250e3):
        gr.top_block.__init__(self, "Ansible Hydra Lora Side1")

        ##################################################
        # Parameters
        ##################################################
        self.ansibleFreqRx = ansibleFreqRx
        self.ansibleFreqTx = ansibleFreqTx
        self.ansibleHostIP = ansibleHostIP
        self.ansibleID = ansibleID
        self.ansibleServerIP = ansibleServerIP
        self.bw = bw
        self.offset = offset

        ##################################################
        # Variables
        ##################################################
        self.spreading_factor = spreading_factor = 8
        self.samp_rate = samp_rate = 1e6
        self.ldr = ldr = True
        self.header = header = False
        self.code_rate = code_rate = 4

        ##################################################
        # Blocks
        ##################################################
        self.pfb_arb_resampler_xxx_0_0 = pfb.arb_resampler_ccf(
        	  bw/samp_rate,
                  taps=None,
        	  flt_size=32)
        self.pfb_arb_resampler_xxx_0_0.declare_sample_delay(0)

        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_ccf(
        	  samp_rate/bw,
                  taps=None,
        	  flt_size=32)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(0)

        self.lora_mod_0 = lora.mod(spreading_factor, 0x12)
        self.lora_encode_0 = lora.encode(spreading_factor, code_rate, ldr, header)
        self.lora_demod_0 = lora.demod(spreading_factor, ldr, 25.0, 2)
        self.lora_decode_0 = lora.decode(spreading_factor, code_rate, ldr, header)
        self.hydra_gr_network_source_0 = hydra.hydra_gr_client_network_source(int(ansibleID), ansibleHostIP, 5000, ansibleServerIP)
        self.hydra_gr_network_source_0.start_client(ansibleFreqRx + samp_rate/2 + (samp_rate * int(ansibleID)), samp_rate, 10000)

        self.hydra_gr_network_sink_0 = hydra.hydra_gr_client_network_sink(int(ansibleID), ansibleHostIP, 5000, ansibleServerIP)
        self.hydra_gr_network_sink_0.start_client(ansibleFreqTx + samp_rate/2 + (samp_rate * int(ansibleID)), samp_rate, 5000)
        self.blocks_tuntap_pdu_0 = blocks.tuntap_pdu('tap0', 1000, False)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tuntap_pdu_0, 'pdus'), (self.lora_encode_0, 'in'))
        self.msg_connect((self.lora_decode_0, 'out'), (self.blocks_tuntap_pdu_0, 'pdus'))
        self.msg_connect((self.lora_demod_0, 'out'), (self.lora_decode_0, 'in'))
        self.msg_connect((self.lora_encode_0, 'out'), (self.lora_mod_0, 'in'))
        self.connect((self.hydra_gr_network_source_0, 0), (self.pfb_arb_resampler_xxx_0_0, 0))
        self.connect((self.lora_mod_0, 0), (self.pfb_arb_resampler_xxx_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.hydra_gr_network_sink_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0_0, 0), (self.lora_demod_0, 0))

    def get_ansibleFreqRx(self):
        return self.ansibleFreqRx

    def set_ansibleFreqRx(self, ansibleFreqRx):
        self.ansibleFreqRx = ansibleFreqRx

    def get_ansibleFreqTx(self):
        return self.ansibleFreqTx

    def set_ansibleFreqTx(self, ansibleFreqTx):
        self.ansibleFreqTx = ansibleFreqTx

    def get_ansibleHostIP(self):
        return self.ansibleHostIP

    def set_ansibleHostIP(self, ansibleHostIP):
        self.ansibleHostIP = ansibleHostIP

    def get_ansibleID(self):
        return self.ansibleID

    def set_ansibleID(self, ansibleID):
        self.ansibleID = ansibleID

    def get_ansibleServerIP(self):
        return self.ansibleServerIP

    def set_ansibleServerIP(self, ansibleServerIP):
        self.ansibleServerIP = ansibleServerIP

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.pfb_arb_resampler_xxx_0_0.set_rate(self.bw/self.samp_rate)
        self.pfb_arb_resampler_xxx_0.set_rate(self.samp_rate/self.bw)

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset

    def get_spreading_factor(self):
        return self.spreading_factor

    def set_spreading_factor(self, spreading_factor):
        self.spreading_factor = spreading_factor

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.pfb_arb_resampler_xxx_0_0.set_rate(self.bw/self.samp_rate)
        self.pfb_arb_resampler_xxx_0.set_rate(self.samp_rate/self.bw)

    def get_ldr(self):
        return self.ldr

    def set_ldr(self, ldr):
        self.ldr = ldr

    def get_header(self):
        return self.header

    def set_header(self, header):
        self.header = header

    def get_code_rate(self):
        return self.code_rate

    def set_code_rate(self, code_rate):
        self.code_rate = code_rate


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--ansibleFreqRx", dest="ansibleFreqRx", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set ansibleFreqRx [default=%default]")
    parser.add_option(
        "", "--ansibleFreqTx", dest="ansibleFreqTx", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set ansibleFreqTx [default=%default]")
    parser.add_option(
        "", "--ansibleHostIP", dest="ansibleHostIP", type="string", default='192.168.5.134',
        help="Set ansibleHostIP [default=%default]")
    parser.add_option(
        "", "--ansibleID", dest="ansibleID", type="string", default='0',
        help="Set ansibleID [default=%default]")
    parser.add_option(
        "", "--ansibleServerIP", dest="ansibleServerIP", type="string", default='192.168.5.134',
        help="Set ansibleServerIP [default=%default]")
    parser.add_option(
        "", "--bw", dest="bw", type="eng_float", default=eng_notation.num_to_str(250e3),
        help="Set bw [default=%default]")
    return parser


def main(top_block_cls=ansible_hydra_lora_side1, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(ansibleFreqRx=options.ansibleFreqRx, ansibleFreqTx=options.ansibleFreqTx, ansibleHostIP=options.ansibleHostIP, ansibleID=options.ansibleID, ansibleServerIP=options.ansibleServerIP, bw=options.bw)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
