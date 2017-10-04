#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: OFDM Tx
# Description: Example of an OFDM Transmitter
# Generated: Wed Oct  4 14:15:48 2017
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import hydra
import numpy


class hydra_dump_to_files(gr.top_block):

    def __init__(self, amplitude1=0.1, amplitude2=0.1, fftm=1024, filepattern="./", freq=950e6, freq1=949.5e6, freq2=951e6, samprate=6e6, samprate1=1e6, samprate2=500e3, vr1fft=170, vr1offset=0, vr2fft=85, vr2offset=640):
        gr.top_block.__init__(self, "OFDM Tx")

        ##################################################
        # Parameters
        ##################################################
        self.amplitude1 = amplitude1
        self.amplitude2 = amplitude2
        self.fftm = fftm
        self.filepattern = filepattern
        self.freq = freq
        self.freq1 = freq1
        self.freq2 = freq2
        self.samprate = samprate
        self.samprate1 = samprate1
        self.samprate2 = samprate2
        self.vr1fft = vr1fft
        self.vr1offset = vr1offset
        self.vr2fft = vr2fft
        self.vr2offset = vr2offset

        ##################################################
        # Variables
        ##################################################
        self.pilot_carriers = pilot_carriers = ((-42, -14, -7, 7, 14, 42),)
        self.pattern2 = pattern2 = [1, -1, 1, -1]
        self.pattern1 = pattern1 = [0., 1.41421356, 0., -1.41421356]
        self.fft_len = fft_len = 128
        self.sync_word2 = sync_word2 = [0., 0., 0., 0., 0., 0.,] + pattern2 * ((fft_len-12)/len(pattern2))  +[0., 0., 0., 0., 0., 0.,]
        self.sync_word1 = sync_word1 = [0., 0., 0., 0., 0., 0.,] + pattern1 * ((fft_len-12)/len(pattern1))  +[0., 0., 0., 0., 0., 0.,]
        self.pilot_symbols = pilot_symbols = ((-1,1, 1, -1, -1, -1),)
        self.packet_len = packet_len = 100
        self.occupied_carriers = occupied_carriers = (sorted(tuple(set([x for x in range(-26,27)]) - set(pilot_carriers[0]) - set([0,]))),)
        self.length_tag_key = length_tag_key = "packet_len"

        ##################################################
        # Blocks
        ##################################################
        self.hydra_hydra_sink_0 = hydra.hydra_sink(2, fftm, freq, samprate,
        	 ((freq1, samprate1),
        	 (freq2, samprate2),
        	 ))

        self.fft_vxx_0_1 = fft.fft_vcc(fftm, True, (window.rectangular(fftm)), True, 1)
        self.fft_vxx_0_0_0 = fft.fft_vcc(4096, False, (window.rectangular(4096)), True, 1)
        self.fft_vxx_0_0 = fft.fft_vcc(4096, False, (window.rectangular(4096)), True, 1)
        self.fft_vxx_0 = fft.fft_vcc(fftm, True, (window.rectangular(fftm)), True, 1)
        self.digital_ofdm_tx_0_1 = digital.ofdm_tx(
        	  fft_len=64, cp_len=16,
        	  packet_length_tag_key=length_tag_key,
        	  occupied_carriers=(sorted(tuple(set([x for x in range(-15,15)]) - set(pilot_carriers[0]) - set([0,]))),),
        	  pilot_carriers=pilot_carriers,
        	  pilot_symbols=pilot_symbols,
        	  sync_word1=[0., 0., 0., 0., 0., 0.,] + pattern1 * ((64-12)/len(pattern1))  +[0., 0., 0., 0., 0., 0.,] ,
        	  sync_word2=[0., 0., 0., 0., 0., 0.,] + pattern2 * ((64-12)/len(pattern2))  +[0., 0., 0., 0., 0., 0.,] ,
        	  bps_header=1,
        	  bps_payload=1,
        	  rolloff=0,
        	  debug_log=False,
        	  scramble_bits=False
        	 )
        self.digital_ofdm_tx_0 = digital.ofdm_tx(
        	  fft_len=128, cp_len=16,
        	  packet_length_tag_key=length_tag_key,
        	  occupied_carriers=(sorted(tuple(set([x for x in range(-60,60)]) - set(pilot_carriers[0]) - set([0,]))),),
        	  pilot_carriers=pilot_carriers,
        	  pilot_symbols=pilot_symbols,
        	  sync_word1=sync_word1,
        	  sync_word2=sync_word2,
        	  bps_header=1,
        	  bps_payload=1,
        	  rolloff=0,
        	  debug_log=False,
        	  scramble_bits=False
        	 )
        self.digital_ofdm_rx_0 = digital.ofdm_rx(
        	  fft_len=128, cp_len=16,
        	  frame_length_tag_key='frame_'+"length",
        	  packet_length_tag_key="length",
        	  occupied_carriers=(sorted(tuple(set([x for x in range(-60,60)]) - set(pilot_carriers[0]) - set([0,]))),),
        	  pilot_carriers=pilot_carriers,
        	  pilot_symbols=pilot_symbols,
        	  sync_word1=sync_word1,
        	  sync_word2=sync_word2,
        	  bps_header=1,
        	  bps_payload=1,
        	  debug_log=False,
        	  scramble_bits=False
        	 )
        self.blocks_vector_to_stream_0_1 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, fftm)
        self.blocks_vector_to_stream_0_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 4096)
        self.blocks_vector_to_stream_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 4096)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, fftm)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, 6e6,True)
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_char*1, '', "VR1 Rx'ed"); self.blocks_tag_debug_0.set_display(True)
        self.blocks_stream_to_vector_0_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fftm)
        self.blocks_stream_to_vector_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 4096)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 4096)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fftm)
        self.blocks_stream_to_tagged_stream_0_1 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, packet_len/2, length_tag_key)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, packet_len, length_tag_key)
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_vcc((1.0/fftm, ))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vcc((1.0/fftm, ))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc((amplitude2, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((amplitude1, ))
        self.blocks_keep_m_in_n_0_0 = blocks.keep_m_in_n(gr.sizeof_gr_complex, vr2fft, fftm, vr2offset)
        self.blocks_keep_m_in_n_0 = blocks.keep_m_in_n(gr.sizeof_gr_complex, vr1fft, fftm, vr1offset)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, int(50e6))
        self.blocks_file_sink_0_0_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, filepattern + "-pos-vr1.bin", False)
        self.blocks_file_sink_0_0_0_0.set_unbuffered(False)
        self.blocks_file_sink_0_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, filepattern + "-pos-vr2.bin", False)
        self.blocks_file_sink_0_0_0.set_unbuffered(False)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, filepattern + "-pre-vr2.bin", False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, filepattern + "-pre-vr1.bin", False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.analog_random_source_x_0_1 = blocks.vector_source_b(map(int, numpy.random.randint(5, 10, 1000)), True)
        self.analog_random_source_x_0 = blocks.vector_source_b(map(int, numpy.random.randint(0, 5, 1000)), True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.analog_random_source_x_0_1, 0), (self.blocks_stream_to_tagged_stream_0_1, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_keep_m_in_n_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_keep_m_in_n_0_0, 0), (self.blocks_stream_to_vector_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.hydra_hydra_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.hydra_hydra_sink_0, 1))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_file_sink_0_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.digital_ofdm_rx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.blocks_file_sink_0_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_ofdm_tx_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_1, 0), (self.digital_ofdm_tx_0_1, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0_0, 0), (self.fft_vxx_0_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_1, 0), (self.fft_vxx_0_1, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_vector_0_1, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_keep_m_in_n_0, 0))
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_vector_to_stream_0_0_0, 0), (self.blocks_multiply_const_vxx_1_0, 0))
        self.connect((self.blocks_vector_to_stream_0_1, 0), (self.blocks_keep_m_in_n_0_0, 0))
        self.connect((self.digital_ofdm_rx_0, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.digital_ofdm_tx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_ofdm_tx_0_1, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_vector_to_stream_0_0, 0))
        self.connect((self.fft_vxx_0_0_0, 0), (self.blocks_vector_to_stream_0_0_0, 0))
        self.connect((self.fft_vxx_0_1, 0), (self.blocks_vector_to_stream_0_1, 0))
        self.connect((self.hydra_hydra_sink_0, 0), (self.blocks_head_0, 0))

    def get_amplitude1(self):
        return self.amplitude1

    def set_amplitude1(self, amplitude1):
        self.amplitude1 = amplitude1
        self.blocks_multiply_const_vxx_0.set_k((self.amplitude1, ))

    def get_amplitude2(self):
        return self.amplitude2

    def set_amplitude2(self, amplitude2):
        self.amplitude2 = amplitude2
        self.blocks_multiply_const_vxx_0_0.set_k((self.amplitude2, ))

    def get_fftm(self):
        return self.fftm

    def set_fftm(self, fftm):
        self.fftm = fftm
        self.blocks_multiply_const_vxx_1_0.set_k((1.0/self.fftm, ))
        self.blocks_multiply_const_vxx_1.set_k((1.0/self.fftm, ))
        self.blocks_keep_m_in_n_0_0.set_n(self.fftm)
        self.blocks_keep_m_in_n_0.set_n(self.fftm)

    def get_filepattern(self):
        return self.filepattern

    def set_filepattern(self, filepattern):
        self.filepattern = filepattern
        self.blocks_file_sink_0_0_0_0.open(self.filepattern + "-pos-vr1.bin")
        self.blocks_file_sink_0_0_0.open(self.filepattern + "-pos-vr2.bin")
        self.blocks_file_sink_0_0.open(self.filepattern + "-pre-vr2.bin")
        self.blocks_file_sink_0.open(self.filepattern + "-pre-vr1.bin")

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq

    def get_freq1(self):
        return self.freq1

    def set_freq1(self, freq1):
        self.freq1 = freq1
        self.hydra_hydra_sink_0.set_central_frequency(0, self.freq1)

    def get_freq2(self):
        return self.freq2

    def set_freq2(self, freq2):
        self.freq2 = freq2
        self.hydra_hydra_sink_0.set_central_frequency(1, self.freq2)

    def get_samprate(self):
        return self.samprate

    def set_samprate(self, samprate):
        self.samprate = samprate

    def get_samprate1(self):
        return self.samprate1

    def set_samprate1(self, samprate1):
        self.samprate1 = samprate1

    def get_samprate2(self):
        return self.samprate2

    def set_samprate2(self, samprate2):
        self.samprate2 = samprate2

    def get_vr1fft(self):
        return self.vr1fft

    def set_vr1fft(self, vr1fft):
        self.vr1fft = vr1fft
        self.blocks_keep_m_in_n_0.set_m(self.vr1fft)

    def get_vr1offset(self):
        return self.vr1offset

    def set_vr1offset(self, vr1offset):
        self.vr1offset = vr1offset
        self.blocks_keep_m_in_n_0.set_offset(self.vr1offset)

    def get_vr2fft(self):
        return self.vr2fft

    def set_vr2fft(self, vr2fft):
        self.vr2fft = vr2fft
        self.blocks_keep_m_in_n_0_0.set_m(self.vr2fft)

    def get_vr2offset(self):
        return self.vr2offset

    def set_vr2offset(self, vr2offset):
        self.vr2offset = vr2offset
        self.blocks_keep_m_in_n_0_0.set_offset(self.vr2offset)

    def get_pilot_carriers(self):
        return self.pilot_carriers

    def set_pilot_carriers(self, pilot_carriers):
        self.pilot_carriers = pilot_carriers
        self.set_occupied_carriers((sorted(tuple(set([x for x in range(-26,27)]) - set(self.pilot_carriers[0]) - set([0,]))),))

    def get_pattern2(self):
        return self.pattern2

    def set_pattern2(self, pattern2):
        self.pattern2 = pattern2
        self.set_sync_word2([0., 0., 0., 0., 0., 0.,] + self.pattern2 * ((self.fft_len-12)/len(self.pattern2))  +[0., 0., 0., 0., 0., 0.,] )

    def get_pattern1(self):
        return self.pattern1

    def set_pattern1(self, pattern1):
        self.pattern1 = pattern1
        self.set_sync_word1([0., 0., 0., 0., 0., 0.,] + self.pattern1 * ((self.fft_len-12)/len(self.pattern1))  +[0., 0., 0., 0., 0., 0.,] )

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.set_sync_word2([0., 0., 0., 0., 0., 0.,] + self.pattern2 * ((self.fft_len-12)/len(self.pattern2))  +[0., 0., 0., 0., 0., 0.,] )
        self.set_sync_word1([0., 0., 0., 0., 0., 0.,] + self.pattern1 * ((self.fft_len-12)/len(self.pattern1))  +[0., 0., 0., 0., 0., 0.,] )

    def get_sync_word2(self):
        return self.sync_word2

    def set_sync_word2(self, sync_word2):
        self.sync_word2 = sync_word2

    def get_sync_word1(self):
        return self.sync_word1

    def set_sync_word1(self, sync_word1):
        self.sync_word1 = sync_word1

    def get_pilot_symbols(self):
        return self.pilot_symbols

    def set_pilot_symbols(self, pilot_symbols):
        self.pilot_symbols = pilot_symbols

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len
        self.blocks_stream_to_tagged_stream_0_1.set_packet_len(self.packet_len/2)
        self.blocks_stream_to_tagged_stream_0_1.set_packet_len_pmt(self.packet_len/2)
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.packet_len)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.packet_len)

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers

    def get_length_tag_key(self):
        return self.length_tag_key

    def set_length_tag_key(self, length_tag_key):
        self.length_tag_key = length_tag_key


def argument_parser():
    description = 'Example of an OFDM Transmitter'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--amplitude1", dest="amplitude1", type="eng_float", default=eng_notation.num_to_str(0.1),
        help="Set amplitude1 [default=%default]")
    parser.add_option(
        "", "--amplitude2", dest="amplitude2", type="eng_float", default=eng_notation.num_to_str(0.1),
        help="Set amplitude2 [default=%default]")
    parser.add_option(
        "", "--fftm", dest="fftm", type="intx", default=1024,
        help="Set fftm [default=%default]")
    parser.add_option(
        "", "--filepattern", dest="filepattern", type="string", default="./",
        help="Set ./ [default=%default]")
    parser.add_option(
        "", "--vr1fft", dest="vr1fft", type="intx", default=170,
        help="Set vr1fft [default=%default]")
    parser.add_option(
        "", "--vr1offset", dest="vr1offset", type="intx", default=0,
        help="Set vr1offset [default=%default]")
    parser.add_option(
        "", "--vr2fft", dest="vr2fft", type="intx", default=85,
        help="Set vr2fft [default=%default]")
    parser.add_option(
        "", "--vr2offset", dest="vr2offset", type="intx", default=640,
        help="Set vr2offset [default=%default]")
    return parser


def main(top_block_cls=hydra_dump_to_files, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(amplitude1=options.amplitude1, amplitude2=options.amplitude2, fftm=options.fftm, filepattern=options.filepattern, vr1fft=options.vr1fft, vr1offset=options.vr1offset, vr2fft=options.vr2fft, vr2offset=options.vr2offset)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
