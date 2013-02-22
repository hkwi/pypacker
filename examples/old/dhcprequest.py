#!/usr/bin/env python

import dnet
from pypacker import dhcp
from pypacker import udp
from pypacker import ip
from pypacker import ethernet

sysintf = 'eth0'
hw = dnet.eth(sysintf)
intf = dnet.intf()


# build ethernet frame
e = ethernet.Ethernet(
	dst = dnet.ETH_ADDR_BROADCAST,
	src = hw.get(),
	)

# build ip packet
i = ip.IP(
	dst = b"\xff\xff\xff\xff"),
	src = intf.get(sysintf)["addr"].ip,
	p = ip.IP_PROTO_UDP
	)

# build udp packet
u = udp.UDP(
	dport = 67,
	sport = 68,
	)

# build a dhcp discover packet to request an ip
d = dhcp.DHCP(
	chaddr = hw.get(),
	xid = 1337,
	op = dhcp.DHCPDISCOVER,
	)

#d.opts += o
#	opts = (
#            (dhcp.DHCP_OP_REQUEST, ''),
#            (dhcp.DHCP_OPT_REQ_IP, ''),
#            (dhcp.DHCP_OPT_ROUTER, ''),
#            (dhcp.DHCP_OPT_NETMASK, ''),
#            (dhcp.DHCP_OPT_DNS_SVRS, '')
#        )


p = e+i+u+d
# force update of length
p.len = 0

# send the data out
hw.send(e + i)
