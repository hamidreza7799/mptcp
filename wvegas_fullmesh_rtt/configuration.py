import os
import itertools
import argparse

parentFolderName = os.path.basename(os.getcwd())
splitArray = parentFolderName.split("_")
CONGESTION = splitArray[0]
PATHMANAGER = splitArray[1]
SCHEDULAR = splitArray[2]

readFilePath = "/home/vagrant/minitopo/experiments/iperf_scenario.py"
writeFilePath = "/home/vagrant/minitopo/experiments/iperf_scenario_2.py"

def FirstChangeIperfSenario():
    with open(readFilePath, "r") as r, open(writeFilePath, "w") as w:
        emptyThreeLine = False
        for i, line in enumerate(r):
            if i == 57 or i == 58 or i == 59:
                lineStrip = line.strip()
                if i == 57 and not (
                        lineStrip == 'self.topo.command_global("modprobe mptcp_rr && sysctl -w net.mptcp.mptcp_scheduler=roundrobin")' or lineStrip == '#self.topo.command_global("modprobe mptcp_rr && sysctl -w net.mptcp.mptcp_scheduler=roundrobin")'):
                    w.write(
                        '        ' + 'self.topo.command_global("modprobe mptcp_rr && sysctl -w net.mptcp.mptcp_scheduler=roundrobin")' + '\n')
                    w.write(
                        '        ' + 'self.topo.command_global("modprobe mptcp_ndiffports && sysctl -w net.mptcp.mptcp_path_manager=ndiffports ")' + '\n')
                    w.write(
                        '        ' + 'self.topo.command_global("echo 2 | sudo tee /sys/module/mptcp_ndiffports/parameters/num_subflows ")' + '\n' + '\n')
                    emptyThreeLine = True
                else:
                    if emptyThreeLine == True:
                        w.write(line)
                        continue
                    if i == 57:
                        if lineStrip == 'self.topo.command_global("modprobe mptcp_rr && sysctl -w net.mptcp.mptcp_scheduler=roundrobin")' or lineStrip == '#self.topo.command_global("modprobe mptcp_rr && sysctl -w net.mptcp.mptcp_scheduler=roundrobin")':
                            w.write(line)
                        else:
                            w.write(
                                '        ' + 'self.topo.command_global("modprobe mptcp_rr && sysctl -w net.mptcp.mptcp_scheduler=roundrobin")' + '\n')
                    if i == 58:
                        if lineStrip == 'self.topo.command_global("modprobe mptcp_ndiffports && sysctl -w net.mptcp.mptcp_path_manager=ndiffports ")' or lineStrip == '#self.topo.command_global("modprobe mptcp_ndiffports && sysctl -w net.mptcp.mptcp_path_manager=ndiffports ")':
                            w.write(line)
                        else:
                            w.write(
                                '        ' + 'self.topo.command_global("modprobe mptcp_ndiffports && sysctl -w net.mptcp.mptcp_path_manager=ndiffports ")' + '\n')
                    if i == 59:
                        if lineStrip == 'self.topo.command_global("echo 2 | sudo tee /sys/module/mptcp_ndiffports/parameters/num_subflows ")' or lineStrip == '#self.topo.command_global("echo 2 | sudo tee /sys/module/mptcp_ndiffports/parameters/num_subflows ")':
                            w.write(line)
                        else:
                            w.write(
                                '        ' + 'self.topo.command_global("echo 2 | sudo tee /sys/module/mptcp_ndiffports/parameters/num_subflows ")' + '\n')
            else:
                w.write(line)
    os.system('mv ' + writeFilePath + " " + readFilePath)

def ChangeIperfSenario():
    with open(readFilePath, "r") as r, open(writeFilePath, "w") as w:
        for i, line in enumerate(r):
            if i == 57 or i == 58 or i == 59:
                lineStrip = line.strip()
                if PATHMANAGER == "fullmesh" and SCHEDULAR == "rtt":
                    if lineStrip[0] == "#":
                        w.write(line)
                    else:
                        lineStrip = "        #" + lineStrip
                        w.write(lineStrip + "\n")
                elif PATHMANAGER == "fullmesh" and SCHEDULAR == "rr":
                    if i == 57 and lineStrip[0] == "#":
                        lineStrip = "        " + lineStrip[1:]
                        w.write(lineStrip + "\n")
                    elif i == 57 and lineStrip[0] != "#":
                        w.write(line)
                    if (i == 58 or i == 59) and lineStrip[0] == "#":
                        w.write(line)
                    elif (i == 58 or i == 59) and lineStrip[0] != "#":
                        lineStrip = "        #" + lineStrip
                        w.write(lineStrip + "\n")
                elif PATHMANAGER == "ndiffports" and SCHEDULAR == "rtt":
                    if i == 57 and lineStrip[0] == "#":
                        w.write(line)
                    elif i == 57 and lineStrip[0] != "#":
                        lineStrip = "        #" + lineStrip
                        w.write(lineStrip + "\n")
                    if (i == 58 or i == 59) and lineStrip[0] == "#":
                        lineStrip = "        " + lineStrip[1:]
                        w.write(lineStrip + "\n")
                    elif (i == 58 or i == 59) and lineStrip[0] != "#":
                        w.write(line)
                elif PATHMANAGER == "ndiffports" and SCHEDULAR == "rr":
                    if i == 57 and lineStrip[0] == "#":
                        lineStrip = "        " + lineStrip[1:]
                        w.write(lineStrip + "\n")
                    elif i == 57 and lineStrip[0] != "#":
                        w.write(line)
                    if (i == 58 or i == 59) and lineStrip[0] == "#":
                        lineStrip = "        " + lineStrip[1:]
                        w.write(lineStrip + "\n")
                    elif (i == 58 or i == 59) and lineStrip[0] != "#":
                        w.write(line)
                else:
                    continue
            else:
                w.write(line)
    os.system('mv ' + writeFilePath + " " + readFilePath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Configuration of Path Manager and Schedular")

    parser.add_argument("--mode", "-m",
                        help="first change in iperf_senario is mode 1 but after that is mode 2",default=2)

    args = parser.parse_args()

    if int(args.mode) == 1:
        FirstChangeIperfSenario()
    else:
        ChangeIperfSenario()