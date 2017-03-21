import sys
from optparse import OptionParser
import matplotlib.pyplot as plt
import numpy as np

def from_bin_file(fname):
    fd = open(fname, "rb")
    arr= np.fromfile(fd, np.dtype(np.complex64))

    return arr

def gen_img(arr, perform_fft, fft_size, fname, nfft_to_group = 1):

        # cut off samples in the end of the file that do not fit a FFT
        arr = np.resize(arr, arr.size - arr.size % fft_size)


        # reshape
        if nfft_to_group == 1:
            arr = arr.reshape(arr.size/fft_size/nfft_to_group, fft_size)
        else:
            print arr.size
            print nfft_to_group
            arr = arr.reshape(nfft_to_group, arr.size/fft_size/nfft_to_group, fft_size)
            arr = np.mean(arr, axis=1)

        print "-----------"
        print arr.size
        if perform_fft:
            arr = np.fft.ifftshift(np.fft.fft(arr))
        arr = complex_to_mag(arr)

        plt.imshow(arr, cmap='hot', interpolation='nearest')
        plt.savefig(fname)

def complex_to_mag(ar):
    return 20 * np.log10(np.absolute(ar))

def main(options):

    arr = from_bin_file(options.in_file)

    fname = lambda idx: options.out_file + str(idx) + "." + options.out_file_ext

    nfft_to_group = 1
    if options.avg_by_time > 0:
         nfft_to_group = int((options.samp_rate/options.fft_size) * (options.avg_by_time/1000.0))
    block_size = options.lines_per_file * options.fft_size * nfft_to_group

    if options.out_pos == -1:
        options.out_pos = len(arr)

    inpos = options.in_pos
    while inpos < options.out_pos:
        gen_img(arr[inpos:inpos+block_size], options.perform_fft, options.fft_size, fname(inpos/block_size), nfft_to_group)

        inpos += block_size

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--in-file", type="string", default="./signal.bin",
                     help="Bin file to read.")
    parser.add_option("", "--fft-size", type="int", default=256,
                     help="FFT size used/to use.")
    parser.add_option("", "--perform-fft", action="store_true", default=False,
                     help="Perform FFT.")
    parser.add_option("", "--lines-per-file", type="int", default=1000,
                     help="Block of samples to read from FILE.")
    parser.add_option("", "--in-pos", type="int", default=0,
                     help="Index of first sample to read.")
    parser.add_option("", "--out-pos", type="int", default=-1,
                     help="Index of last sample to read.")
    parser.add_option("", "--out-file", type="string", default="spectrum",
                     help="Output file name. Each image is generate from BLOCK-SIZE samples.")
    parser.add_option("", "--out-file-ext", type="string", default="png",
                     help="Ouput image extension.")
    parser.add_option("", "--samp-rate", type="float", default=1e6,
                      help="Sample rate used to generate file. Used to group FFT bins by TIME.")
    parser.add_option("", "--avg-by-time", type="int", default=-1,
                      help="In milliseconds. Group FFT BINS by time based on the SAMP RATE.")
    (options, args) = parser.parse_args ()

    main(options)
