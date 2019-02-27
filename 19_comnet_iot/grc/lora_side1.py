#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Lora Side1
# Generated: Wed Feb 27 18:32:44 2019
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fec
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import lora
import math
import sip
import sys
import time
from gnuradio import qtgui


class lora_side1(gr.top_block, Qt.QWidget):

    def __init__(self, MTU=10000, bw=100e3, frequency_rx=2.4505e9 + 3e6, frequency_tx=2.4505e9, offset=0):
        gr.top_block.__init__(self, "Lora Side1")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Lora Side1")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "lora_side1")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.MTU = MTU
        self.bw = bw
        self.frequency_rx = frequency_rx
        self.frequency_tx = frequency_tx
        self.offset = offset

        ##################################################
        # Variables
        ##################################################
        self.rep = rep = 3
        self.spreading_factor = spreading_factor = 8
        self.samp_rate = samp_rate = 500e3
        self.ldr = ldr = True
        self.header = header = False
        self.gain_tx = gain_tx = 0.1
        self.gain_rx = gain_rx = 1.0


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
        self._gain_tx_range = Range(0, 1, 0.01, 0.1, 200)
        self._gain_tx_win = RangeWidget(self._gain_tx_range, self.set_gain_tx, 'gain_tx', "counter_slider", float)
        self.top_layout.addWidget(self._gain_tx_win)
        self._gain_rx_range = Range(0, 1, 0.01, 1.0, 200)
        self._gain_rx_win = RangeWidget(self._gain_rx_range, self.set_gain_rx, 'gain_rx', "counter_slider", float)
        self.top_layout.addWidget(self._gain_rx_win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(('', '')),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(frequency_rx, 0)
        self.uhd_usrp_source_0.set_normalized_gain(gain_rx, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(frequency_tx, 0)
        self.uhd_usrp_sink_0.set_normalized_gain(gain_tx, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
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
        self.fec_async_encoder_0 = fec.async_encoder(enc_rep, False, True, True, MTU)
        self.fec_async_decoder_0 = fec.async_decoder(dec_rep, True, True, MTU)
        self.blocks_tuntap_pdu_0 = blocks.tuntap_pdu('tap0', MTU, False)
        self.blocks_rotator_cc_0_0 = blocks.rotator_cc((2 * math.pi * offset) / samp_rate)
        self.blocks_rotator_cc_0 = blocks.rotator_cc((2 * math.pi * offset) / samp_rate)
        self.blocks_message_debug_2 = blocks.message_debug()
        self.blocks_message_debug_1 = blocks.message_debug()
        self.blocks_message_debug_0 = blocks.message_debug()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tuntap_pdu_0, 'pdus'), (self.fec_async_encoder_0, 'in'))
        self.msg_connect((self.fec_async_decoder_0, 'out'), (self.blocks_message_debug_0, 'print_pdu'))
        self.msg_connect((self.fec_async_decoder_0, 'out'), (self.blocks_tuntap_pdu_0, 'pdus'))
        self.msg_connect((self.fec_async_encoder_0, 'out'), (self.blocks_message_debug_2, 'print_pdu'))
        self.msg_connect((self.fec_async_encoder_0, 'out'), (self.lora_encode_0, 'in'))
        self.msg_connect((self.lora_decode_0, 'out'), (self.fec_async_decoder_0, 'in'))
        self.msg_connect((self.lora_demod_0, 'out'), (self.lora_decode_0, 'in'))
        self.msg_connect((self.lora_encode_0, 'out'), (self.lora_mod_0, 'in'))
        self.connect((self.blocks_rotator_cc_0, 0), (self.pfb_arb_resampler_xxx_0, 0))
        self.connect((self.blocks_rotator_cc_0_0, 0), (self.pfb_arb_resampler_xxx_0_0, 0))
        self.connect((self.lora_mod_0, 0), (self.blocks_rotator_cc_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0_0, 0), (self.lora_demod_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_rotator_cc_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "lora_side1")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

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
        self.uhd_usrp_source_0.set_center_freq(self.frequency_rx, 0)

    def get_frequency_tx(self):
        return self.frequency_tx

    def set_frequency_tx(self, frequency_tx):
        self.frequency_tx = frequency_tx
        self.uhd_usrp_sink_0.set_center_freq(self.frequency_tx, 0)

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.blocks_rotator_cc_0_0.set_phase_inc((2 * math.pi * self.offset) / self.samp_rate)
        self.blocks_rotator_cc_0.set_phase_inc((2 * math.pi * self.offset) / self.samp_rate)

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
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)
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

    def get_gain_tx(self):
        return self.gain_tx

    def set_gain_tx(self, gain_tx):
        self.gain_tx = gain_tx
        self.uhd_usrp_sink_0.set_normalized_gain(self.gain_tx, 0)


    def get_gain_rx(self):
        return self.gain_rx

    def set_gain_rx(self, gain_rx):
        self.gain_rx = gain_rx
        self.uhd_usrp_source_0.set_normalized_gain(self.gain_rx, 0)


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
        "", "--frequency-rx", dest="frequency_rx", type="eng_float", default=eng_notation.num_to_str(2.4505e9 + 3e6),
        help="Set frequency_rx [default=%default]")
    parser.add_option(
        "", "--frequency-tx", dest="frequency_tx", type="eng_float", default=eng_notation.num_to_str(2.4505e9),
        help="Set frequency_tx [default=%default]")
    return parser


def main(top_block_cls=lora_side1, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(MTU=options.MTU, frequency_rx=options.frequency_rx, frequency_tx=options.frequency_tx)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
