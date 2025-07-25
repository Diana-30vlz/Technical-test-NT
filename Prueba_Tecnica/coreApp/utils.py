class MissingNumberFinder:
    """
    Clase para representar un conjunto de números y encontrar el número faltante (1 a 100).
    """
    def __init__(self, numbers_list):
        # Constructor
        self.numbers = numbers_list
        # (1 a 100).
        self.expected_range = set(range(1, 101))

    def validate_input(self):
        """
        Valida que los números en la lista de entrada estén dentro del rango esperado (1-100) y que tanga la cantidad 
        de elementos esperadas.
        """
        if not isinstance(self.numbers, list):
            return False, "La entrada debe ser una lista de números."
        
        if len(self.numbers) != 99:
            return False, f"La lista debe contener 99 números, pero se recibieron {len(self.numbers)}."

        for num in self.numbers:
            if not isinstance(num, (int, float)):
                return False, f"Todos los elementos de la lista deben ser números. Se encontró: {num}"
            if not (1 <= num <= 100):
                return False, f"Todos los números deben estar entre 1 y 100. Se encontró: {num}"
        
        return True, "" 

    def find_missing(self):
        """
        Calcula y devuelve el número faltante en el conjunto.
        Lanza ValueError si hay un error de validación o más de un número faltante.
        """
        is_valid, message = self.validate_input()
        if not is_valid:
            raise ValueError(message) 

        input_set = set(self.numbers)

        missing_numbers = list(self.expected_range - input_set)

        if len(missing_numbers) == 1:
            return missing_numbers[0]
        elif len(missing_numbers) == 0:
            raise ValueError("No parece faltar ningún número en el conjunto proporcionado.")
        else:
            raise ValueError(f"Parecen faltar múltiples números: {missing_numbers}")

    @staticmethod
    def generate_test_set(missing_num=None):
        """
        Método para generar un conjunto de los primeros 100 números
        con un número específico extraído.
        """
        import random
        full_set = list(range(1, 101))
        
        if missing_num is None:
            num_to_extract = random.choice(full_set)
        elif not (1 <= missing_num <= 100):
            raise ValueError("El número a extraer debe estar entre 1 y 100.")
        else:
            num_to_extract = missing_num

        if num_to_extract in full_set:
            full_set.remove(num_to_extract)
        
        return full_set, num_to_extract 