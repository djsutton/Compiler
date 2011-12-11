	.text
.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $24, %esp
	pushl %ebx
	pushl %edx
	pushl %esi
	pushl %edi
	movl $0, %eax
	sall $2, %eax
	orl $0, %eax
	movl $1, %ebx
	sall $2, %ebx
	orl $0, %ebx
	movl %ebx, %eax
	andl $3, %eax
	cmpl $0, %eax
	sete %al
	movzbl %al, %ecx
	cmpl $0, %ecx
	je label_18_else
	sarl $2, %ebx
	cmpl $0, %ebx
	setne %al
	movzbl %al, %ebx
	jmp label_19_if_end
label_18_else:
	movl %ebx, %eax
	andl $3, %eax
	cmpl $1, %eax
	sete %al
	movzbl %al, %ecx
	cmpl $0, %ecx
	je label_16_else
	movl %ebx, %eax
	sarl $2, %eax
	cmpl $0, %eax
	setne %al
	movzbl %al, %ebx
	jmp label_17_if_end
label_16_else:
	subl $12, %esp
	pushl %ebx
	call is_true
	addl $16, %esp
	movl %eax, %ebx
label_17_if_end:
label_19_if_end:
	cmpl $0, %ebx
	je label_20_else
	movl $1, %eax
	sall $2, %eax
	orl $0, %eax
	jmp label_21_if_end
label_20_else:
	movl $2, %eax
	sall $2, %eax
	orl $0, %eax
label_21_if_end:
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

