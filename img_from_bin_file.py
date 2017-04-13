#!env python

import sys
from optparse import OptionParser
import matplotlib.pyplot as plt
import numpy as np
import os

from PIL import Image


hydra_filename_template= 'hydra/{mode}_{A1}A1_{A2}A2_4Msps_20Ms.bin'
single_filename_template= 'single/{radio}_{A}_4Msps_20Ms.bin'

mode = ['atomic', 'burst' ]
A1 = ["00", "01", "05", "1"] # amplitudes for VR 1
A2 = ["00", "01", "05", "1"] # amplitudes for VR 2

radio = ['lte', 'nb_iot']
A = ["00", "01", "05", "1"] # amplitudes for VR 1

BIN_NOISE = -1
BIN_DC =    -2



#CROP = { 'lte' :(1230, 0, 2610, 200),
CROP = { 'lte' :(910, 0, 2290, 200),
         'nbiot':(2894, 0, 3250, 200),
}

def from_bin_file(fname):
    fd = open(fname, "rb")
    arr= np.fromfile(fd, np.dtype(np.complex64))

    return arr

def parse_arr(arr, options):
        nfft_to_group = options.nfft_to_group
        fft_size = options.fft_size

        # cut off samples in the end of the file that do not fit a FFT
        arr = np.resize(arr, arr.size - arr.size % fft_size)

        print('\t ... reshaping')
        arr = arr.reshape(arr.size/fft_size, fft_size)

        if options.perform_fft:
            print('\t ... fft')
            arr = np.fft.ifftshift(np.fft.fft(arr))
        print('\t ... complex to mag')
        #arr = np.log10(np.absolute(arr))
        arr = np.absolute(arr)

        # reshape
        if nfft_to_group > 1:
            print('\t ... grouping')
            arr2 = []
            for i in range(0, len(arr)/nfft_to_group):
                gsum = np.array([0.0 for _tmp in range(fft_size)])
                print(str(i) + "/" + str(len(arr)))
                gsum = arr[0:min(nfft_to_group, len(arr)-1)]
                arr = np.delete(arr, range(0,min(nfft_to_group, len(arr)-1)), 0)
                arr2.append(gsum.sum(axis=0)/len(gsum))

                print(arr2[-1])

            arr = np.array(arr2)

        mi = np.min(arr)
        # bin mask for ADC ONLY
        bin_mask = gen_bin_mask(None, None, fft_size, ())
        for i in range(len(arr)):
            pass
            #arr[i][ bin_mask == BIN_DC ] = mi


        print('\t ... normalizing')
        print('\t\t ... min: ' + str(np.min(arr)))
        print('\t\t ... max: ' + str(np.max(arr)))
        print('\t\t ... avg: ' + str(np.average(arr)))
        print('\t\t ... std: ' + str(np.std(arr)))
        mi = np.min(arr)
        ma = np.max(arr)

        arr_norm = (arr - mi) / (ma - mi)

        return arr, arr_norm

def gen_bin_mask(cf, bw, fft_size, vr_confs):
    bin_mask = np.array([BIN_NOISE] * fft_size)

    for idx, vr in enumerate(vr_confs):
        vr_cf = vr[0]
        vr_bw = vr[1]

        bw_per_bin = bw/fft_size

        vr_mid_fft = (fft_size/2) + ((vr_cf-cf) / bw_per_bin)
        vr_fi_fft = int(vr_mid_fft - (vr_bw/2/bw_per_bin))
        vr_la_fft = int(vr_mid_fft + (vr_bw/2/bw_per_bin))

        print("---- VR: %d,  1st FFT: %d, 9th FFT: %d" % (idx, vr_fi_fft, vr_la_fft))

        bin_mask[vr_fi_fft:vr_la_fft] = idx

    # MAJOR SOURCE OF BUGS IF YOU CHANGE THE FFT SIZE
    mid = fft_size/2
    bin_mask[mid-20:mid+20] = BIN_DC

    return bin_mask

def gen_power_csv(arr, options):
    cf = 5.48e9
    bw = 4e6
    vr_confs = [(cf-500e3, 1e6), (cf+400e3, 200e3)]

    bin_mask = gen_bin_mask(cf, bw, options.fft_size, vr_confs)

    res = []

    for idx, vr in enumerate(vr_confs):
        arr2 = sum (arr)

        # sum arr values in indexes where bin_mask == vr id
        power = np.sum(arr2[bin_mask == idx]) / sum(bin_mask == idx)
        noise = np.sum(arr2[bin_mask == BIN_NOISE])  / sum(bin_mask == BIN_NOISE)

        snr = np.log10((power/noise) ** 2)
        res.extend([idx, snr, noise, power])
        print("VR %d -- SNR: %f [noise: %f, power:%f]" % (idx, snr, noise, power))

    with open(options.csv_file, 'a+') as fd:
        fd.write(options.in_file + "," + ",".join([str(x) for x in res]))
        fd.write("\n")

def gen_heatmap(arr_norm, options, imgname):
    print('\t ... saving colored image: ' + imgname)
    img = Image.fromarray(np.uint8(plt.get_cmap('Accent')(arr_norm) * 255.0))
    img.save(imgname)

    if options.binarize:
        print('\t ... binarizing')
        low = arr_norm <= (np.average(arr_norm) + 2 * (np.std(arr_norm)))
        high = arr_norm > (np.average(arr_norm) + 2 * (np.std(arr_norm)))
        arr_norm[low] = 50.0
        arr_norm[high] = 255.0

        print('\t\t ... saving binarized imag')
        bin_img = Image.fromarray(arr_norm).convert('RGB')
        bin_img.save(imgname.replace(options.out_file_ext, '_binarized.' + options.out_file_ext))

    if options.crop:
        print('\t ... cropping images')
        for k, v in CROP.iteritems():
            print('\t\t ... saving crop ' + k)
            crop_img = bin_img.copy()
            crop_img.crop(v).save(imgname.replace(options.out_file_ext, k + '.' + options.out_file_ext))
    print("DONE")

def gen_plotline(arr_parsed, options, imgname, eof):
    plt.plot(np.mean(arr_parsed, axis=0))
    plt.savefig(imgname.replace(options.in_file, options.in_file +'_line.png'))
    plt.close()

def parse_file(options):
    arr = from_bin_file(options.in_file)

    imgname = lambda idx: (options.dst_folder if options.dst_folder else "") + "/" + os.path.basename(options.in_file) + str(idx) + "." + options.out_file_ext

    inpos = options.in_pos
    if options.lines_per_file == -1:
        print("Generating a single image. This can take a while ...")
        block_size = len(arr)
    else:
        block_size = options.lines_per_file * options.fft_size * options.nfft_to_group

    if options.out_pos == -1:
        options.out_pos = len(arr)

    while inpos < options.out_pos:
        arr_parsed, arr_norm = parse_arr(arr[inpos:inpos+block_size], options)

        if options.gen_csv:
            gen_power_csv(arr_parsed, options)

        if options.gen_img:
            gen_heatmap(arr_norm, options, imgname(inpos/block_size))
            gen_plotline(arr_parsed, options, imgname(inpos/block_size), inpos + block_size < options.out_pos)

        inpos += block_size


def parse_all_files(options):

    for _r, _d, _f in os.walk(options.folder):
        if '.git' in _r:
            continue

        bin_files = [b for b in _f if b.endswith('.bin') and 'burst' not in b]

        for bf in bin_files:
            options.in_file = _r + '/' + bf
            print('Parsing file: ' + options.in_file)

            parse_file(options)

if __name__ == "__main__":
    parser = OptionParser()
    batch_group = parser.add_option_group('General Options')
    parser.add_option("-f", "--in-file", type="string", default="./signal.bin",
                     help="Bin file to read [default=%default].")
    parser.add_option("", "--fft-size", type="int", default=5120,
                     help="FFT size used/to use [default=%default].")
    parser.add_option("", "--perform-fft", action="store_true", default=True,
                     help="Perform FFT [default=%default].")
    parser.add_option("", "--lines-per-file", type="int", default=-1,
                     help="Block of samples to read from FILE [default=%default].")
    parser.add_option("", "--in-pos", type="int", default=0,
                     help="Index of first sample to read [default=%default].")
    parser.add_option("", "--out-pos", type="int", default=-1,
                     help="Index of last sample to read [default=%default].")
    parser.add_option("", "--samp-rate", type="float", default=1e6,
                      help="Sample rate used to generate file. Used to group FFT bins by TIME [default=%default].")
    parser.add_option("", "--nfft-to-group", type="int", default=1,
                      help="Group block of FFTs and extract the average [default=%default].")

    batch_group = parser.add_option_group('Batch Conversion')
    batch_group.add_option("", "--folder", type="string", default='.',
                     help="Specify the folder to parse all files [default=%default].")
    batch_group.add_option("", "--parse-all", action="store_true", default=False,
                     help="Parse all files in FOLDER [default=%default].")

    img_group = parser.add_option_group('Image Conversion')
    batch_group.add_option("", "--gen-img", action="store_true", default=False,
                     help="Genenerate images [default=%default].")
    img_group.add_option("", "--out-file-ext", type="string", default="png",
                         help="Ouput image extension [default=%default].")
    img_group.add_option("", "--binarize", action="store_true", default=False,
                         help="Save binarized version of image [default=%default].")
    img_group.add_option("", "--crop", action="store_true", default=False,
                         help="Save cropped version of image [default=%default]. Edit CROP variable to change crop coordinates.")
    batch_group.add_option("", "--dst-folder", type="string", default=None,
                     help="Destiny FOLDER of images [default=Same as binary file].")

    csv_group = parser.add_option_group('CSV Generation')
    batch_group.add_option("", "--gen-csv", action="store_true", default=False,
                     help="Genenerate CSV file [default=%default].")
    csv_group.add_option("", "--csv-file", type="string", default='csv.csv',
                     help="Specify the file to save the csv data [default=%default].")

    (options, args) = parser.parse_args ()

    if not (options.gen_img or options.gen_csv):
        print("Must specify --gen-img or --gen-csv [or both]")
        sys.exit(1)

    if options.parse_all:
        parse_all_files(options)
    else:
        parse_file(options)
