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
	movl $0, %eax
	sall $2, %eax
	orl $0, %eax
	movl $1, %eax
	sall $2, %eax
	orl $0, %eax
	movl $1, %eax
	sall $2, %eax
	orl $0, %eax
	movl %eax, %ecx
	movl %ecx, %eax
	andl $3, %eax
	cmpl $0, %eax
	sete %al
	movzbl %al, %ebx
	cmpl $0, %ebx
	je label_42_else
	sarl $2, %ecx
	cmpl $0, %ecx
	setne %al
	movzbl %al, %ebx
	jmp label_43_if_end
label_42_else:
	movl %ecx, %eax
	andl $3, %eax
	cmpl $1, %eax
	sete %al
	movzbl %al, %ebx
	cmpl $0, %ebx
	je label_40_else
	movl %ecx, %eax
	sarl $2, %eax
	cmpl $0, %eax
	setne %al
	movzbl %al, %ebx
	jmp label_41_if_end
label_40_else:
	subl $12, %esp
	pushl %ecx
	call is_true
	addl $16, %esp
	movl %eax, %ebx
label_41_if_end:
label_43_if_end:
	cmpl $0, %ebx
	je label_48_else
	movl $1, %ebx
	sall $2, %ebx
	orl $0, %ebx
	movl $2, %edi
	sall $2, %edi
	orl $0, %edi
	movl %esi, %eax
	andl $3, %eax
	cmpl $0, %eax
	sete %al
	movzbl %al, %ebx
	cmpl $0, %ebx
	je label_46_else
	movl %esi, %eax
	sarl $2, %eax
	sarl $2, %edi
	addl %edi, %eax
	sall $2, %eax
	orl $0, %eax
	jmp label_47_if_end
label_46_else:
	movl %esi, %eax
	andl $3, %eax
	cmpl $1, %eax
	sete %al
	movzbl %al, %ebx
	cmpl $0, %ebx
	je label_44_else
	sarl $2, %esi
	sarl $2, %edi
	addl %edi, %esi
	movl %esi, %eax
	sall $2, %eax
	orl $0, %eax
	jmp label_45_if_end
label_44_else:
	movl $3, %ecx
	notl %ecx
	andl %esi, %ecx
	movl $3, %ebx
	notl %ebx
	andl %edi, %ebx
	subl $8, %esp
	pushl %ebx
	pushl %ecx
	call add
	addl $16, %esp
	movl %eax, %ebx
	movl %ebx, %eax
	orl $3, %eax
label_45_if_end:
label_47_if_end:
	movl %eax, %ebx
	movl $3, %esi
	sall $2, %esi
	orl $0, %esi
	movl $4, %esi
	sall $2, %esi
	orl $0, %esi
	pushl $0
	pushl $0
	pushl $0
	pushl %ebx
	call print_any
	addl $16, %esp
	jmp label_49_if_end
label_48_else:
	movl $7, %ebx
	sall $2, %ebx
	orl $0, %ebx
	movl $0, %eax
	sall $2, %eax
	orl $0, %eax
	movl %eax, %esi
	pushl $0
	pushl $0
	pushl $0
	pushl %ebx
	call print_any
	addl $16, %esp
label_49_if_end:
	popl %edi
	popl %esi
	popl %edx
	popl %ebx

        movl $0, %eax
        leave
        ret

