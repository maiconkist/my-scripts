#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Ansible Hydra Gr Server
# Generated: Thu Feb 28 17:07:28 2019
##################################################

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import hydra
import threading


class ansible_hydra_gr_server(gr.top_block):

    def __init__(self, ansibleFreqRx='2.4555e9', ansibleFreqTx='2.4505e9', ansibleIP='192.168.5.134:5000'):
        gr.top_block.__init__(self, "Ansible Hydra Gr Server")

        ##################################################
        # Parameters
        ##################################################
        self.ansibleFreqRx = ansibleFreqRx
        self.ansibleFreqTx = ansibleFreqTx
        self.ansibleIP = ansibleIP

        ##################################################
        # Blocks
        ##################################################
        self.ahydra_gr_server_0 = hydra.hydra_gr_server(ansibleIP)
        if float(ansibleFreqTx) > 0 and 2e6 > 0 and 2048 > 0:
           self.ahydra_gr_server_0.set_tx_config(float(ansibleFreqTx), 2e6, 2048, "USRP")
        if float(ansibleFreqRx) > 0 and 2e6 > 0 and 2048 > 0:
           self.ahydra_gr_server_0.set_rx_config(float(ansibleFreqRx), 2e6, 2048, "USRP")
        self.ahydra_gr_server_0_thread = threading.Thread(target=self.ahydra_gr_server_0.start_server)
        self.ahydra_gr_server_0_thread.daemon = True
        self.ahydra_gr_server_0_thread.start()

    def get_ansibleFreqRx(self):
        return self.ansibleFreqRx

    def set_ansibleFreqRx(self, ansibleFreqRx):
        self.ansibleFreqRx = ansibleFreqRx

    def get_ansibleFreqTx(self):
        return self.ansibleFreqTx

    def set_ansibleFreqTx(self, ansibleFreqTx):
        self.ansibleFreqTx = ansibleFreqTx

    def get_ansibleIP(self):
        return self.ansibleIP

    def set_ansibleIP(self, ansibleIP):
        self.ansibleIP = ansibleIP


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--ansibleFreqRx", dest="ansibleFreqRx", type="string", default='2.4555e9',
        help="Set ansibleFreqRx [default=%default]")
    parser.add_option(
        "", "--ansibleFreqTx", dest="ansibleFreqTx", type="string", default='2.4505e9',
        help="Set ansibleFreqTx [default=%default]")
    parser.add_option(
        "", "--ansibleIP", dest="ansibleIP", type="string", default='192.168.5.134:5000',
        help="Set ansibleIP [default=%default]")
    return parser


def main(top_block_cls=ansible_hydra_gr_server, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(ansibleFreqRx=options.ansibleFreqRx, ansibleFreqTx=options.ansibleFreqTx, ansibleIP=options.ansibleIP)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
