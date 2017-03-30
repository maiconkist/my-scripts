MODE=$1
A1=$2;
A2=$3;

case "$MODE" in
		  "lte") file=./single/lte_${A1}_4Msps_20Ms.bin
		  ;;

		  "nbiot") file=./single/nbiot_${A2}_4Msps_20Ms.bin
		  ;;

		  "atomic")   file=./hydra/atomic_${A1}A1_${A2}A2_4Msps_20Ms.bin
		  ;;


		  *)
					 echo "Deu bosta"
		  ;;
esac


python ./spectrum_to_binfile.py -f $file;

python ./img_from_bin_file.py --samp-rate 4e6 --fft-size 4096 -f $file --lines-per-file -1 --perform-fft --nfft-to-group 1 --binarize;

xdg-open ${file}0.png

