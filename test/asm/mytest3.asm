.data
X: .word 1, -2, 3, 4, 5,
N: .word 5
SUM: .word 0
a: .word 4
b: .word -1

.text
la R1, N
ld R2, 0(R1)
la R3, X
la R10, SUM
la R11, a
la R12, b
ld R13, 0(R11)
ld R14, 0(R12)

loop:
ld R5, 0(R3)
add R3, R3, R13
add R4, R4, R5
add R2, R2, R14
cmp 7, 1, R2, R20
bc 7, 29, loop

std R4, 0(R10)
