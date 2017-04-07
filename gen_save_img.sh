MODE=$1
A1=$2;
A2=$3;

case "$MODE" in
		  "lte-burst") file=./single/lte_burst_${A1}_4Msps_20Ms.bin ;;
		  "nbiot-burst") file=./single/nbiot_burst_${A2}_4Msps_20Ms.bin ;;
		  "atomic-burst")   file=./hydra/atomic_burst_${A1}A1_${A2}A2_4Msps_20Ms.bin ;;

		  "lte-cont") file=./single/lte_cont_${A1}_4Msps_20Ms.bin ;;
		  "nbiot-cont") file=./single/nbiot_cont_${A2}_4Msps_20Ms.bin ;;
		  "atomic-cont")   file=./hydra/atomic_cont_${A1}A1_${A2}A2_4Msps_20Ms.bin ;;

		  *) echo "Deu bosta" ;;
esac


python ./spectrum_to_binfile.py -f $file;

python ./img_from_bin_file.py --samp-rate 4e6 --fft-size 4096 -f $file --lines-per-file -1 --perform-fft --nfft-to-group 1 --binarize;
