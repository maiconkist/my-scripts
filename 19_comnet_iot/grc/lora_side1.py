#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Lora Side1
# Generated: Thu Feb 28 12:33:23 2019
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fec
from gnuradio import gr
from gnuradio import zeromq
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from optparse import OptionParser
import lora
import math


class lora_side1(gr.top_block):

    def __init__(self, MTU=10000, bw=100e3, frequency_rx=2.4505e9 + 1e6, frequency_tx=2.4505e9, ip_pub='tcp://192.168.5.134:7001', ip_sub='tcp://192.168.5.109:7000', offset=-250e3):
        gr.top_block.__init__(self, "Lora Side1")

        ##################################################
        # Parameters
        ##################################################
        self.MTU = MTU
        self.bw = bw
        self.frequency_rx = frequency_rx
        self.frequency_tx = frequency_tx
        self.ip_pub = ip_pub
        self.ip_sub = ip_sub
        self.offset = offset

        ##################################################
        # Variables
        ##################################################
        self.rep = rep = 3
        self.spreading_factor = spreading_factor = 8
        self.samp_rate = samp_rate = 500e3
        self.ldr = ldr = True
        self.header = header = False


        self.enc_rep = enc_rep = fec.repetition_encoder_make(480, rep)



        self.enc_dummy = enc_dummy = fec.dummy_encoder_make(MTU*8)



        self.enc_ccsds = enc_ccsds = fec.ccsds_encoder_make(MTU*8, 0, fec.CC_TERMINATED)



        self.dec_rep = dec_rep = fec.repetition_decoder.make(480, rep, 0.5)



        self.dec_dummy = dec_dummy = fec.dummy_decoder.make(MTU*8)



        self.dec_cc = dec_cc = fec.cc_decoder.make(8000, 7, 2, ([109,79]), 0, -1, fec.CC_TERMINATED, False)

        self.code_rate = code_rate = 4

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_push_sink_0 = zeromq.push_sink(gr.sizeof_gr_complex, 1, ip_pub, 100, False, -1)
        self.zeromq_pull_source_0 = zeromq.pull_source(gr.sizeof_gr_complex, 1, ip_sub, 100, False, -1)
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
        self.blocks_tuntap_pdu_0 = blocks.tuntap_pdu('tap0', MTU, False)
        self.blocks_message_debug_0 = blocks.message_debug()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tuntap_pdu_0, 'pdus'), (self.lora_encode_0, 'in'))
        self.msg_connect((self.lora_decode_0, 'out'), (self.blocks_message_debug_0, 'print_pdu'))
        self.msg_connect((self.lora_decode_0, 'out'), (self.blocks_tuntap_pdu_0, 'pdus'))
        self.msg_connect((self.lora_demod_0, 'out'), (self.lora_decode_0, 'in'))
        self.msg_connect((self.lora_encode_0, 'out'), (self.lora_mod_0, 'in'))
        self.connect((self.lora_mod_0, 0), (self.pfb_arb_resampler_xxx_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.zeromq_push_sink_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0_0, 0), (self.lora_demod_0, 0))
        self.connect((self.zeromq_pull_source_0, 0), (self.pfb_arb_resampler_xxx_0_0, 0))

    def get_MTU(self):
        return self.MTU

    def set_MTU(self, MTU):
        self.MTU = MTU

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.pfb_arb_resampler_xxx_0_0.set_rate(self.bw/self.samp_rate)
        self.pfb_arb_resampler_xxx_0.set_rate(self.samp_rate/self.bw)

    def get_frequency_rx(self):
        return self.frequency_rx

    def set_frequency_rx(self, frequency_rx):
        self.frequency_rx = frequency_rx

    def get_frequency_tx(self):
        return self.frequency_tx

    def set_frequency_tx(self, frequency_tx):
        self.frequency_tx = frequency_tx

    def get_ip_pub(self):
        return self.ip_pub

    def set_ip_pub(self, ip_pub):
        self.ip_pub = ip_pub

    def get_ip_sub(self):
        return self.ip_sub

    def set_ip_sub(self, ip_sub):
        self.ip_sub = ip_sub

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset

    def get_rep(self):
        return self.rep

    def set_rep(self, rep):
        self.rep = rep

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

    def get_enc_rep(self):
        return self.enc_rep

    def set_enc_rep(self, enc_rep):
        self.enc_rep = enc_rep

    def get_enc_dummy(self):
        return self.enc_dummy

    def set_enc_dummy(self, enc_dummy):
        self.enc_dummy = enc_dummy

    def get_enc_ccsds(self):
        return self.enc_ccsds

    def set_enc_ccsds(self, enc_ccsds):
        self.enc_ccsds = enc_ccsds

    def get_dec_rep(self):
        return self.dec_rep

    def set_dec_rep(self, dec_rep):
        self.dec_rep = dec_rep

    def get_dec_dummy(self):
        return self.dec_dummy

    def set_dec_dummy(self, dec_dummy):
        self.dec_dummy = dec_dummy

    def get_dec_cc(self):
        return self.dec_cc

    def set_dec_cc(self, dec_cc):
        self.dec_cc = dec_cc

    def get_code_rate(self):
        return self.code_rate

    def set_code_rate(self, code_rate):
        self.code_rate = code_rate


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--MTU", dest="MTU", type="intx", default=10000,
        help="Set MTU [default=%default]")
    parser.add_option(
        "", "--frequency-rx", dest="frequency_rx", type="eng_float", default=eng_notation.num_to_str(2.4505e9 + 1e6),
        help="Set frequency_rx [default=%default]")
    parser.add_option(
        "", "--frequency-tx", dest="frequency_tx", type="eng_float", default=eng_notation.num_to_str(2.4505e9),
        help="Set frequency_tx [default=%default]")
    parser.add_option(
        "", "--ip-pub", dest="ip_pub", type="string", default='tcp://192.168.5.134:7001',
        help="Set ip_pub [default=%default]")
    parser.add_option(
        "", "--ip-sub", dest="ip_sub", type="string", default='tcp://192.168.5.109:7000',
        help="Set ip_sub [default=%default]")
    return parser


def main(top_block_cls=lora_side1, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(MTU=options.MTU, frequency_rx=options.frequency_rx, frequency_tx=options.frequency_tx, ip_pub=options.ip_pub, ip_sub=options.ip_sub)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
