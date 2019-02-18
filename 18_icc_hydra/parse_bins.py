#!env python2.7

import sys
from optparse import OptionParser

import matplotlib
import matplotlib.pyplot as plt
from pylab import genfromtxt
import numpy as np
import os
import re

from PIL import Image

BIN_NOISE = -1
BIN_DC =    -2

# used to cut image in certain coordinates to better analize it
CROP = { 'lte' :(910, 0, 2290, 200),
         'nbiot':(2894, 0, 3250, 200),
}

def from_bin_file(fname):
    fd = open(fname, "rb")
    arr = np.fromfile(fd, np.dtype(np.complex64))
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
            arr = np.fft.ifftshift(np.fft.fft(arr)/fft_size)
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
        ## bin mask for ADC ONLY
        #bin_mask = gen_bin_mask(None, None, fft_size, ())
        #for i in range(len(arr)):
        #    pass
        #    arr[i][ bin_mask == BIN_DC ] = mi

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

        print("\t--- VR: %d -- 1st FFT: %d, 9th FFT: %d" % (idx, vr_fi_fft, vr_la_fft))

        bin_mask[vr_fi_fft:vr_la_fft] = idx

    # MAJOR SOURCE OF BUGS IF YOU CHANGE THE FFT SIZE
    mid = fft_size/2
    bin_mask[mid-20:mid+20] = BIN_DC

    return bin_mask

def gen_csv(arr, options):
    cf = 950e6
    bw = 1e6

    # we will generate the results analyzing this cfs and bandwidth
    vr_confs = [(950e6, 1e6), ]

    bin_mask = gen_bin_mask(cf, bw, options.fft_size, vr_confs)

    res = []
    for idx, vr in enumerate(vr_confs):
        arr2 = sum(arr)

        # sum arr values in indexes where bin_mask == vr id
        power = np.sum(arr2[bin_mask == idx]) / sum(bin_mask == idx)
        noise = np.min(arr2[bin_mask == idx])
        snr = 10 * np.log10((power/noise))

        res.extend([idx, snr, 10 * np.log10(noise), 10 * np.log10(power)])
        print("\t--- VR %d -- SNR: %f [noise: %f, power:%f]" % (idx, snr, noise, power))

    print("\t--- Saving CSV file to: " + options.csv_file)
    with open(options.csv_file, 'a+') as fd:
        cf, amplitude, it = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", options.in_file.split("/")[-1])
        fd.write(cf + " " + amplitude + " " + it + " ".join([str(x) for x in res]))
        fd.write("\n")
    awk_str = r'{snr[$1] += $4; snrq[$1] += ($4 ^ 2); count[$1] += 1;} END{for (a in snr) {print a " " snr[a]/count[a] " " sqrt((snrq[a]-snr[a]^2/count[a])/count[a]);}}'

    import subprocess as sp
    args = ['awk', awk_str, options.csv_file]
    p = sp.call(args, stdin = sp.PIPE, stdout = open(options.csv_file.replace(".csv", "-plottable.csv"), "w+"), stderr = sp.PIPE)

def calculate_mse(bin1, bin2):
    smallest = min(len(bin1), len(bin2))

    bin1 = bin1[0:smallest]
    bin2 = bin2[0:smallest]

    mse = sum(abs(bin1 - bin2) ** 2) / smallest
    return mse


def gen_mse_file(options):
    for _r, _d, _f in os.walk(options.src_folder):
        if '.git' in _r:
            con

        bin_files = [b for b in sorted(_f) if b.endswith('.bin') and options.pre_pattern in b]

        for bf in sorted(bin_files):
            prefile = _r + '/' + bf
            posfile = _r + '/' + bf.replace(options.pre_pattern, options.pos_pattern)
            mse = calculate_mse(from_bin_file(prefile), from_bin_file(posfile))

            fft, it, vr = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", prefile.split("/")[-1])

            with open(options.mse_file, 'a+') as fd:
                fd.write(" ".join([str(fft), str(int(float(vr))), str(abs(int(it))), str(mse), "\n"]))


def plot_mse_bars(options):
    import csv

    awk_str = r'{mse[$2][$1] += $4; mseq[$2][$1] += ($4 ^ 2); count[$2][$1] += 1;} END {for (vr in mse) {for (fft in mse[vr]){print fft " " vr " " mse[vr][fft]/count[vr][fft] " " sqrt((mseq[vr][fft]-mse[vr][fft]^2/count[vr][fft])/count[vr][fft]);}}}'
    import subprocess as sp
    args = ['awk', awk_str, options.mse_file]
    p = sp.call(args, stdin = sp.PIPE, stdout = open('./plottable.csv', "w+"), stderr = sp.PIPE)

    with open('./plottable.csv', 'r') as fd:
       dat = fd.read().split('\n')

    print dat

    # cut-off a '' line at the end
    if dat[-1] == '':
        dat = dat[0:-1]

    fft_filter = ['512', '1024', '2048', '4096']

    vr1_mse = [ 10* np.log10(float(d.split(' ')[2])) for d in dat if d.split(' ')[1] == '1' and d.split(' ')[0] in fft_filter]
    vr1_std = [ 10*np.log10(float(d.split(' ')[3])) for d in dat if d.split(' ')[1] == '1' and d.split(' ')[0] in fft_filter]
    vr2_mse = [ 10*np.log10(float(d.split(' ')[2])) for d in dat if d.split(' ')[1] == '2' and d.split(' ')[0] in fft_filter]
    vr2_std = [ 10*np.log10(float(d.split(' ')[3])) for d in dat if d.split(' ')[1] == '2' and d.split(' ')[0] in fft_filter]

    N = len(fft_filter)
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, vr1_mse, width, color='blue', yerr=vr1_std,  label='LTE')
    rects2 = ax.bar(ind + width, vr2_mse, width, color='green', yerr=vr2_std, label='NB-IoT')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Mean Square Error')
    ax.set_xlabel('Hydra FFT M Size')
    ax.set_xlim(-0.25, 4)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(fft_filter)
    plt.legend()
    plt.savefig("mse.pdf")

def plot_guard_band(options):
    datas = [
        genfromtxt( "0_0/plottable.csv"),
        genfromtxt("0_05/plottable.csv"),
        genfromtxt( "0_1/plottable.csv"),
        genfromtxt( "0_5/plottable.csv"),
    ]

    datas[0] = np.array([x for x in datas[0] if  x[0] < 949.27e6])
    datas[1] = np.array([x for x in datas[1] if  x[0] < 949.27e6])
    datas[2] = np.array([x for x in datas[2] if  x[0] < 949.27e6])
    datas[3] = np.array([x for x in datas[3] if  x[0] < 949.27e6])
    #datas[0] = np.array([x for x in datas[0] if  x[0] <= 949e6])
    #datas[1] = np.array([x for x in datas[1] if  x[0] <= 949e6])
    #datas[2] = np.array([x for x in datas[2] if  x[0] <= 949e6])
    #datas[3] = np.array([x for x in datas[3] if  x[0] <= 949e6])

    for d, cor, mar in zip(datas, ['r', 'b', 'g', 'y', 'k'], ['o', '^', 's', '*', 'v']):
        plt.errorbar(d[:,0] - 948.25e6, d[:,1], yerr=d[:,2], linestyle='-', marker = mar, color=cor)
        #plt.errorbar(d[:,0] - 948e6, d[:,1], yerr=d[:,2], linestyle='-', marker = mar, color=cor)

    plt.ylabel("SINR")
    plt.ylim([0,10])
    plt.xlabel("Guard Band [KHz]")
    plt.xticks((200e3, 400e3, 600e3, 800e3, 1e6), ('200 KHz', '400 KHz', '600KHz', '800 KHz', '1 MHz'))
    plt.xticks()

    plt.legend(("LTE Only", "Normalized", "2x Amplitude", "10x Amplitude"), loc = 'lower right')

    plt.savefig("guard_band_snr.pdf")

def plot_cpu_overhead(options):
    awk_str = r'{cpu += $2; cpuq += ($2 ^ 2); count += 1;} END{print "%s " cpu/count " " sqrt((cpuq-cpu^2/count)/count);}'

    for _r, _d, _f in os.walk(options.src_folder):
        cpu_files = [b for b in sorted(_f) if b.endswith('.txt') and 'cpu-' in b]

    for cf in sorted(cpu_files):
        import subprocess as sp

        args = ['awk', awk_str % cf.replace(".txt", "").split("-")[1], cf]
        p = sp.call(args, stdin = sp.PIPE, stdout = open("cpu-usage.txt", "a+"), stderr = sp.PIPE)

    data = open("cpu-usage.txt", "r").readlines()

    group1 = ['hydra', 'vr1_hydra', 'vr2_hydra']
    #group2 = ['vr1_all', 'vr2_all' ]

    data1 = [float(x.split(' ')[1]) for x in data if bool(set(x.split(' ')) & set(group1))]
    #data2 = [float(x.split(' ')[1]) for x in data if bool(set(x.split(' ')) & set(group2))]

    width = 0.15    # the width of the bars: can also be len(x) sequence
    ind = np.array([1, 2])  # the x locations for the groups

    p11 = plt.bar(ind[0], data1[0], width, color = 'b')
    p12 = plt.bar(ind[0], data1[1], width, bottom = data1[0], color='g' )
    p13 = plt.bar(ind[0], data1[2], width, bottom = data1[0] + data1[1], color='r')

    #p21 = plt.bar(ind[1], data2[0], width, color='b')
    #p22 = plt.bar(ind[1], data2[1], width, bottom = data2[0], color='g')

    plt.ylabel('CPU Utilization [%]')
    #plt.xticks(ind+0.175, ('HyDRA', 'Standalone'))
    plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
    plt.yticks(np.arange(0, 51, 10))
    plt.legend((p11[0], p12[0], p13[0]), ('LTE', 'NB-IoT', 'HyDRA'))

    plt.text(ind[0], sum(data1) + 2.0, '%4.2f%%' % sum(data1), ha='center', va='bottom')
    #plt.text(ind[1] + width/2, sum(data2) + 1.0, '%4.2f%%' % sum(data2), ha='center', va='bottom')

    plt.xlim((0.85, 2.5))
    plt.xlim((0.90, 1.25))
    plt.savefig("cpu-usage.pdf")

def gen_heatmap(arr_norm, options, imgname):
    print('\t\t...saving heatmap image: ' + imgname)
    img = Image.fromarray(np.uint8(plt.get_cmap('Accent')(arr_norm) * 255.0))
    img.save(imgname)

    if options.binarize:
        print('\t\t ... binarizing')
        low = arr_norm <= (np.average(arr_norm) + 2 * (np.std(arr_norm)))
        high = arr_norm > (np.average(arr_norm) + 2 * (np.std(arr_norm)))
        arr_norm[low] = 50.0
        arr_norm[high] = 255.0

        print('\t\t ... saving binarized imag')
        bin_img = Image.fromarray(arr_norm).convert('RGB')
        bin_img.save(imgname.replace(options.out_file_ext, '_binarized.' + options.out_file_ext))

    if options.crop:
        print('\t\t ... cropping images')
        for k, v in CROP.iteritems():
            print('\t\t ... saving crop ' + k)
            crop_img = bin_img.copy()
            crop_img.crop(v).save(imgname.replace(options.out_file_ext, k + '.'
                                                  + options.out_file_ext))
    print("DONE")


def gen_plotline(arr_parsed, imgname, eof=True):
    plt.plot(np.mean(arr_parsed, axis=0))
    print("\t... Saving plotline image: " + imgname)
    plt.savefig(imgname)

    if eof:
        plt.close()


def parse_file(options):
    arr = from_bin_file(options.in_file)

    imgname = lambda idx: (options.dst_folder if options.dst_folder else "") + "/" + os.path.basename(options.in_file) + str(idx) + "." + options.out_file_ext

    inpos = options.in_pos
    if options.lines_per_file == -1:
        print("\t Generating a single image. This can take a while ...")
        block_size = len(arr)
    else:
        block_size = options.lines_per_file * options.fft_size * options.nfft_to_group

    if options.out_pos == -1:
        options.out_pos = len(arr)

    while inpos < options.out_pos:
        arr_parsed, arr_norm = parse_arr(arr[inpos:inpos+block_size], options)

        if options.gen_csv:
            gen_csv(arr_parsed, options)

        if options.gen_img:
            print("\t...Generating heatmap")
            gen_heatmap(arr_norm, options, imgname(inpos/block_size).replace(".png", "-heatmap.png"))

            print("\t...Generating plotline")
            gen_plotline(arr_parsed, imgname(inpos/block_size).replace(".png", "-line.png"), inpos + block_size < options.out_pos)

        inpos += block_size


def parse_all_files(options):
    for _r, _d, _f in os.walk(options.src_folder):
        if '.git' in _r:
            continue

        bin_files = [b for b in sorted(_f) if b.endswith('.bin') and 'burst' not in b]

        for bf in bin_files:
            options.in_file = _r + '/' + bf
            print('Parsing file: ' + options.in_file)
            parse_file(options)

if __name__ == "__main__":
    parser = OptionParser()
    single_group = parser.add_option_group('Single File Options')
    single_group.add_option("-f", "--in-file", type="string", default=None,
                     help="Bin file to read [default=%default].")
    single_group.add_option("", "--fft-size", type="int", default=256,
                     help="FFT size used/to use [default=%default].")
    single_group.add_option("", "--perform-fft", action="store_true", default=True,
                     help="Perform FFT [default=%default].")
    single_group.add_option("", "--lines-per-file", type="int", default=-1,
                     help="Block of samples to read from FILE [default=%default].")
    single_group.add_option("", "--in-pos", type="int", default=0,
                     help="Index of first sample to read [default=%default].")
    single_group.add_option("", "--out-pos", type="int", default=-1,
                     help="Index of last sample to read [default=%default].")
    single_group.add_option("", "--samp-rate", type="float", default=1e6,
                      help="Sample rate used to generate file. Used to group FFT bins by TIME [default=%default].")
    single_group.add_option("", "--nfft-to-group", type="int", default=1,
                      help="Group block of FFTs and extract the average [default=%default].")

    batch_group = parser.add_option_group('Batch Conversion')
    batch_group.add_option("", "--batch", action="store_true", default=False,
                     help="Parse all files in FOLDER [default=%default].")
    batch_group.add_option("", "--src-folder", type="string", default='.',
                     help="Specify the folder to parse all files [default=%default].")

    img_group = parser.add_option_group('Image Conversion')
    batch_group.add_option("", "--gen-img", action="store_true", default=False,
                     help="Genenerate images [default=%default].")
    img_group.add_option("", "--out-file-ext", type="string", default="png",
                         help="Ouput image extension [default=%default].")
    img_group.add_option("", "--binarize", action="store_true", default=False,
                         help="Save binarized version of image [default=%default].")
    img_group.add_option("", "--spectogram", action="store_true", default=False,
                         help="Save spectogram version of bin file [default=%default].")
    img_group.add_option("", "--crop", action="store_true", default=False,
                         help="Save cropped version of image [default=%default]. Edit CROP variable to change crop coordinates.")
    batch_group.add_option("", "--dst-folder", type="string", default=None,
                     help="Destiny FOLDER of images [default=Same as binary file].")

    csv_group = parser.add_option_group('CSV Generation')
    batch_group.add_option("", "--gen-csv", action="store_true", default=False,
                     help="Genenerate CSV file [default=%default].")
    csv_group.add_option("", "--csv-file", type="string", default='csv.csv',
                     help="Specify the file to save the csv data [default=%default].")

    lines_group = parser.add_option_group('PlotLines Generation')
    lines_group.add_option("", "--gen-plotlines", action="store_true", default=False,
                     help="Genenerate plot lines files [default=%default].")

    gb_group = parser.add_option_group('Plot Guard-Band Lines')
    gb_group.add_option("", "--plot-gb", action="store_true", default=False,
                     help="Genenerate Guard-Band plot [default=%default].")

    cpu_group = parser.add_option_group('Plot CPU Overhead Lines')
    cpu_group.add_option("", "--plot-cpu", action="store_true", default=False,
                     help="Genenerate Guard-Band plot [default=%default].")

    mse_group = parser.add_option_group('MSE Calculation Generation')
    mse_group.add_option("", "--gen-mse", action="store_true", default=False,
                     help="Genenerate MSE file [default=%default].")
    mse_group.add_option("", "--mse-file", type="string", default='mse.csv',
                     help="Specify the file to save the MSE data [default=%default].")
    mse_group.add_option("", "--pre-pattern", type="string", default="pre-",
                     help="Pattern in bin file to identify it contains IQ samples PRIOR to HyDRA [default=%default].")
    mse_group.add_option("", "--pos-pattern", type="string", default="pos-",
                     help="Pattern in bin file to identify it contains IQ samples AFTER HyDRA [default=%default].")
    (options, args) = parser.parse_args()

    if not (options.gen_img or options.gen_csv or options.gen_mse or options.gen_plotlines, options.plot_gb or options.plot_cpu):
        print("Must specify --gen-img or --gen-csv or --gen-plotlines or --gen-mse or --gen-plotlines or --plot-gb or --plot-cpu")
        sys.exit(1)

#    if options.batch:
#        parse_all_files(options)
#    elif options.in_file:
#        parse_file(options)

    if options.plot_gb:
        plot_guard_band(options)

    if options.plot_cpu:
        plot_cpu_overhead(options)

    if options.gen_mse:
        gen_mse_file(options)
        plot_mse_bars(options)
