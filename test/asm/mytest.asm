.data
x: .word -5, 6, 7,
y: .asciiz 'Hello World'
zig: .word 8

.text
main:
addi R11, R14, -15
add R1, R4, R5
subf R6, R7, R8
and R1, R4, R5

loop:
or R1, R4, R5
xor R1, R4, R5
sld R11, R14, R15
srd R11, R14, R15
srad R11, R14, R15
addi R11, R14, 15
addis R1, R4, 5
andi R11, R14, 15
ori R1, R4, 5

loop2:
xori R11, R14, 15
sradi R11, R14, 5
lwz R1, 2(R3)
ld R12, 32(R5)

done:
rlwinm R11, R14, 5, 6, 7
extsw R14, R5
bc 7, 14, main
bca 7, 14, loop
b main
bl loop
cmp 7, 1, R4, R14
cmpi 7, 1, R5, 15
la R7, zig

