#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Ansible Hydra Gr Client 1Tx 1Rx
# Generated: Tue Feb 19 11:03:52 2019
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


class ansible_hydra_gr_client_1tx_1rx(gr.top_block):

    def __init__(self, ansibleFreqRx=919.75e6, ansibleFreqTx=919.75e6, ansibleID='1', ansibleIP='notValid', bw=250e3, offset=-250e3):
        gr.top_block.__init__(self, "Ansible Hydra Gr Client 1Tx 1Rx")

        ##################################################
        # Parameters
        ##################################################
        self.ansibleFreqRx = ansibleFreqRx
        self.ansibleFreqTx = ansibleFreqTx
        self.ansibleID = ansibleID
        self.ansibleIP = ansibleIP
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
        self.hydra_gr_sink_0 = hydra.hydra_gr_client_sink(int(ansibleID), ansibleIP, 5000)
        self.hydra_gr_sink_0.start_client(ansibleFreqTx + samp_rate/2 + (samp_rate * int(ansibleID)), samp_rate, 1000)
        self.hydra_gr__source_0 = hydra.hydra_gr_client_source(int(ansibleID), ansibleIP, ansibleIP, 5000)
        self.hydra_gr__source_0.start_client(ansibleFreqRx + samp_rate/2 + (samp_rate * int(ansibleID)), samp_rate, 1000)

        self.blocks_tuntap_pdu_0 = blocks.tuntap_pdu('tap0', 1000, False)
        self.blocks_rotator_cc_0_0 = blocks.rotator_cc((2 * math.pi * offset) / samp_rate)
        self.blocks_rotator_cc_0 = blocks.rotator_cc((2 * math.pi * offset) / samp_rate)
        self.blocks_message_debug_0_0 = blocks.message_debug()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tuntap_pdu_0, 'pdus'), (self.lora_encode_0, 'in'))
        self.msg_connect((self.lora_decode_0, 'out'), (self.blocks_tuntap_pdu_0, 'pdus'))
        self.msg_connect((self.lora_demod_0, 'out'), (self.lora_decode_0, 'in'))
        self.msg_connect((self.lora_encode_0, 'out'), (self.lora_mod_0, 'in'))
        self.connect((self.blocks_rotator_cc_0, 0), (self.pfb_arb_resampler_xxx_0, 0))
        self.connect((self.blocks_rotator_cc_0_0, 0), (self.pfb_arb_resampler_xxx_0_0, 0))
        self.connect((self.hydra_gr__source_0, 0), (self.blocks_rotator_cc_0_0, 0))
        self.connect((self.lora_mod_0, 0), (self.blocks_rotator_cc_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.hydra_gr_sink_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0_0, 0), (self.lora_demod_0, 0))

    def get_ansibleFreqRx(self):
        return self.ansibleFreqRx

    def set_ansibleFreqRx(self, ansibleFreqRx):
        self.ansibleFreqRx = ansibleFreqRx

    def get_ansibleFreqTx(self):
        return self.ansibleFreqTx

    def set_ansibleFreqTx(self, ansibleFreqTx):
        self.ansibleFreqTx = ansibleFreqTx

    def get_ansibleID(self):
        return self.ansibleID

    def set_ansibleID(self, ansibleID):
        self.ansibleID = ansibleID

    def get_ansibleIP(self):
        return self.ansibleIP

    def set_ansibleIP(self, ansibleIP):
        self.ansibleIP = ansibleIP

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
        self.blocks_rotator_cc_0_0.set_phase_inc((2 * math.pi * self.offset) / self.samp_rate)
        self.blocks_rotator_cc_0.set_phase_inc((2 * math.pi * self.offset) / self.samp_rate)

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
        self.blocks_rotator_cc_0_0.set_phase_inc((2 * math.pi * self.offset) / self.samp_rate)
        self.blocks_rotator_cc_0.set_phase_inc((2 * math.pi * self.offset) / self.samp_rate)

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
        "", "--ansibleFreqRx", dest="ansibleFreqRx", type="eng_float", default=eng_notation.num_to_str(919.75e6),
        help="Set ansibleFreqRx [default=%default]")
    parser.add_option(
        "", "--ansibleFreqTx", dest="ansibleFreqTx", type="eng_float", default=eng_notation.num_to_str(919.75e6),
        help="Set ansibleFreqTx [default=%default]")
    parser.add_option(
        "", "--ansibleID", dest="ansibleID", type="string", default='1',
        help="Set 1 [default=%default]")
    parser.add_option(
        "", "--ansibleIP", dest="ansibleIP", type="string", default='notValid',
        help="Set notValid [default=%default]")
    parser.add_option(
        "", "--bw", dest="bw", type="eng_float", default=eng_notation.num_to_str(250e3),
        help="Set bw [default=%default]")
    return parser


def main(top_block_cls=ansible_hydra_gr_client_1tx_1rx, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(ansibleFreqRx=options.ansibleFreqRx, ansibleFreqTx=options.ansibleFreqTx, ansibleID=options.ansibleID, ansibleIP=options.ansibleIP, bw=options.bw)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
