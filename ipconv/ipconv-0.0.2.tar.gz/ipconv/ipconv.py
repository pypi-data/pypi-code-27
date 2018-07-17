import re
import math

##########################################################
##########################################################
####												######
####	Author: Pranav Gajjewar						######
####	Github: github.com/Cartmanishere			######
####												######
##########################################################
##########################################################

class IPConv:

	def __init__(self, address):
		'''
		IPConv is a class used to crossconvert IP address into its various forms.
		'''
		self.REGEX_BIN = r'[01]{32}'
		self.REGEX_DD = r'((([1-2][0-9][0-9])|([1-9][0-9])|([0-9]))\.){3}(([1-2][0-9][0-9])|([1-9][0-9])|([0-9]))$'
		self.REGEX_HEX = r'([0-9abcdef]{2}\:){3}([0-9abcdef]{2})'
		self.REGEX_CIDR = r'((([1-2][0-9][0-9])|([1-9][0-9])|([0-9]))\.){3}(([1-2][0-9][0-9])|([1-9][0-9])|([0-9]))(\/((3[0-2])|([1-2][0-9])|([0-9])))$'
		self.cache = {}
		self.classless_mask = None
		self.bin_ip = self._validate_get_binary(address.strip().lower())
		self.cache['binary'] = self.bin_ip

	def __repr__(self):
		return '<IP {}>'.format(self.dotted_decimal())

	def desc(self):
		'''
		Describes the ip address
		'''
		show_block_info = True
		if self.bin_ip[0] == '0':
			_class = 'A'
			mask = 8
		else:
			if self.bin_ip[:4] == '1111':
				_class ='E'
				show_block_info = False
			elif self.bin_ip[:4] == '1110':
				_class = 'D'
				show_block_info = False
			elif self.bin_ip[:3] == '110':
				_class = 'C'
				mask = 24
			elif self.bin_ip[:2] == '10':
				_class = 'B'
				mask = 16
			else:
				_class = '?'
				show_block_info = False

		if show_block_info:
			_range, _first_ad, _last_ad = self._apply_mask(mask)
			_first_ad = self.dotted_decimal(ip=_first_ad, no_cache=True)
			_last_ad = self.dotted_decimal(ip=_last_ad, no_cache=True)

		show_cless_info = False if self.classless_mask is None else True
		if show_cless_info:
			_cless_range, _cless_first_ad, _cless_last_ad = self._apply_mask(self.classless_mask)
			_cless_first_ad = self.dotted_decimal(ip=_cless_first_ad, no_cache=True)
			_cless_last_ad = self.dotted_decimal(ip=_cless_last_ad, no_cache=True)

		print()		
		print('%-20s: %s' % ('Dotted-Decimal', self.dotted_decimal()))
		print('%-20s: %s' % ('Binary', self.bin_ip))
		print('%-20s: %s' % ('Hexadecimal', self.hexadecimal()))
		print()
		if show_block_info:
			print('Classful Addressing Scheme:')
			print('%-20s: %s' % ('Class', _class))
			print('%-20s: %s' % ('Network mask', mask))
			print('%-20s: %s' % ('Range', _range))
			print('%-20s: %s' % ('Network address', _first_ad))
			print('%-20s: %s' % ('Broadcast address', _last_ad))

		if show_cless_info:
			print()
			print('Classless Addressing Scheme:'.format(_class))
			print('%-20s: %s' % ('Network mask', self.classless_mask))
			print('%-20s: %s' % ('Range', _cless_range))
			print('%-20s: %s' % ('Network address', _cless_first_ad))
			print('%-20s: %s' % ('Broadcast address', _cless_last_ad))


		print()

	#####################
	# Utility functions #
	#####################

	def _validate_get_binary(self, address, update_cache=True):
		'''
		Validates entered address type and returns the binary equivalent of this address.
		'''

		# Detect IP type (binary, hexadecimal, dotted-decimal)
		match = re.search(self.REGEX_BIN, address)
		if match is not None:
			# Binary address
			return address

		else:
			match = re.search(self.REGEX_DD, address)
			if match is not None:
				# Dotted-decimal address
				if update_cache:
					self.cache['dotted_decimal'] = address
				return self._dotted_to_binary(address)

			else:
				match = re.search(self.REGEX_HEX, address)
				if match is not None:
					# Hexadecimal address
					if update_cache:
						self.cache['hexadecimal'] = address
					return self._hex_to_binary(address)

				else:
					match = re.search(self.REGEX_CIDR, address)
					if match is not None:
						# CIDR address
						ip_addr, mask = address.split('/')
						self.classless_mask = int(mask)
						if update_cache:
							self.cache['dotted_decimal'] = ip_addr
						return self._dotted_to_binary(ip_addr)
					else:
						raise ValueError('Unknown IP address notation. Use valid binary, hexadecimal or dotted-decimal notation.')

	def _dotted_to_binary(self, address):
		'''
		Converts valid dotted-decimal IP address and return its binary equivalent
		'''
		groups = list(map(lambda x: int(x), address.split('.')))
		# Convert each group into its equivalent binary string
		bin_ip = ''
		for val in groups:
			bin_ip += self._dec_to_bin(val, 8) # we want each group to be 8-bit binary

		return bin_ip
		
	def _hex_to_binary(self, address):
		'''
		Converts valid hexadecimal IP address and return its binary equivalent
		'''
		groups = list(map(lambda x: self._hexadecimal_to_decimal(x), address.split(':')))
		# Convert each group into its equivalent binary string
		bin_ip = ''
		for val in groups:
			bin_ip += self._dec_to_bin(val, 8) # we want each group to be 8-bit binary

		return bin_ip

	def _dec_to_bin(self, value, pad):
		'''
		Converts decimal integer 'value' to binary string of length 'pad' and return the string
		'''
		init_bin = self._decimal_to_binary(value)
		pad_val = pad - len(init_bin)

		return '0'*pad_val + init_bin

    ##################
    # Output methods #
    ##################    

	def dotted_decimal(self, ip=None, no_cache=False):
		'''
		Returns the dotted decimal form of the address.
		'''
		try:
			if no_cache:
				raise Exception
			assert self.cache['dotted_decimal']
			return self.cache['dotted_decimal']
		except Exception as e:
			# Convert 32-bit binary to dotted-decimal
			if ip == None:
				bin_ip = self.bin_ip
			else:
				bin_ip = self._validate_get_binary(ip)
			dec_vals = []
			for i in range(0, 32, 8):
				bin_val = bin_ip[i:i+8]
				dec_val = int(bin_val, 2)
				dec_vals.append(dec_val)

			dec_ip = '.'.join([ str(dec) for dec in dec_vals])
			if not no_cache:
				self.cache['dotted_decimal'] = dec_ip
			return dec_ip

	def hexadecimal(self, ip=None, no_cache=False):
		'''
		Returns the hexdecimal form of the address.
		'''
		try:
			if no_cache:
				raise Exception
			assert self.cache['hexadecimal']
			return self.cache['hexadecimal']
		except Exception as e:
			# Convert 32-bit binary to hexadecimal
			if ip == None:
				bin_ip = self.bin_ip
			else:
				bin_ip = self._validate_get_binary(ip)
			hex_val = ''
			for i in range(0, 32, 8):
				bin_val = bin_ip[i:i+8]
				dec_val = int(bin_val, 2)
				interim_val = str(hex(dec_val))[2:]
				if len(interim_val) < 2:
					interim_val = '0'+interim_val
				hex_val += interim_val + ':'


			hex_ip = hex_val.upper()[:-1]
			if not no_cache:
				self.cache['hexadecimal'] = hex_ip
			return hex_ip

	def binary(self):
		return self.bin_ip

    ###########################
    # Low Level conversions   #
    ###########################

	def _decimal_to_binary(self, value):
		'''
		Converts decimal value to binary value (returns string)
		'''
		_bin = ''
		_dec = value
		while _dec != 0:
			rem = _dec % 2
			_bin = str(rem) + _bin
			_dec = _dec // 2 

		return _bin

	def _hexadecimal_to_decimal(self, value):
		'''
		Converts hexadecimal string to decimal value (returns integer)
		'''
		_hex = value.lower()
		_dec = 0
		_hex_dict = { str(i): i for i in range(10) }
		_hex_dict['a'] = 10
		_hex_dict['b'] = 11
		_hex_dict['c'] = 12
		_hex_dict['d'] = 13
		_hex_dict['e'] = 14
		_hex_dict['f'] = 15

		for _hex_char, index in zip(_hex, range(len(_hex))):
			_dec += _hex_dict[_hex_char] * (16 ** index)

		return _dec



	##################
	# IP Operations  #
	##################

	def _apply_mask(self, mask, ip=None):
		'''
		Applies mask on the current ip with value n=mask and returns 3 things.
		range of the IP block, first address, last address
		'''    
		_range = 2 ** (32 - mask)
		_network_mask = '1' * mask + '0' * (32 - mask)
		if ip == None:
			_ip = self.bin_ip
		else:
			_ip = ip

		_first_address = self._bitwise_and(_ip, _network_mask)
		_last_address = self._bitwise_or(_ip, self._bitwise_not(_network_mask))

		return _range, _first_address, _last_address

	def _bitwise_and(self, ip1, ip2):
		'''
		Takes bitwise AND operation on two IPs
		'''
		_bin_ip1 = self._validate_get_binary(ip1, update_cache=False)
		_bin_ip2 = self._validate_get_binary(ip2, update_cache=False)
		_bin_and = ['1' if x=='1' and x==y else '0' for x, y in zip(_bin_ip1, _bin_ip2)]

		return ''.join([ _ for _ in _bin_and])

	def _bitwise_not(self, ip1):
		'''
		Takes bitwise NOT operation on IP
		'''
		_bin_ip = self._validate_get_binary(ip1, update_cache=False)
		return _bin_ip.translate(str.maketrans('01', '10'))

	def _bitwise_or(self, ip1, ip2):
		'''
		Takes bitwise OR operation on IP
		'''
		_bin_ip1 = self._validate_get_binary(ip1, update_cache=False)
		_bin_ip2 = self._validate_get_binary(ip2, update_cache=False)
		_bin_or = ['1' if x=='1' or y=='1' else '0' for x, y in zip(_bin_ip1, _bin_ip2)]

		return ''.join([ _ for _ in _bin_or])

	def increment(self, val):
		'''
		Returns the binary string obtained after adding 'val' to the ip.
		'''
		_int = int(self.bin_ip, 2) + val
		if _int == 4294967295:
			raise ValueError('Addition exceeds allowed IP range.')

		init_bin = bin(_int)[2:]
		pad_val = 32 - len(init_bin)

		return '0'*pad_val + init_bin

	######################
	# Data Model Methods #
	######################

	def __add__(self, ip):
		'''
		Data model method for addition
		'''
		if type(ip) == type(0):
			_int = ip
			if _int < 0:
				return self.__sub__(ip * (-1))

		elif type(ip) == type(self):
			_bin = ip.bin_ip
			_int = int(_bin, 2)
		else:
			raise ValueError('Cannot add {} to {}'.format(type(ip), type(self)))

		_self = int(self.bin_ip, 2)
		_dec_final = _int + _self
		if _dec_final > 2 ** 32:
			raise ValueError('Addition exceeds valid IP range.')

		_bin_final = self._dec_to_bin(_dec_final, 32)
		return IPConv(_bin_final)			

	def __sub__(self, ip):
		'''
		Data model method for subtraction
		'''
		if type(ip) == type(0):
			_int = ip
			if _int < 0:
				return self.__add__(ip * (-1))

		elif type(ip) == type(self):
			_bin = ip.bin_ip
			_int = int(_bin, 2)
		else:
			raise ValueError('Cannot subtract {} from {}'.format(type(ip), type(self)))

		_self = int(self.bin_ip, 2)
		_dec_final = _self - _int
		if _dec_final < 0:
			raise ValueError('Subtraction yields negative result. Not a valid IP.')

		_bin_final = self._dec_to_bin(_dec_final, 32)
		return IPConv(_bin_final)

	def next(self, value):
		'''
		Return an iterator that gives the next 'value' IP addresses
		'''
		_start = self
		for i in range(value):
			if _start.bin_ip != '1'*32:
				_start = _start + 1
				yield _start

	def prev(self, value):
		'''
		Returns an iterator that gives the prev 'value' IP addresses
		'''
		_start = self
		for i in range(value):
			if _start.bin_ip != '0'*32:
				_start = _start - 1
				yield _start




class Net:
	def __init__(self, ip1, ip2, _range):
		self.first = IPConv(ip1)
		self.last = IPConv(ip2)
		self.range = _range

	def __repr__(self):
		return "<subnet {}/{}>".format(self.first.dotted_decimal(), int(math.log(self.range, 2)))

class Subnet:
	def __init__(self, ip, n_subnets, init_calc=False):
		self.ip = IPConv(ip)
		if self.ip.classless_mask == None:
			raise ValueError('Invalid CIDR notation used to specify ip address.')

		# Convert number of subnets to 2's power
		_ = 0
		while 2 ** _ < n_subnets:
			_ += 1

		self.net_mask = self.ip.classless_mask
		self.n_subnets = n_subnets

		if self.net_mask + _ > 32:
			raise ValueError('Provided IP range cannot be subnetted into {} subnets.'.format(n_subnets))

		self.subnet_mask = self.net_mask + _

		self.block_range, block_first, block_last = self.ip._apply_mask(self.net_mask)
		self.block_first = IPConv(block_first)
		self.block_last = IPConv(block_last)
		self.subnet_range = 2 ** (32 - self.subnet_mask)
		if init_calc:
			self.subnets = self._make_subnets()
		else:
			self.subnets = []

	def desc(self, num=10, _type='dotted_decimal'):
		'''
		Print info of first num subnets
		'''
		if len(self.subnets) < 1:
			self.subnets = self._make_subnets()

		if num > self.n_subnets:
			num = self.n_subnets
		if num < 0:
			num = 10


		print()
		print('+'+'='*67+'+')
		print('|%-7s|' % ('Index'), end='')
		print('%-19s|' % ('First Address'), end='')
		print('%-19s|' % ('Last Address'), end='')
		print('%-19s|' % ('Range'))
		print('+'+'='*67+'+')
		for index in range(num):
			print('|%-7d|' % (index + 1), end='')
			print('%-19s|' % (self.subnets[index].first.dotted_decimal()), end='')
			print('%-19s|' % (self.subnets[index].last.dotted_decimal()), end='')
			print('%-19s|' % (self.subnets[index].range))
			print('-'*69)

	def _make_subnets(self):
		'''Return a list of n nets which are subnets of given IP range'''

		subnets = []
		cur_first = self.block_first
		for index in range(2 **(self.subnet_mask - self.net_mask)):
			_range, sub_first, sub_last = self.ip._apply_mask(self.subnet_mask, ip=cur_first.bin_ip)
			s = Net(sub_first, sub_last, _range)
			subnets.append(s)
			cur_first = IPConv(sub_last) + 1

		return subnets

	def first(self, value):
		'''
		Returns an iterator for the next 10 subnets.
		Each subnet returned has the following characteristics
			subnet.first, subnet.last, subnet.range
		'''
		if value > self.n_subnets:
			value = self.n_subnets

		for i in range(value):
			_start = self.block_first + (i) * self.subnet_range
			_range, sub_first, sub_last = self.ip._apply_mask(self.subnet_mask, ip=_start.bin_ip)
			yield Net(sub_first, sub_last, _range)


	def last(self, value):
		'''
		Returns an iterator for the last 10 subnets starting with last subnet
		Each subnet returned has following attributes
			subnet.first, subnet.last, subnet.range
		'''
		if value > self.n_subnets:
			value = self.n_subnets

		for i in range(self.n_subnets, self.n_subnets-1):
			_start = self.block_last + (i) * self.subnet_range
			_range, sub_first, sub_last = self.ip._apply_mask(self.subnet_mask, ip=_start.bin_ip)
			yield Net(sub_first, sub_last, _range)




def convert(address, _type='dotted'):
	ip = IPConv(address)
	if _type == 'binary':
		return ip.bin_ip
	elif _type == 'dotted':
		return ip.dotted_decimal()
	elif _type == 'hexdecimal':
		return ip.hexadecimal()
	else:
		raise ValueError('Unknown IP Address type: {}'.format(_type))

if __name__=="__main__":
	ip = IPConv('127.0.0.1')

