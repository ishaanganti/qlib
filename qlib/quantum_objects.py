import numpy as np

class oper:
    def __init__(self, matrix):
        self.matrix = np.array(matrix, dtype=complex)

    def to_matrix(self):
        return self.matrix

    def dag(self):
        return oper(self.matrix.conj().T)

    def trace(self):
        return np.trace(self.matrix)

    def __add__(self, other):
        if isinstance(other, oper):
            return oper(self.matrix + other.matrix)
        raise TypeError("Cannot add oper with non-oper")

    def __sub__(self, other):
        if isinstance(other, oper):
            return oper(self.matrix - other.matrix)
        raise TypeError("Cannot subtract oper with non-oper")

    def __mul__(self, other):
        if isinstance(other, oper):
            return oper(np.matmul(self.matrix, other.to_matrix()))
        if isinstance(other, ket):
            return ket(np.matmul(self.matrix, other.to_vector()))
        if isinstance(other, (int, float, complex)):
            return oper(other * self.matrix)
        raise TypeError("Cannot multiply oper with non-compatible type")

    def __rmul__(self, other):
        if isinstance(other, (int, float, complex)):
            return oper(other * self.matrix)
        raise TypeError("Cannot multiply oper with non-compatible type")
    
    def commutator(self, other):
        if isinstance(other, oper):
            return self * other - other * self
        raise TypeError("Commutator can only be computed with another oper")

    def format(self, decimals=3):
        matrix = self.matrix
        format_string = "{:." + str(decimals) + "f}"
        if matrix.shape == (1, 1):
            formatted_matrix = f"[{format_string.format(matrix[0, 0])}]"
        else:
            formatted_matrix = "["
        
            for row in matrix:
                formatted_row = "[" + ", ".join([format_string.format(val) for val in row]) + "]"
                formatted_matrix += formatted_row + ";\n "
        
            formatted_matrix = formatted_matrix[:-3] + "]"
        return formatted_matrix

class ket:
    def __init__(self, vector):
        self.vector = np.array(vector, dtype=complex)

    def dim(self):
        return self.vector.shape[0]

    def to_vector(self):
        return self.vector

    def to_density_matrix(self):
        return oper(np.outer(self.vector, self.vector.conj()))

    def dag(self):
        return bra(self.vector.conj())

    def normalize(self):
        norm = np.linalg.norm(self.vector)
        if norm != 0:
            self.vector /= norm
        return self

    def norm(self):
        return np.linalg.norm(self.vector)

    def __add__(self, other):
        if isinstance(other, ket):
            return ket(self.vector + other.vector)
        raise TypeError("Cannot add ket with non-ket")

    def __sub__(self, other):
        if isinstance(other, ket):
            return ket(self.vector - other.vector)
        raise TypeError("Cannot subtract ket with non-ket")

    def __mul__(self, other):
        if isinstance(other, (int, float, complex)):
            return ket(other * self.vector)
        if isinstance(other, bra):
            return oper(np.outer(self.vector, other.to_vector()))
        raise TypeError("Cannot multiply ket with non-compatible type")

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def format(self, decimals=3):
        vector = self.vector
        format_string = "{:." + str(decimals) + "f}"
        formatted_vector = "[" + "; ".join([format_string.format(val) for val in vector]) + "]"
        return formatted_vector

class bra:
    def __init__(self, vector):
        self.vector = np.array(vector, dtype=complex)

    def to_vector(self):
        return self.vector

    def to_density_matrix(self):
        return oper(np.outer(self.vector.conj(), self.vector))

    def dag(self):
        return ket(self.vector.conj())

    def normalize(self):
        norm = np.linalg.norm(self.vector)
        if norm != 0:
            self.vector /= norm
        return self

    def norm(self):
        return np.linalg.norm(self.vector)

    def __add__(self, other):
        if isinstance(other, bra):
            return bra(self.vector + other.vector)
        raise TypeError("Cannot add bra with non-bra")

    def __sub__(self, other):
        if isinstance(other, bra):
            return bra(self.vector - other.vector)
        raise TypeError("Cannot subtract bra with non-bra")

    def __mul__(self, other):
        if isinstance(other, (int, float, complex)):
            return bra(other * self.vector)
        if isinstance(other, ket):
            return np.dot(self.vector, other.to_vector())
        if isinstance(other, oper):
            return bra(np.matmul(self.vector, other.to_matrix()))
        raise TypeError("Cannot multiply bra with non-compatible type")


    def __rmul__(self, other):
        return self.__mul__(other)
    
    def format(self, decimals=3):
        vector = self.vector
        format_string = "{:." + str(decimals) + "f}"
        formatted_vector = "[" + ", ".join([format_string.format(val) for val in vector]) + "]"
        return formatted_vector
    

def qprint(obj, decimal_places=3):
    if isinstance(obj, oper) or isinstance(obj, ket) or isinstance(obj, bra):
        print(obj.format(decimal_places))
    else:
        print(obj)