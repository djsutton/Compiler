	.text
.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $40, %esp
	pushl %ebx
	pushl %edx
	pushl %esi
	pushl %edi
	movl $1, %ebx
	sall $2, %ebx
	orl $0, %ebx
	subl $12, %esp
	pushl %ebx
	call create_list
	addl $16, %esp
	movl %eax, %ebx
	orl $3, %ebx
	movl $0, %esi
	sall $2, %esi
	orl $0, %esi
	movl $1, %ecx
	sall $2, %ecx
	orl $0, %ecx
	pushl $0
	pushl %ecx
	pushl %esi
	pushl %ebx
	call set_subscript
	addl $16, %esp
	movl %eax, %ecx
	movl %ebx, %esi
	movl $1, %ebx
	sall $2, %ebx
	orl $0, %ebx
	subl $12, %esp
	pushl %ebx
	call create_list
	addl $16, %esp
	movl %eax, %ebx
	orl $3, %ebx
	movl $0, %ecx
	sall $2, %ecx
	orl $0, %ecx
	movl $0, %edi
	sall $2, %edi
	orl $0, %edi
	pushl $0
	pushl %edi
	pushl %ecx
	pushl %ebx
	call set_subscript
	addl $16, %esp
	movl %eax, %ecx
	movl %esi, %eax
	andl $3, %eax
	cmpl $0, %eax
	sete %al
	movzbl %al, %ecx
	cmpl $0, %ecx
	je label_38_else
	movl %esi, %eax
	sarl $2, %eax
	movl %ebx, %ecx
	sarl $2, %ecx
	addl %ecx, %eax
	sall $2, %eax
	orl $0, %eax
	jmp label_39_if_end
label_38_else:
	movl %esi, %eax
	andl $3, %eax
	cmpl $1, %eax
	sete %al
	movzbl %al, %ecx
	cmpl $0, %ecx
	je label_36_else
	sarl $2, %esi
	movl %ebx, %eax
	sarl $2, %eax
	addl %eax, %esi
	movl %esi, %eax
	sall $2, %eax
	orl $0, %eax
	jmp label_37_if_end
label_36_else:
	movl $3, %ecx
	notl %ecx
	andl %esi, %ecx
	movl $3, %esi
	notl %esi
	andl %ebx, %esi
	subl $8, %esp
	pushl %esi
	pushl %ecx
	call add
	addl $16, %esp
	movl %eax, %ecx
	movl %ecx, %eax
	orl $3, %eax
label_37_if_end:
label_39_if_end:
	movl %eax, %esi
	pushl $0
	pushl $0
	pushl $0
	pushl %ebx
	call print_any
	addl $16, %esp
	pushl $0
	pushl $0
	pushl $0
	pushl %esi
	call print_any
	addl $16, %esp
	popl %edi
	popl %esi
	popl %edx
	popl %ebx

        movl $0, %eax
        leave
        ret

