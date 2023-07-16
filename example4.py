#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import subprocess
import tmuxCmd
import comnetsemu.node

from comnetsemu.cli import CLI, spawnXtermDocker
from comnetsemu.net import Containernet, VNFManager

from cmd import Cmd
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller
from connectivityTest import test_connections
from configurationTest import configurationTest
from python_modules.Open5GS   import Open5GS

import json, time, subprocess, sys

if __name__ == "__main__":

    AUTOTEST_MODE = os.environ.get("COMNETSEMU_AUTOTEST_MODE", 0)

    setLogLevel("info")

    prj_folder="/home/vagrant/comnetsemu/app/5Gnetwork"
    mongodb_folder="/home/vagrant/mongodbdata"

    env = dict()

    net = Containernet(controller=Controller, link=TCLink)

    info("*** Adding Host for open5gs CP\n")
    cp = net.addDockerHost(
        "cp",
        dimage="my5gc_v2-4-4",
        ip="192.168.0.111/24",
        # dcmd="",
        dcmd="bash /open5gs/install/etc/open5gs/5gc_cp_init.sh",
        docker_args={
            "ports" : { "3000/tcp": 3000 },
            "volumes": {
                prj_folder + "/log": {
                    "bind": "/open5gs/install/var/log/open5gs",
                    "mode": "rw",
                },
                mongodb_folder: {
                    "bind": "/var/lib/mongodb",
                    "mode": "rw",
                },
                prj_folder + "/open5gs/config": {
                    "bind": "/open5gs/install/etc/open5gs",
                    "mode": "rw",
                },
                "/etc/timezone": {
                    "bind": "/etc/timezone",
                    "mode": "ro",
                },
                "/etc/localtime": {
                    "bind": "/etc/localtime",
                    "mode": "ro",
                },
            },
        },
    )



    info("*** Adding Host for open5gs UPF\n")
    env["COMPONENT_NAME"]="upf_cld"
    upf_cld = net.addDockerHost(
        "upf_cld",
        dimage="my5gc_v2-4-4",
        ip="192.168.0.112/24",
        # dcmd="",
        dcmd="bash /open5gs/install/etc/open5gs/temp/5gc_up_init.sh",
        docker_args={
            "environment": env,
            "volumes": {
                prj_folder + "/log": {
                    "bind": "/open5gs/install/var/log/open5gs",
                    "mode": "rw",
                },
                prj_folder + "/open5gs/config": {
                    "bind": "/open5gs/install/etc/open5gs/temp",
                    "mode": "rw",
                },
                "/etc/timezone": {
                    "bind": "/etc/timezone",
                    "mode": "ro",
                },
                "/etc/localtime": {
                    "bind": "/etc/localtime",
                    "mode": "ro",
                },
            },
            "cap_add": ["NET_ADMIN"],
            "sysctls": {"net.ipv4.ip_forward": 1},
            "devices": "/dev/net/tun:/dev/net/tun:rwm"
        }, 
    )

    info("*** Adding Host for open5gs UPF MEC\n")
    env["COMPONENT_NAME"]="upf_mec"
    upf_mec = net.addDockerHost(
        "upf_mec",
        dimage="my5gc_v2-4-4",
        ip="192.168.0.113/24",
        # dcmd="",
        dcmd="bash /open5gs/install/etc/open5gs/temp/5gc_up_init.sh",
        docker_args={
            "environment": env,
            "volumes": {
                prj_folder + "/log": {
                    "bind": "/open5gs/install/var/log/open5gs",
                    "mode": "rw",
                },
                prj_folder + "/open5gs/config": {
                    "bind": "/open5gs/install/etc/open5gs/temp",
                    "mode": "rw",
                },
                "/etc/timezone": {
                    "bind": "/etc/timezone",
                    "mode": "ro",
                },
                "/etc/localtime": {
                    "bind": "/etc/localtime",
                    "mode": "ro",
                },
            },
            "cap_add": ["NET_ADMIN"],
            "sysctls": {"net.ipv4.ip_forward": 1},
            "devices": "/dev/net/tun:/dev/net/tun:rwm"
        },
    )

    info("*** Adding gNB\n")
    env["COMPONENT_NAME"]="gnb"
    gnb = net.addDockerHost(
        "gnb", 
        dimage="myueransim_v3-2-6",
        ip="192.168.0.131/24",
        # dcmd="",
        dcmd="bash /mnt/ueransim/open5gs_gnb_init.sh",
        docker_args={
            "environment": env,
            "volumes": {
                prj_folder + "/ueransim/config": {
                    "bind": "/mnt/ueransim",
                    "mode": "rw",
                },
                prj_folder + "/log": {
                    "bind": "/mnt/log",
                    "mode": "rw",
                },
                "/etc/timezone": {
                    "bind": "/etc/timezone",
                    "mode": "ro",
                },
                "/etc/localtime": {
                    "bind": "/etc/localtime",
                    "mode": "ro",
                },
                "/dev": {"bind": "/dev", "mode": "rw"},
            },
            "cap_add": ["NET_ADMIN"],
            "devices": "/dev/net/tun:/dev/net/tun:rwm"
        },
    )

    info("*** Adding gNB2\n")
    env["COMPONENT_NAME"]="gnb2"
    gnb2 = net.addDockerHost(
        "gnb2", 
        dimage="myueransim_v3-2-6",
        ip="192.168.0.133/24",
        # dcmd="",
        dcmd="bash /mnt/ueransim/open5gs-gnb2-init.sh",
        docker_args={
            "environment": env,
            "volumes": {
                prj_folder + "/ueransim/config": {
                    "bind": "/mnt/ueransim",
                    "mode": "rw",
                },
                prj_folder + "/log": {
                    "bind": "/mnt/log",
                    "mode": "rw",
                },
                "/etc/timezone": {
                    "bind": "/etc/timezone",
                    "mode": "ro",
                },
                "/etc/localtime": {
                    "bind": "/etc/localtime",
                    "mode": "ro",
                },
                "/dev": {"bind": "/dev", "mode": "rw"},
            },
            "cap_add": ["NET_ADMIN"],
            "devices": "/dev/net/tun:/dev/net/tun:rwm"
        },
    )

    info("*** Adding UE\n")
    env["COMPONENT_NAME"]="ue"
    ue = net.addDockerHost(
        "ue", 
        dimage="myueransim_v3-2-6",
        ip="192.168.0.132/24",
        # dcmd="",
        dcmd="bash /mnt/ueransim/open5gs_ue_init.sh",
        docker_args={
            "environment": env,
            "volumes": {
                prj_folder + "/ueransim/config": {
                    "bind": "/mnt/ueransim",
                    "mode": "rw",
                },
                prj_folder + "/log": {
                    "bind": "/mnt/log",
                    "mode": "rw",
                },
                "/etc/timezone": {
                    "bind": "/etc/timezone",
                    "mode": "ro",
                },
                "/etc/localtime": {
                    "bind": "/etc/localtime",
                    "mode": "ro",
                },
                "/dev": {"bind": "/dev", "mode": "rw"},
            },
            "cap_add": ["NET_ADMIN"],
            "devices": "/dev/net/tun:/dev/net/tun:rwm"
        },
    )

    info("*** Adding UE2\n")
    env["COMPONENT_NAME"]="ue2"
    ue2 = net.addDockerHost(
        "ue2", 
        dimage="myueransim_v3-2-6",
        ip="192.168.0.134/24",
        # dcmd="",
        dcmd="bash /mnt/ueransim/open5gs-ue2_init.sh",
        docker_args={
            "environment": env,
            "volumes": {
                prj_folder + "/ueransim/config": {
                    "bind": "/mnt/ueransim",
                    "mode": "rw",
                },
                prj_folder + "/log": {
                    "bind": "/mnt/log",
                    "mode": "rw",
                },
                "/etc/timezone": {
                    "bind": "/etc/timezone",
                    "mode": "ro",
                },
                "/etc/localtime": {
                    "bind": "/etc/localtime",
                    "mode": "ro",
                },
                "/dev": {"bind": "/dev", "mode": "rw"},
            },
            "cap_add": ["NET_ADMIN"],
            "devices": "/dev/net/tun:/dev/net/tun:rwm"
        },
    )

    info("*** Add controller\n")
    net.addController("c0")

    info("*** Adding switch\n")
    s1 = net.addSwitch("s1")
    s2 = net.addSwitch("s2")
    s3 = net.addSwitch("s3")

    info("*** Adding links\n")
    net.addLink(s1,  s2, bw=1000, delay="10ms", intfName1="s1-s2",  intfName2="s2-s1")
    net.addLink(s2,  s3, bw=1000, delay="50ms", intfName1="s2-s3",  intfName2="s3-s2")
    
    net.addLink(cp,      s3, bw=1000, delay="1ms", intfName1="cp-s1",  intfName2="s1-cp")
    net.addLink(upf_cld, s3, bw=1000, delay="1ms", intfName1="upf-s3",  intfName2="s3-upf_cld")
    net.addLink(upf_mec, s2, bw=1000, delay="1ms", intfName1="upf_mec-s2", intfName2="s2-upf_mec")

    net.addLink(ue,  s1, bw=1000, delay="1ms", intfName1="ue-s1",  intfName2="s1-ue")
    net.addLink(gnb, s1, bw=1000, delay="1ms", intfName1="gnb-s1", intfName2="s1-gnb")

    net.addLink(gnb2,  s1, bw=1000, delay="1ms", intfName1="gnb2-s1",  intfName2="s1-gnb2")
    net.addLink(ue2,  s1, bw=1000, delay="1ms", intfName1="ue2-s1",  intfName2="s1-ue2")


    
    print(f"*** Open5GS: Init subscriber for UE 0")
    o5gs   = Open5GS( "172.17.0.2" ,"27017")
    o5gs.removeAllSubscribers()
    with open( prj_folder + "/python_modules/subscriber_profile.json" , 'r') as f:
        profile = json.load( f )
    o5gs.addSubscriber(profile)
    print(f"*** Open5GS: Init subscriber for UE 1")
    with open( prj_folder + "/python_modules/subscriber_profile_gnb2.json" , 'r') as file:
        profile2 = json.load( file )
    o5gs.addSubscriber(profile2)
    print(f"*** Open5GS: Init subscriber for UE 2")


    info("\n*** Starting network\n")
    net.start()

    if not AUTOTEST_MODE:
        # spawnXtermDocker("open5gs")
        # spawnXtermDocker("gnb")
        info("*** Waiting for the configuration of the network to finish \n")
        time.sleep(20)
        
        #This is a common error that occurs, if you have a bad connection or if you are on a videocall and for many other reasons
        commonerror = 'ERROR: socket bind(2) [192.168.0.111]:38412 failed (99:Cannot assign requested address)'
        # ***** Testing configuration ****
        info("*** Configuration test *** \n")
        if(configurationTest('/home/vagrant/comnetsemu/app/5Gnetwork/log/amf.log',commonerror,8) is True):
            info("*** Configuration problem. Please, check your internet connection. \n")
            net.stop()
            os.system("sudo ./clean.sh")
            sys.exit(1)
        output = ue2.cmd('ifconfig')
        info("Interfaces :\n")
        info(output+"\n")
        while "uesimtun0:" not in output and "uesimtun1:" not in output:
            info("Waiting more time\n")
            time.sleep(5)
            output = ue2.cmd('ifconfig')
            info("Interfaces :\n")
            info(output+"\n")
        info("Configuration of the network ready\n***\n")

        # ***** Testing connectivity ***********
        info("*** Connections tests *** \n")
        output = ue2.cmd("ping -c 3 -n -I uesimtun0 www.google.com")
        info(output+"\n")
        if "3 packets transmitted, 3 received" not in output:
            info("Connections tests failed\n")
        output = ue2.cmd("ping -c 3 -n -I uesimtun1 www.google.com")
        info(output+"\n")
        if "3 packets transmitted, 3 received" not in output:
            info("Connections tests failed\n")

        info("Connections tests ok\n\n")
        info("*** Latency tests *** \n\n")
        first_cmd = './start_tcpdump.sh upf_cld'
        second_cmd = './start_tcpdump.sh upf_mec'
        # Starting two terminals and passing the commands
        tmuxCmd.start_two_terminals(first_cmd,second_cmd)
        output = ue2.cmd("ping -c 3 -n -I uesimtun0 10.45.0.1")
        info(output+"\n")
        if "3 packets transmitted, 3 received" in output:
            info("Latency test 1 passed\n")
        else :
            info("Latency test 1 failed\n")
        output = ue2.cmd("ping -c 3 -n -I uesimtun1 10.46.0.1")
        info(output+"\n")
        if "3 packets transmitted, 3 received" in output:
            info("Latency test 2 passed\n")
        else :
            info("Latency test 2 failed\n")
        
        info("*** Bandwith tests *** \n\n")
        output = ue2.cmd("iperf3 -c 10.45.0.1 -B 10.45.0.3 -t 5")
        info(output+"\n")
        if "iperf3: error" in output:
            info("Bandwith test 1 failed\n")
        else :
            info("Bandwith test 1 passed\n")
        output = ue2.cmd("iperf3 -c 10.46.0.1 -B 10.46.0.3 -t 5")
        info(output+"\n")
        if "iperf3: error" in output:
            info("Bandwith test 2 failed\n")
        else :
            info("Bandwith test 2 passed\n")
        
        
        info("*** Bandwith tests part 2 ***\n")
        
        #info("Updating subscribers")

        #script_path = "update_subscribers.py"
        # Run the script using the Python interpreter
        #subprocess.run(['sudo','python3', script_path], check=True)  

        # ue2.cmd("./nr-cli imsi-001011234567896 &")
        # time.sleep(5)
        # ue2.popen("docker exec nr-cli ps-establish IPv4 --sst 1 --sd 1 ")
        # time.sleep(5)
        # ue2.popen("docker exec nr-cli ps-establish IPv4 --sst 2 --sd 1 ")
        # time.sleep(5)
        # ue2.popen("docker exec nr-cli status")
        # time.sleep(5)
        # output = ue2.cmd("ifconfig")
        # info(output+"\n")
        # if "uesimtun2" not in output and "uesimtun3" not in output:
        #     info("Bandwith tests part 2 failed\n")
        # else :
        #     info("Bandwith tests part 2: Test 1 passed\n")
        #     output = ue2.cmd("iperf3 -c 10.45.0.1 -B 10.45.0.4 -t 5")
        #     info(output+"\n")
        #     if "iperf3: error" not in output:
        #         info("Bandwith tests part 2: Test 2 passed\n")
        #     output = ue2.cmd("iperf3 -c 10.46.0.1 -B 10.46.0.3 -t 5")
        #     info(output+"\n")
        #     if "iperf3: error" not in output:
        #         info("Bandwith tests part 3: Test 1 passed\n")

        info("*** Testing the connection ue2-ue1 *** \n")
        output = ue2.cmd("ping -c 3 -n -I uesimtun0 192.168.0.132")
        info(output+"\n")
        info("*** Testing the connection ue1-ue2 *** \n")
        output = ue.cmd("ping -c 3 -n -I uesimtun0 192.168.0.134")  
        info(output+"\n")  
        info("Test finished\n")

        subprocess.run(['tmux','kill-session', '-t','my_session'], check=True)
        
    net.stop()
    os.system("sudo ./clean.sh")