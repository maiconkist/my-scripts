import pexpect
import time
import xmlrpclib
import sys

RX_SSH_CMD = "ssh -CY connect@192.168.10.30"
TX_SSH_CMD = "ssh -CY root@192.168.10.104"

TX_SCRIPT_FOLDER =  "~/fg-stuff/"
RX_SCRIPT_FOLDER =  "~/fg-stuff/"

TX_GNURADIO_ADDR = "192.168.10.104:8084"


tx = pexpect.spawn(TX_SSH_CMD)
rx = pexpect.spawn(RX_SSH_CMD)

def do_one_test(cf, thefile):
    rx.sendline("cd " + RX_SCRIPT_FOLDER)

    tx.sendline("cd " + TX_SCRIPT_FOLDER)
    tx.sendline("python test_tx_hydra.py &")
    tx.expect("VR 1:")
    print "Testing with NB-IoT at CF:" + str(cf)

    # set NB-IoT CF at usrp_hydra
    print "... Waiting 5 secs for TX to start"
    # cmd here
    time.sleep(8)

    print "Configuring NB center frequency"
    cli = xmlrpclib.ServerProxy("http://" + TX_GNURADIO_ADDR)
    cli.set_freq2(cf)

    # start capture
    rx.sendline("python vr1_rx_to_file.py --thefile " + thefile + " &")
    rx.expect("Performing timer loopback test")

    print "... Waiting 20 secs for RX to finish"
    time.sleep(20)
    print "... Ok. Killing RX process"
    rx.sendline("killall python; fg")
    rx.sendline("cd " + RX_SCRIPT_FOLDER + "; rm *.dat") # remove temporary files

    tx.sendline("killall python; fg")
    tx.sendline("cd " + TX_SCRIPT_FOLDER + "; rm *.dat") # remove temporary files
    print "... Done"

def main():
    #rx.sendline("screen -x XXX")
    #tx.sendline("screen -x XXX")


    cfin = int(947.1 * 10**6)
    cffi = int(952.7 * 10**6)
    step = int(100 * 10**3)
    r2 = range(cfin, cffi, step)

    for cf in r2:
        if sys.argv[1] is "":
            thefile = "./rx_" + str(cf) + ".bin"
        else:
            thefile = './rx_' + str(cf) + sys.argv[1] + ".bin"

        print ("RX saving to: " + thefile)
        do_one_test(cf, thefile)

if __name__ == '__main__':
    main()
