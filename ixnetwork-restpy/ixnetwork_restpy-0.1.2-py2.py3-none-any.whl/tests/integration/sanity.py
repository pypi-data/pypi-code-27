
if __name__ != '__main__':
	exit()

import sys
import os
sys.path[0] = os.path.abspath(sys.path[0] + '\\..\\..\\..\\')

from ixnetwork_restpy.testplatform.testplatform import TestPlatform
from ixnetwork_restpy.errors import IxNetworkError
from ixnetwork_restpy.files import Files

session = None

try:
	#test_platform = TestPlatform('10.36.79.20')
	test_platform = TestPlatform('127.0.0.1', rest_port=11009)
	test_platform.Trace = False
	test_platform.Authenticate('admin', 'admin')
	print(test_platform)

	for session in test_platform.Sessions():
		print(session)
	session = test_platform.add_Sessions()
	print(session)
	
	ixnetwork = session.Ixnetwork
	print(ixnetwork)

	try:
		ixnetwork.LoadConfig('c:/temp/ipv4_traffic.ixncfg')
		assert ('Type checking failed')
	except TypeError as e:
		print(e)
	ixnetwork.LoadConfig(Files('c:/users/anbalogh/downloads/ipv4_traffic.ixncfg', local_file=True))

	print(ixnetwork.Globals)
	print(ixnetwork.AvailableHardware)
	print(ixnetwork.Traffic)
	print(ixnetwork.Statistics)
	print(ixnetwork.ResourceManager)
	
	ixnetwork.NewConfig()
	
	assert(len(ixnetwork.Vport()) == 0)
	assert(len(ixnetwork.Topology()) == 0)
	assert(len(ixnetwork.AvailableHardware.Chassis()) == 0)
	assert(len(ixnetwork.Statistics.View()) == 0)
	assert(len(ixnetwork.Traffic.TrafficItem()) == 0)

	vport_name = 'Abstract Port 1'
	vport = ixnetwork.add_Vport(Name=vport_name, Type='pos')
	assert (vport.Type == 'pos')
	assert (vport.Name == vport_name)
	vport.Type = 'ethernet'
	assert (vport.Type == 'ethernet')
	vport.refresh()
	print(vport)

	topology = ixnetwork.add_Topology(Name='Device Group 1', Ports=[vport.href])
	print(topology)

	device_group = topology.add_DeviceGroup(Name='Device 1', Multiplier='7')
	print(device_group)
	device_group.Enabled.alternate('False')
	assert (device_group.Enabled == 'Alt: False')
	
	# create and print ethernet information
	ethernet = device_group.add_Ethernet()
	print(ethernet)

	# get multivalue information
	# # outputs format, count, possible patterns etc
	print(ethernet.Mac.info)

	# update multivalue on server immediately
	ethernet.Mac.decrement(start_value='00:00:de:ad:be:ef', step_value='00:00:fa:ce:fa:ce')
	assert (ethernet.Mac == 'Dec: 00:00:de:ad:be:ef, 00:00:fa:ce:fa:ce')
	ethernet.Mac.increment(start_value='00:00:fa:ce:fa:ce', step_value='00:00:de:ad:be:ef')
	assert (ethernet.Mac == 'Inc: 00:00:fa:ce:fa:ce, 00:00:de:ad:be:ef')
	ethernet.Mac.random()
	assert (ethernet.Mac == 'Rand')
	ethernet.Mac.randomRange()
	assert (ethernet.Mac.pattern.startswith('Randr:'))
	ethernet.Mac.randomMask()
	assert (ethernet.Mac.pattern.startswith('Randb:'))
	ethernet.Mac.distributed(algorithm='autoEven', mode='perPort', values=[('00:00:fa:ce:fa:ce', 60), ('0:00:de:ad:be:ef', 40)])
	assert (ethernet.Mac.pattern.startswith('Dist:'))
	ethernet.Mac.valueList(values=['00:00:fa:ce:fa:ce', '00:00:de:ad:be:ef'])
	assert (ethernet.Mac.pattern.startswith('List:'))
	ethernet.Mac.custom(start_value='00:00:fa:ce:fa:ce', step_value='00:00:de:ad:be:ef', increments=[('00:00:ab:ab:ab:ab', 6, [('00:00:01:01:01:01', 2, None)])])
	assert (ethernet.Mac.pattern.startswith('Custom:'))
	print(ethernet.Mac.values)

	ipv4 = ethernet.add_Ipv4(Name='Ipv4 1')
	print(ipv4)
	ipv4.Address.increment(start_value='1.1.1.1', step_value='0.1.1.1')
	assert(ipv4.Address == 'Inc: 1.1.1.1, 0.1.1.1')
	
	bgp4 = ipv4.add_BgpIpv4Peer(Name='Bgp 1')
	bgp4.Md5Key.string('my-md5-key-{Dec: 1,1}')
	print(bgp4)

	vports = ixnetwork.Vport(Name=vport_name)
	assert(len(vports) == 1)
	assert(vports[0].Name == vport_name)

	bgp6 = topology.add_DeviceGroup(Name='Device 2').add_Ethernet().add_Ipv6().add_BgpIpv6Peer()
	print(bgp6)

	vports[0].AddQuickFlowGroups([vports[0].href], 2)
	config = ixnetwork.ResourceManager.ExportConfig(['/descendant-or-self::*'], False, 'json')
	ixnetwork.ResourceManager.ImportConfig(config, True)

	# errors = ixnetwork.Globals.AppErrors()[0].Error(Name='JSON Import Errors')
	# for instance in errors[0].Instance():
	# 	print(instance)

	chassis = ixnetwork.AvailableHardware.add_Chassis(Hostname='10.36.24.55')
except IxNetworkError as e:
	print(e)

if session is not None:
	session.Stop()


