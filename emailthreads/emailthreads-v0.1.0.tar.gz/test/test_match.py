import emailthreads
import os
import unittest
from email.message import EmailMessage
from email import message_from_file

class MatchBlocksTestCase(unittest.TestCase):
	def _open_file(self, name):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		return open(dir_path + "/data/" + name)

	def _load_msg_from_file(self, name):
		f = self._open_file(name)
		msg = message_from_file(f)
		f.close()
		return msg

	# def test_with_scissor(self):
	# 	patch = self._load_msg_from_file("scissor/patch.eml")
	# 	reply = self._load_msg_from_file("scissor/reply.eml")
	#
	# 	blocks = emailthreads.parse_blocks(reply)
	# 	blocks = emailthreads.match_quotes(blocks, patch)
	# 	blocks = emailthreads.trim_noisy_text(blocks)
	#
	# 	got = "\n".join([str(block) for block in blocks])
	#
	# 	f = self._open_file("scissor/output.txt")
	# 	want = f.read().strip()
	# 	f.close()
	#
	# 	self.assertEqual(got, want)

if __name__ == '__main__':
	unittest.main()
