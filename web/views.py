from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import re, json
import ipaddress

# Create your views here.

ipaddrmatch = re.compile('^(?:[0-9]{1,3}\.){3}[0-9]{1,3}(/[0-9]+)?$')
cidrmatch = re.compile('/[0-9]+$')

def showIndex(request):
	return render_to_response('templates/index.html', {}, context_instance=RequestContext(request))

def checkIP4(request):
	result = {'result': False}
	if request.POST.has_key('i'):
		try:
			addr = ipaddress.IPv4Address(request.POST['i'])
			result['result'] = True
			result['addrtype'] = 'ipv4'
		except:
			try:
				addr = ipaddress.IPv4Network(request.POST['i'], False)
				result['result'] = True
				result['addrtype'] = 'cidr4'
			except:
				pass
			pass
	
	
	return HttpResponse(json.dumps(result), {}, )

def calculateIP4(request):
	result = {'result': False}
	if request.POST.has_key('i') and request.POST.has_key('itype'):
		if request.POST['itype'] == 'ipv4':
			if request.POST.has_key('netmask'):
				addr = ipaddress.IPv4Address(request.POST['i'])
				network = ipaddress.IPv4Network('%s/%s' % (request.POST['i'], request.POST['netmask']), False)
				calresult = ip4netcal(network)
				if calresult:
					result['result'] = True
					result['output'] = calresult
		elif request.POST['itype'] == 'cidr4':
			network = ipaddress.IPv4Network(request.POST['i'], False)
			calresult = ip4netcal(network)
			if calresult:
				result['result'] = True
				result['output'] = calresult
			
	return HttpResponse(json.dumps(result), {})
	

def ip4netcal(cidr):
	netobj = ipaddress.IPv4Network(cidr, False)
	firsthost = netobj.network_address + 1
	lasthost = netobj.broadcast_address - 1
	output = {
		'version': netobj.version,
		'hostmask': str(netobj.hostmask),
		'firsthost': str(firsthost),
		'lasthost': str(lasthost),
		'isglobal': 'Yes' if netobj.is_global else 'No',
		'isprivate': 'Yes' if netobj.is_private else 'No',
		'ismulticast': 'Yes' if netobj.is_multicast else 'No',
		'netmask': str(netobj.netmask),
		'netbits': netobj.prefixlen,
		'broadcast_address': str(netobj.broadcast_address),
		'network_address': str(netobj.network_address),	
		'total': netobj.num_addresses,
		'usable': netobj.num_addresses - 2 if netobj.num_addresses > 0 else 1,
		'cidr': str(cidr),
	}
	return output

	return False
