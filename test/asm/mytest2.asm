.data
x: .word 5
zig: .word 6
y: .word 0

.text

main:
addi R1, R2, -5
la R4, x
la R5, zig
ld R6, 0(R4)
ld R7, 0(R5)
nand R8, R6, R7
la R9, y
std R8, 0(R9)
cmp 7, 1, R6, R7
bc 7, 28, done
add R8, R6, R7
std R8, 0(R9)


done:
subf R8, R6, R7
