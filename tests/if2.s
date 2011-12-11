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
	movl $1, %eax
	sall $2, %eax
	orl $0, %eax
	movl %eax, %edi
	movl $0, %ebx
	sall $2, %ebx
	orl $0, %ebx
	movl %edi, %eax
	andl $3, %eax
	cmpl $0, %eax
	sete %al
	movzbl %al, %ecx
	cmpl $0, %ecx
	je label_29_else
	movl %edi, %eax
	sarl $2, %eax
	cmpl $0, %eax
	setne %al
	movzbl %al, %ecx
	movl %ecx, %eax
	jmp label_30_if_end
label_29_else:
	movl %edi, %eax
	andl $3, %eax
	cmpl $1, %eax
	sete %al
	movzbl %al, %ecx
	cmpl $0, %ecx
	je label_27_else
	movl %edi, %eax
	sarl $2, %eax
	cmpl $0, %eax
	setne %al
	movzbl %al, %ecx
	movl %ecx, %eax
	jmp label_28_if_end
label_27_else:
	subl $12, %esp
	pushl %edi
	call is_true
	addl $16, %esp
	movl %eax, %ecx
	movl %ecx, %eax
label_28_if_end:
label_30_if_end:
	cmpl $0, %eax
	je label_37_else
	movl $1, %edi
	sall $2, %edi
	orl $0, %edi
	movl %ebx, %eax
	andl $3, %eax
	cmpl $0, %eax
	sete %al
	movzbl %al, %ecx
	cmpl $0, %ecx
	je label_33_else
	movl %ebx, %eax
	sarl $2, %eax
	cmpl $0, %eax
	setne %al
	movzbl %al, %ebx
	movl %ebx, %eax
	jmp label_34_if_end
label_33_else:
	movl %ebx, %eax
	andl $3, %eax
	cmpl $1, %eax
	sete %al
	movzbl %al, %ecx
	cmpl $0, %ecx
	je label_31_else
	sarl $2, %ebx
	cmpl $0, %ebx
	setne %al
	movzbl %al, %ebx
	movl %ebx, %eax
	jmp label_32_if_end
label_31_else:
	subl $12, %esp
	pushl %ebx
	call is_true
	addl $16, %esp
	movl %eax, %ebx
	movl %ebx, %eax
label_32_if_end:
label_34_if_end:
	cmpl $0, %eax
	je label_35_else
	movl $0, %esi
	sall $2, %esi
	orl $0, %esi
	jmp label_36_if_end
label_35_else:

label_36_if_end:
	jmp label_38_if_end
label_37_else:
	movl $2, %esi
	sall $2, %esi
	orl $0, %esi
label_38_if_end:
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

