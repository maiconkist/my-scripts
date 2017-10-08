FFT=(512 1024 2048 4096)

for fft in ${FFT[@]}; do

    vr1_offset_bw="$(python -c "print((949.5e6-1e6/2.0) - (950e6-6e6/2))")"
    vr1_offset="$(python -c "print(int(${vr1_offset_bw}/(6e6/${fft})))")"
    vr1_fft="$(python -c "print(int(1e6/(6e6/${fft})))")"

    vr2_offset_bw="$(python -c "print((951e6-500e3/2.0) - (950e6-6e6/2))")"
    vr2_offset="$(python -c "print(int(${vr2_offset_bw}/(6e6/${fft})))")"
    vr2_fft="$(python -c "print(int(500e3/(6e6/${fft})))")"

    #vr2_mid_fft="$(python -c "print((${fft}/2)+((951e6-950e6) / (6e6/${fft})))")"
    #vr2_fi_fft="$(python -c "print(int(${vr2_mid_fft} - (500e3/2/(6e6/${fft}))))")"
    #vr2_la_fft="$(python -c "print(int(${vr2_mid_fft} + (500e3/2/(6e6/${fft}))))")"
    #vr2_fft="$(python -c "print(int(${vr2_la_fft} - ${vr2_fi_fft}))")"


    echo "VR1 FFT: ${vr1_fft}, OFFSET: ${vr1_offset}"
    echo "VR2 FFT: ${vr2_fft}, OFFSET: ${vr2_offset}"

	  for it in `seq 0 10`; do
      echo "Iteration ${it}/10"
		  python hydra_dump_to_files.py --fftm ${fft} --filepattern "./${fft}-${it}" --vr1fft ${vr1_fft} --vr1offset ${vr1_offset} --vr2fft ${vr2_fft} --vr2offset ${vr2_offset}
    done
done

python ../parse_bins.py --gen-mse --src-folder ./ --dst-folder ./ --mse-file mse.csv
