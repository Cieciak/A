memory_size equ ext_mem_size_here ; Here is memory space used by A


includelib "kernel32.Lib"

extern GetStdHandle: PROTO
extern WriteConsoleA: PROTO
extern ReadConsoleA: PROTO
extern ExitProcess: PROTO

.data?
stdout dq ?
stdin dq ?
to_print db ?
to_write db 3 dup(?)
temp_one db ?

.data
instructions db instructions_here
end_of_instructions db 0ffh
memory db memory_size dup(0h)

.code
main proc
    ;Get handle id to console window & keyboard
    getioport:
        mov rcx, -11          ;/subsystem:console
        call GetStdHandle;        ;handle in rax
       	mov stdout, rax           ;save out handle
       	mov rcx, -10         ;keyboard code
       	call GetStdHandle         ;handle in rax
       	mov stdin, rax            ;save in handle

	lea rcx, instructions
	jmp exec_instruction
	
	increment:
		inc rcx

	exec_instruction:
		mov rbx, [rcx]
		and rbx, 0ffh

		; No operation
		cmp rbx, 00h
		je increment

		; Set pointer position
		cmp rbx, 01h
		je set_pointer_position

		; Set pointer value
		cmp rbx, 02h
		je set_pointer_value

		; Write pointer value to memory
		cmp rbx, 03h
		je write_pointer_value

		; Read pointer value from memory
		cmp rbx, 04h
		je read_pointer_value

		; Print value of the pointer
		cmp rbx, 05h
		je print_pointer_value

		; Input value
		cmp rbx, 06h
		je input_pointer_value

		; Add
		cmp rbx, 07h
		je dodaj

		cmp rbx, 08h
		je odejmij

		; Mul
		cmp rbx, 09h
		je mnoz

		; Div
		cmp rbx, 0Ah
		je dziel

		; Jump if 0
		cmp rbx, 0Bh
		je jump_if_pointer_zero

		cmp rbx, 0Ch
		je jump_if_smaller

		cmp rbx, 0Dh
		je jump

		; End execution
		cmp rbx, 0ffh
		je end_complete

		; You should never get here
		jmp increment

;
; Instructions
;
	set_pointer_position:
		inc rcx           ; Get next value
		lea r9, memory    ; Get starting adderess of program memory
		mov r15, [rcx]    ; Load value
		and r15, 0ffh     ; Make sure nothing else is moved
		add r9, r15       ; Set pointer position
		jmp increment

	set_pointer_value:
		inc rcx           ; Get next value
		mov r8, [rcx]     ; Set pointer value
		and r8, 0ffh      ; Make sure nothing else is moved
		jmp increment

	write_pointer_value:
		mov [r9], r8      ; Write to selected memory cell
		jmp increment

	read_pointer_value:
		mov r8, [r9]      ; Write from selected memory cell
		and r8, 0ffh      ; Tactical AND
		jmp increment

	;Add
	dodaj:
		mov r15, [r9]     ; Move cell value to r15 since you can't add to RAM
		and r15, 0ffh     ; Tactical AND again
		add r15, r8       ; Add
		mov [r9], r15     ; Write to RAM
		jmp increment

	;Sub
	odejmij:
		mov r15, [r9]     ; Move cell value to r15 since you can't add to RAM
		and r15, 0ffh     ; Tactical AND again
		sub r15, r8       ; Sub
		mov [r9], r15     ; Write to RAM
		jmp increment

	; Multiply
	mnoz:
		mov rax, [r9]     ; Move cell value to r15 since you can't add to RAM
		and rax, 0ffh     ; Tactical AND again
		mul r8            ; Multiply rax and r8
		mov [r9], rax     ; Write to RAM
		jmp increment

	dziel:
		push rdx          ; Save rdx
		xor rdx, rdx      ; Clear rdx
		mov rax, [r9]     ; Move value of selected memory cell to rax
		and rax, 0ffh     ; Tactical AND once again
		div r8d           ; Divide rax by r8
		mov [r9], rax     ; Wirite to RAM
		pop rdx           ; Restore rdx
		jmp increment

	jump_if_pointer_zero:
		inc rcx               ; Next memory cell
		lea r14, instructions ; Get starting position of instructions in RAM
		mov r15, [rcx]        ; Get instruction that you are jumping to
		and r15, 0ffh         ; AND (No idea what to put here)
		cmp r8, 0             ; Compare pointer value to 0
		jne increment         ; If not 0, next instruction
		add r14, r15          ; Calculate position in RAM
		mov rcx, r14          ; Put it in rcx (position register)
		dec rcx               ; Because code is jumping to increment decrement rcx by one
		jmp increment
		
	jump_if_smaller:
		inc rcx               ; Next memory cell
		lea r14, instructions ; Get starting position of instructions in RAM
		mov r15, [rcx]        ; Get instruction that you are jumping to
		and r15, 0ffh         ; AND (No idea what to put here)
		cmp r8, 0             ; Compare pointer value to 0
		jg increment          ; If not 0, next instruction
		add r14, r15          ; Calculate position in RAM
		mov rcx, r14          ; Put it in rcx (position register)
		dec rcx               ; Because code is jumping to increment decrement rcx by one
		jmp increment

	jump:
		inc rcx
		lea r14, instructions
		mov r15, [rcx]
		and r15, 0ffh
		add r15, r14
		mov rcx, r15
		dec rcx
		jmp increment


    ;Print
    print_pointer_value:
		mov to_print, r8b         ; Move value to print
		push rcx                  ; Save rcx
		push r9                   ; Save r9
		push r8                   ; Save r8
		mov rcx, stdout           ; I have no idea why?
		lea rdx, to_print         ; Tells CPU where to look
		mov r9, 0                 ; No saving
		mov r8, lengthof to_print ; Number of bytes to print
		call WriteConsoleA        ; Print
		pop r8                    ; Restore r8
		pop r9                    ; Restore r9
		pop rcx                   ; Restore rcx
		jmp increment

	; Input
	input_pointer_value:
		push rcx                  ; Save rcx
		push r9                   ; Save r9
		push r8                   ; Save r8
        mov rcx, stdin            ;	I still have no idea why?
        lea rdx, to_write         ;	Finds address in memory
        mov r8, lengthof to_write ;	Number of bytes to read
        lea r9, temp_one          ;	Store bytes actually read
		mov r15, r9               ;	Copy to r15
        call ReadConsoleA         ;	Get keystrokes
		pop r8                    ; Restore r8
		pop r9                    ; Restore r9
		pop rcx                   ; Restore rcx
		sub r15, 3                ; Move to beginig of qword
		mov r8, [r15]             ; Get byte
		and r8, 0ffh		      ; Make sure that nothing else got moved
		jmp increment
		
		
	end_complete:
		ret 0

main endp
end