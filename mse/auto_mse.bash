FFT=(512 1024 2048 4096)

for fft in ${FFT[@]}; do

    vr1_mid_fft="$(python -c "print((${fft}/2)+((947.5e6-950e6) / (6e6/${fft})))")"
    vr1_fi_fft="$(python -c "print(int(${vr1_mid_fft} - (1e6/2/(6e6/${fft}))))")"
    vr1_la_fft="$(python -c "print(${vr1_mid_fft} + (1e6/2/(6e6/${fft})))")"
    vr1_fft="$(python -c "print(int(${vr1_la_fft} - ${vr1_fi_fft}))")"

    vr2_mid_fft="$(python -c "print((${fft}/2)+((951e6-950e6) / (6e6/${fft})))")"
    vr2_fi_fft="$(python -c "print(int(${vr2_mid_fft} - (500e3/2/(6e6/${fft}))))")"
    vr2_la_fft="$(python -c "print(${vr2_mid_fft} + (500e3/2/(6e6/${fft})))")"
    vr2_fft="$(python -c "print(int(${vr2_la_fft} - ${vr2_fi_fft}))")"

    python hydra_dump_to_files.py --fftm ${fft} --filepattern "./${fft}" --vr1fft ${vr1_fft} --vr1offset ${vr1_fi_fft} --vr2fft ${vr2_fft} --vr2offset ${vr2_fi_fft}

done
