#!env python

import sys
from optparse import OptionParser
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image

def from_bin_file(fname):
    fd = open(fname, "rb")
    arr= np.fromfile(fd, np.dtype(np.complex64))

    return arr

def gen_img(arr, options, fname):

        nfft_to_group = options.nfft_to_group
        fft_size = options.fft_size

        # cut off samples in the end of the file that do not fit a FFT
        arr = np.resize(arr, arr.size - arr.size % fft_size)

        print '\t ... reshaping'
        arr = arr.reshape(arr.size/fft_size, fft_size)

        if options.perform_fft:
            print '\t ... fft'
            arr = np.fft.ifftshift(np.fft.fft(arr))

        print '\t ... complex to mag'
        arr = complex_to_mag(arr)

        # reshape
        if nfft_to_group > 1:
            print '\t ... grouping'
            arr2 = []
            for i in range(0, len(arr)/nfft_to_group):
                gsum = np.array([0.0 for _tmp in range(fft_size)])
                print str(i) + "/" + str(len(arr))
                gsum = arr[0:min(nfft_to_group, len(arr)-1)]
                arr = np.delete(arr, range(0,min(nfft_to_group, len(arr)-1)), 0)
                arr2.append(gsum.sum(axis=0)/len(gsum))

                print arr2[-1]

            arr = np.array(arr2)

        print '\t ... normalizing'
        arr = arr - np.min(arr)
        arr = arr / np.max(arr)
        print '\t\t ... avg: ' + str(np.average(arr))
        print '\t\t ... std: ' + str(np.std(arr))

        print '\t ... saving colored imag'
        img = Image.fromarray(np.uint8(plt.get_cmap('Accent')(arr) * 255.0))
        img.save(fname)

        if options.binarize:
            print '\t ... binarizing'
            low = arr <= (np.average(arr) + 3 * np.std(arr))
            high = arr > (np.average(arr) + 3 * np.std(arr))
            arr[low] = 100.0
            arr[high] = 255.0

            print '\t\t ... saving binarized imag'
            img = Image.fromarray(arr).convert('RGB')
            img.save(fname.replace(options.in_file, options.in_file +'_binarized'))

def complex_to_mag(ar):
    return np.log10(np.absolute(ar))

def main(options):

    arr = from_bin_file(options.in_file)

    fname = lambda idx: options.in_file + str(idx) + "." + options.out_file_ext

    inpos = options.in_pos
    if options.lines_per_file == -1:
        print "Generating a single image. This can take a while ..."
        block_size = len(arr)
    else:
        block_size = options.lines_per_file * options.fft_size * options.nfft_to_group

    if options.out_pos == -1:
        options.out_pos = len(arr)


    while inpos < options.out_pos:
        gen_img(arr[inpos:inpos+block_size], options, fname(inpos/block_size))

        inpos += block_size

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--in-file", type="string", default="./signal.bin",
                     help="Bin file to read.")
    parser.add_option("", "--fft-size", type="int", default=256,
                     help="FFT size used/to use.")
    parser.add_option("", "--perform-fft", action="store_true", default=False,
                     help="Perform FFT.")
    parser.add_option("", "--lines-per-file", type="int", default=-1,
                     help="Block of samples to read from FILE.")
    parser.add_option("", "--in-pos", type="int", default=0,
                     help="Index of first sample to read.")
    parser.add_option("", "--out-pos", type="int", default=-1,
                     help="Index of last sample to read.")
    parser.add_option("", "--out-file-ext", type="string", default="png",
                     help="Ouput image extension.")
    parser.add_option("", "--samp-rate", type="float", default=1e6,
                      help="Sample rate used to generate file. Used to group FFT bins by TIME.")
    parser.add_option("", "--nfft-to-group", type="int", default=1,
                      help="Group block of FFTs and extract the average.")
    parser.add_option("", "--binarize", action="store_true", default=False,
                     help="Save binarized version of image.")
    (options, args) = parser.parse_args ()

    main(options)
