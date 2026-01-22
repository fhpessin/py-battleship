from typing import List, Tuple


class Battleship:
    def __init__(self, ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]):
        # field rastreia o que está visível (vazio, deck, hit, sunk)
        self.field = [["~" for _ in range(10)] for _ in range(10)]
        # ships_decks armazena cada navio como uma lista de coordenadas de seus decks
        self.ships_decks = []

        for start, end in ships:
            ship_coords = self._get_ship_coordinates(start, end)
            self.ships_decks.append(ship_coords)
            for r, c in ship_coords:
                self.field[r][c] = u"\u25A1"  # □

    def _get_ship_coordinates(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[List[int]]:
        """Gera todas as coordenadas entre as extremidades do navio."""
        coords = []
        r1, c1 = start
        r2, c2 = end
        
        # Ordena para garantir que o range funcione (do menor para o maior)
        for r in range(min(r1, r2), max(r1, r2) + 1):
            for c in range(min(c1, c2), max(c1, c2) + 1):
                coords.append([r, c])
        return coords

    def fire(self, cell: Tuple[int, int]) -> str:
        row, col = cell
        target = [row, col]

        # Verifica se atingiu algum navio
        for ship in self.ships_decks:
            if target in ship:
                self.field[row][col] = "*"  # Marca como atingido
                ship.remove(target)  # Remove o deck "vivo" da lista do navio
                
                if not ship:  # Se não restam decks no navio
                    # Opcional: marcar todos os decks desse navio com 'x' no field
                    return "Sunk!"
                return "Hit!"

        return "Miss!"

    def print_field(self) -> None:
        """Imprime o estado atual do tabuleiro."""
        for row in self.field:
            print(" ".join(row))

    def _validate_field(self, ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> bool:
        """
        Valida as regras: 10 navios no total (4x1, 3x2, 2x3, 1x4) 
        e sem vizinhos adjacentes.
        """
        if len(ships) != 10:
            return False

        lengths = []
        occupied_cells = set()

        for start, end in ships:
            coords = self._get_ship_coordinates(start, end)
            lengths.append(len(coords))
            
            for r, c in coords:
                # Verifica se a célula ou vizinhos já estão ocupados
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        if (r + dr, c + dc) in occupied_cells:
                            return False
                occupied_cells.add((r, c))

        # Verifica a quantidade de cada tipo de navio
        return (
            lengths.count(1) == 4 and
            lengths.count(2) == 3 and
            lengths.count(3) == 2 and
            lengths.count(4) == 1
        )
