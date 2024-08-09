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
        self.cells: list[list[Cell]] = [[Cell(self) for _ in range(cols)] for _ in range(rows)]

    def print(self) -> None:
        [print(row) for row in self.cells]

    def set(self, ref: str, content: str) -> None:
        row, col = self.ref_to_address(ref)
        # TODO validate content
        cell = self.cells[row][col]

        self.check_circular_dependency(cell, content)

        cell.set(content)

    def cell(self, ref) -> Cell:
        row, col = self.ref_to_address(ref)
        return self.cells[row][col]

    def get_refs(self, cell: Cell) -> list[Cell]:
        refs = self.exp_refs(cell.exp)
        return self.refs_to_cell(refs)

    def exp_refs(self, exp):
        return re.findall(self.pattern, exp)

    def refs_to_cell(self, refs: list):
        return [self.cell(ref) for ref in refs]

    def check_circular_dependency(self, cell: Cell, exp: str):
        def dfs(parent: Cell, deps: list[Cell]):
            children = self.get_refs(parent)

            circular_deps = [c for c in children if c in deps]

            if parent in children or circular_deps:
                raise RuntimeError("Circular dependency occurred - please check.")

            for child in children:
                new_deps = deps.copy()
                new_deps.append(parent)
                dfs(child, new_deps)

        # initial cell
        new_refs = self.exp_refs(exp)
        ref_cells = self.refs_to_cell(new_refs)

        if cell in ref_cells:
            raise RuntimeError("Circular dependency - first cell points to itself.")

        existing_dependencies = [cell]
        [dfs(rc, existing_dependencies) for rc in ref_cells]

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

    try:
        s.set('A1', 'A3')
    except RuntimeError as e:
        print("Caught exception:", e)
    s.print()
    print()
