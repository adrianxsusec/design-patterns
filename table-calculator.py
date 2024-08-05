import ast
import re


class Cell:
    def __init__(self, sheet, exp=""):
        self.sheet = sheet
        self.exp: str = exp
        self.value = None
        self.observers: list[Cell] = []

        self.set(exp)

    def __repr__(self):
        return str(self.value)

    def set(self, content: str) -> None:
        self.exp = content

        dependencies: list[Cell] = self.sheet.get_refs(self)
        [d.add_observer(self) for d in dependencies]

        self.evaluate()

    def update_observers(self):
        [o.evaluate() for o in self.observers]

    def evaluate(self) -> None:
        self.determine_self_val()
        self.update_observers()

    def determine_self_val(self):
        refs: list[Cell] = self.sheet.get_refs(self)
        variables = {ref: self.sheet.cell(ref).value for ref in re.findall(self.sheet.pattern, self.exp)}
        self.value = self.eval_expression(self.exp, variables)

    def add_observer(self, cell) -> None:
        self.observers.append(cell)

    @staticmethod
    def eval_expression(exp, variables={}):
        if not exp:
            return None

        def _eval(node):
            if isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.Name):
                return variables[node.id]
            elif isinstance(node, ast.BinOp):
                return _eval(node.left) + _eval(node.right)
            else:
                raise Exception('Unsupported type {}'.format(node))

        node = ast.parse(exp, mode='eval')
        return _eval(node.body)


class Sheet:
    pattern = r'([A-Z]+[0-9]+)'

    def __init__(self, rows, cols):
        self.cells: list[list[Cell | None]] = [[Cell(self) for _ in range(cols)] for _ in range(rows)]

    def print(self) -> None:
        [print(row) for row in self.cells]

    def set(self, ref: str, content: str) -> None:
        row, col = self.ref_to_address(ref)
        # TODO validate content
        # TODO check circular dependency
        cell = self.cells[row][col]
        if not cell:
            self.cells[row][col] = Cell(self, content)
        else:
            cell.set(content)

    def cell(self, ref) -> Cell:
        row, col = self.ref_to_address(ref)
        return self.cells[row][col]

    def get_refs(self, cell: Cell) -> list[Cell]:
        refs = re.findall(self.pattern, cell.exp)
        return [self.cell(ref) for ref in refs]

    @staticmethod
    def ref_to_address(ref: str) -> (int, int):
        # TODO add bigger addresses
        # TODO check if ref is inside the table size
        pattern = re.compile(r'^[A-Z][0-9]+$')
        if bool(pattern.match(ref)):
            return ord(ref[0]) - ord("A"), int(ref[1])
        else:
            raise ValueError("Ref/address is not in valid form")


if __name__ == "__main__":
    s = Sheet(5, 5)
    print()

    s.set('A1', '2')
    s.set('A2', '5')
    s.set('A3', 'A1+A2')
    s.print()
    print()

    s.set('A1', '4')
    s.set('A4', 'A1+A3')
    s.print()
    print()
