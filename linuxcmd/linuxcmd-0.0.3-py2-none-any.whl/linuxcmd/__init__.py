import paramiko
import sys 

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


