import paramiko
import sys 
import socket
import os

def getcmd(hostname,username,password,cmds,filename=''):
        try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname, username=username, password=password, port='22',look_for_keys=False, allow_agent=False)
                for cmd in cmds:
                        stdin,stdout,stderr=ssh.exec_command(cmd)
                        result = stdout.readlines()
                        resp=''.join(result)
                        if filename:
                                myfile = open(filename,"a")
                                myfile.write('\n\n\n'+cmd+':\n')
                                myfile.write(resp)
                                myfile.close()
                        else:
                                print '\n'+cmd+':\n'+resp
        except Exception as e:
                print e
                sys.exit(1)





def portstatus(server,ports):
	server    = server
	serverIP  = socket.gethostbyname(server)


	print "Please wait, scanning remote host,", serverIP, "This may take some time."



	try:
    
    		for port in ports:  
        		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        		result = sock.connect_ex((serverIP, port))
        		if result == 0:
            			print "Port {}: Open".format(port)
        			sock.close()
        		if result != 0:
            			print "Port {}: Closed".format(port)
        			sock.close()
    

	except socket.gaierror:
    		print 'Hostname could not be resolved.'
    		sys.exit()

	except socket.error:
    		print "Couldn't connect to server."
    		sys.exit()
