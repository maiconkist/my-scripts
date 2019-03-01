#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Ansible Hydra Server Side1
# Generated: Fri Mar  1 16:34:15 2019
##################################################

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import hydra
import threading


class ansible_hydra_server_side1(gr.top_block):

    def __init__(self, ansibleFreqRx='2e6', ansibleFreqTx='2e6', ansibleHostIP='192.168.5.134:5000', ansibleRemoteIP='192.168.5.109:5000'):
        gr.top_block.__init__(self, "Ansible Hydra Server Side1")

        ##################################################
        # Parameters
        ##################################################
        self.ansibleFreqRx = ansibleFreqRx
        self.ansibleFreqTx = ansibleFreqTx
        self.ansibleHostIP = ansibleHostIP
        self.ansibleRemoteIP = ansibleRemoteIP

        ##################################################
        # Blocks
        ##################################################
        self.hydra_gr_server_network_0 = hydra.hydra_gr_server_network(ansibleHostIP)
        if 2e6 > 0 and 4e6 > 0 and 2048 > 0:
           self.hydra_gr_server_network_0.set_tx_config(2e6, 4e6, 2048, ansibleHostIP, ansibleRemoteIP)
        if 2e6 > 0 and 4e6 > 0 and 2048 > 0:
           self.hydra_gr_server_network_0.set_rx_config(2e6, 4e6, 2048, ansibleHostIP, ansibleRemoteIP)
        self.hydra_gr_server_network_0_thread = threading.Thread(target=self.hydra_gr_server_network_0.start_server)
        self.hydra_gr_server_network_0_thread.daemon = True
        self.hydra_gr_server_network_0_thread.start()

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

    def get_ansibleRemoteIP(self):
        return self.ansibleRemoteIP

    def set_ansibleRemoteIP(self, ansibleRemoteIP):
        self.ansibleRemoteIP = ansibleRemoteIP


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--ansibleFreqRx", dest="ansibleFreqRx", type="string", default='2e6',
        help="Set ansibleFreqRx [default=%default]")
    parser.add_option(
        "", "--ansibleFreqTx", dest="ansibleFreqTx", type="string", default='2e6',
        help="Set ansibleFreqTx [default=%default]")
    parser.add_option(
        "", "--ansibleHostIP", dest="ansibleHostIP", type="string", default='192.168.5.134:5000',
        help="Set ansibleHostIP [default=%default]")
    parser.add_option(
        "", "--ansibleRemoteIP", dest="ansibleRemoteIP", type="string", default='192.168.5.109:5000',
        help="Set ansibleRemoteIP [default=%default]")
    return parser


def main(top_block_cls=ansible_hydra_server_side1, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(ansibleFreqRx=options.ansibleFreqRx, ansibleFreqTx=options.ansibleFreqTx, ansibleHostIP=options.ansibleHostIP, ansibleRemoteIP=options.ansibleRemoteIP)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
