class InstructionLookup:
    def __init__(self):
        self.opcodeDict = {
            'XO-TYPE': {
                'add': 31,
                'subf': 31
            },
            'X-TYPE': {
                'and': 31,
                'nand': 31,
                'or': 31,
                'xor': 31,
                'sld': 31,
                'srd': 31,
                'srad': 31
            },
            'D-TYPE': {
                'addi': 14,
                'addis': 15,
                'andi': 28,
                'ori': 24,
                'xori': 26
            },
            'LA-TYPE': {
                'la': 13
            },
            'XS-TYPE': {
                'sradi': 31
            },
            'D2-TYPE': {
                'lwz': 32,
                'stw': 36,
                'stwu': 37,
                'lhz': 40,
                'lha': 42,
                'sth': 44,
                'lbz': 34,
                'stb': 38
            },
            'D3-TYPE': {
                'cmpi': 11
            },
            'DS-TYPE': {
                'ld': 58,
                'std': 62
            },
            'M-TYPE': {
                'rlwinm': 21
            },
            'X2-TYPE': {
                'extsw': 31
            },
            'X3-TYPE': {
                'cmp': 31
            },
            'B-TYPE': {
                'bc': 19,
                'bca': 19
            },
            'I-TYPE': {
                'b': 18,
                'ba': 18,
                'bl': 18
            }
        }

    def type(self, operator):
        for k in self.opcodeDict:
            if operator in self.opcodeDict[k]:
                return k

        return ''

    def opcode(self, operator):
        k = self.type(operator)
        if k == '':
            return -1

        return self.opcodeDict[k][operator]
