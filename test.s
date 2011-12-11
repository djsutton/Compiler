	.text
.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $8, %esp
	pushl %ebx
	pushl %edx
	pushl %esi
	pushl %edi
	movl $1, %eax
	sall $2, %eax
	orl $0, %eax
	pushl $0
	pushl $0
	pushl $0
	pushl %eax
	call print_any
	addl $16, %esp
	popl %edi
	popl %esi
	popl %edx
	popl %ebx

        movl $0, %eax
        leave
        ret

