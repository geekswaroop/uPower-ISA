import re

from InstructionLookup import InstructionLookup
from Utils import Utils


class BaseInstruction(object):
    def __init__(self, instrRegex):
        self.instrRegex = re.compile(instrRegex)

    def parseInstr(self, instr):
        match = self.instrRegex.match(instr)
        if not match:
            return '', ()

        groups = filter(lambda x: x is not None, match.groups())
        operator = groups[0]
        operands = groups[1:]

        return operator, operands


class XOTypeInstruction(BaseInstruction):
    def __init__(self):
        XOTypeRegex = r'(\w+)\s+(R\d+)\W\s+(R\d+)\W\s+(R\d+)'
        super(XOTypeInstruction, self).__init__(XOTypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(XOTypeInstruction, self).parseInstr(instr)
        if operator == 'add':
            return operator, (operands[0], operands[1], operands[2], '0', '266', '0')
        if operator == 'subf':
            return operator, (operands[0], operands[1], operands[2], '0', '40', '0')


class XTypeInstruction(BaseInstruction):
    def __init__(self):
        XTypeRegex = r'(\w+)\s+(R\d+)\W\s+(R\d+)\W\s+(R\d+)'
        super(XTypeInstruction, self).__init__(XTypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(XTypeInstruction, self).parseInstr(instr)
        if operator == 'and':
            return operator, (operands[1], operands[0], operands[2], '28', '0')
        if operator == 'nand':
            return operator, (operands[1], operands[0], operands[2], '476', '0')
        if operator == 'or':
            return operator, (operands[1], operands[0], operands[2], '444', '0')
        if operator == 'xor':
            return operator, (operands[1], operands[0], operands[2], '316', '0')
        if operator == 'sld':
            return operator, (operands[1], operands[0], operands[2], '27', '0')
        if operator == 'srd':
            return operator, (operands[1], operands[0], operands[2], '539', '0')
        if operator == 'srad':
            return operator, (operands[1], operands[0], operands[2], '794', '0')


class DTypeInstruction(BaseInstruction):
    def __init__(self):
        DTypeRegex = r'(\w+)\s+(R\d+)\W\s+(R\d+)\W\s+(\d+)'
        super(DTypeInstruction, self).__init__(DTypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(DTypeInstruction, self).parseInstr(instr)
        if operator == 'addi':
            return operator, (operands[0], operands[1], operands[2])
        if operator == 'addis':
            return operator, (operands[0], operands[1], operands[2])
        if operator == 'andi':
            return operator, (operands[0], operands[1], operands[2])
        if operator == 'ori':
            return operator, (operands[0], operands[1], operands[2])
        if operator == 'xori':
            return operator, (operands[0], operands[1], operands[2])


class D2TypeInstruction(BaseInstruction):
    def __init__(self):
        D2TypeRegex = r'(\w+)\s+(R\d+)\W\s+(\d+)\W(R\d+)\W'  # Change the regex
        # r'(\w+)\s+(R\d+)\W\s+(\d+)\(R\d+\)'
        super(D2TypeInstruction, self).__init__(D2TypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(D2TypeInstruction, self).parseInstr(instr)
        if operator == 'lwz':
            return operator, (operands[0], operands[2], operands[1])
        if operator == 'stw':
            return operator, (operands[0], operands[2], operands[1])
        if operator == 'stwu':
            return operator, (operands[0], operands[2], operands[1])
        if operator == 'lhz':
            return operator, (operands[0], operands[2], operands[1])
        if operator == 'lha':
            return operator, (operands[0], operands[2], operands[1])
        if operator == 'sth':
            return operator, (operands[0], operands[2], operands[1])
        if operator == 'lbz':
            return operator, (operands[0], operands[2], operands[1])
        if operator == 'stb':
            return operator, (operands[0], operands[2], operands[1])


class XSTypeInstruction(BaseInstruction):
    def __init__(self):
        XSTypeRegex = r'(\w+)\s+(R\d+)\W\s+(R\d+)\W\s+(\d+)'
        super(XSTypeInstruction, self).__init__(XSTypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(XSTypeInstruction, self).parseInstr(instr)
        if operator == 'sradi':
            return operator, (operands[1], operands[0], operands[2], '413', '0', '0')


class DSTypeInstruction(BaseInstruction):
    def __init__(self):
        DSTypeRegex = r'(\w+)\s+(R\d+)\W\s+(\d+)\W(R\d+)\W'
        super(DSTypeInstruction, self).__init__(DSTypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(DSTypeInstruction, self).parseInstr(instr)
        if operator == 'ld':
            return operator, (operands[0], operands[2], operands[1], '0')
        if operator == 'std':
            return operator, (operands[0], operands[2], operands[1], '0')


class InstructionParser:
    def __init__(self, labelsMap={}):
        self.instrObjMap = {
            'XO-TYPE': XOTypeInstruction,
            'X-TYPE': XTypeInstruction,
            'D-TYPE': DTypeInstruction,
            'XS-TYPE': XSTypeInstruction,
            'D2-TYPE': D2TypeInstruction,
            'DS-TYPE': DSTypeInstruction

        }

        self.formatFuncMap = {
            'binary': lambda s, n: Utils.int2bs(s, n),
            'hex': lambda s, n: Utils.bs2hex(Utils.int2bs(s, n))
        }

        self.labelsMap = labelsMap

        self.instrLookup = InstructionLookup()
        self.instrObj = None

    def extractLabels(self, instr):
        if not instr:
            return '', ''

        split = instr.split(':', 1)

        if len(split) < 2:
            return '', instr

        return split[0], split[1].strip()

    def parse(self, instr):
        label, instr = self.extractLabels(instr)
        if not instr:
            return '', '', None

        operator = instr.split(' ')[0]
        instrType = self.instrLookup.type(operator)
        if not instrType:
            return '', '', None

        instrObj = self.instrObjMap[instrType]()
        operator, operands = instrObj.parseInstr(instr)

        if label:
            operands = list(operands)
            if label not in self.labelsMap:
                operands[-1] = None

            operands[-1] = str(self.labelsMap[label])
            operands = tuple(operands)

        return instrType, operator, operands

    def convert(self, instr, format='binary', formatFunc=None, instrFieldSizes=(6, 26)):
        if not instr:
            return ''

        if formatFunc is None:
            formatFunc = self.formatFuncMap[format]

        instrType, operator, operands = self.parse(instr)
        if not operator:
            return ''

        if instrType == 'XO-TYPE':
            instrFieldSizes = (6, 5, 5, 5, 1, 9, 1)
        if instrType == 'X-TYPE':
            instrFieldSizes = (6, 5, 5, 5, 10, 1)
        if instrType == 'D-TYPE':
            instrFieldSizes = (6, 5, 5, 16)
        if instrType == 'XS-TYPE':
            instrFieldSizes = (6, 5, 5, 5, 9, 1, 1)
        if instrType == 'D2-TYPE':
            instrFieldSizes = (6, 5, 5, 16)
        if instrType == 'DS-TYPE':
            instrFieldSizes = (6, 5, 5, 14, 2)

        opcode = self.instrLookup.opcode(operator)
        convertedOpcode = formatFunc(opcode, instrFieldSizes[0])
        operands = map(lambda op: op.strip('R,'), operands)
        convertedOperands = map(lambda (i, s): formatFunc(s, instrFieldSizes[i + 1]), enumerate(operands))

        convertedOutput = convertedOpcode + ''.join(convertedOperands)
        return convertedOutput


if __name__ == '__main__':
    # Test
    ip = InstructionParser()
    print ip.convert('add $6 $2 $4')
    print ip.convert('addi $2 $0 2', format='binary')
    print hex(int(ip.convert('addi $2 $0 2', format='binary'), 2))
