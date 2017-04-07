import pexpect
import time


RX_SCRIPT_FOLDER = "~/my-scripts/"
RX_SCRIPT = "./gen_save_img.sh {MODE} {A1} {A2}"

SSH_CMD = "ssh nodeuser@192.168.10.120"

TX_SCRIPT_FOLDER =  "~/gr-hydra/apps/"
TX_SCRIPT = {
    'hydra-burst': './atomic/tx/hydra_async_tx.py',
    'hydra-const': './atomic/tx/hydra_tx.py',

    'lte-burst': './no_hydra_tx/tx/single_radio_tx.py',
    'nbiot-burst': './no_hydra_tx/tx/single_radio_tx.py',
    'lte-cont': './no_hydra_tx/tx/single_radio_tx.py',
    'nbiot-cont': './no_hydra_tx/tx/single_radio_tx.py'
}

TX_OPT = {
    'burst': "--vr1-file ./vr1fifo --vr2-file ./vr2fifo --tx-gain 60 --vr2-buffersize 1000 --vr1-tx-amplitude {A1} --vr2-tx-amplitude {A2}",
    'cont': "--vr1-file ./vr1fifo --vr2-file ./vr2fifo --tx-gain 60 --vr2-buffersize 1000 --vr1-tx-amplitude {A1} --vr2-tx-amplitude {A2}",
}

TX_EXTRA_OPTS = {
    'atomic': "",
    'lte': "--lte-radio",
    'nbiot': "--nbiot-radio",
}

def main():
    remote = pexpect.spawn(SSH_CMD)
    local = pexpect.spawn('zsh')

    remote.sendline("cd " + RX_SCRIPT_FOLDER)
    local.sendline("cd " + TX_SCRIPT_FOLDER)

    #for split in ['hydra', 'lte', 'nbiot']:
    for split in ['lte', 'nbiot' ]:
        for mode in ['cont',  ]:
            for A1, A2 in [
                          ("00", "00"), ("00", "0.1"),  ("00", "0.5"), ("00", "1"),
                          ("0.1", "00"), ("0.1", "0.1"),  ("0.1", "0.5"), ("0.1", "1"),
                          ("0.5", "00"), ("0.5", "0.1"),  ("0.5", "0.5"), ("0.5", "1"),
                          ("1", "00"), ("1", "0.1"),  ("1", "0.5"), ("1", "1")]:
                print "Testing " + split + "-" + mode + " A1: " + A1 + ", A2:" + A2

                tx_opt_string = TX_OPT[mode].format(A1 = A1, A2 = A2)
                rx_script = RX_SCRIPT.format(MODE=split+'-'+mode, A1 = A1.replace('.',''), A2 = A2.replace(".", ""))

                print "\t ... Starting Transmitter"
                local.sendline(" ".join([TX_SCRIPT[split+"-"+mode], tx_opt_string, TX_EXTRA_OPTS[split]]))
                print "\t ... Waiting for USRP"
                local.expect("Start XMLRPC")
                time.sleep(2)

                print "\t ... Starting Receiver"
                remote.sendline(" ".join(["bash", rx_script]))
                print "... Waiting for DONE"

                remote.expect("DONE")

                print "\t ... Ok. Killing transmitter process"
                print str(local.before)
                local2 = pexpect.spawn('zsh')
                local2.sendline("killall hydra_async_tx.py; killall hydra_tx.py; killall single_radio_tx.py; fg")
                print "\t\t ... Done"

if __name__ == '__main__':
    main()
