
class GameEngine:
    def __init__(self, player_1, player_2) -> None:
        self.table = [[None, None, None] for _ in range(3)]
        self.active_player = player_1
        self.player_1 = player_1
        self.player_2 = player_2

    def check_win_condition(self):
        # Проверка побед по горизонтали
        for row in self.table:
            if all(cell == row[0] and cell is not None for cell in row):
                return True

        # Проверка побед по вертикали
        for col in range(3):
            if all(self.table[row][col] == self.table[0][col] and self.table[row][col] is not None for row in range(3)):
                return True

        # Проверка побед по диагонали (левая верхняя - правая нижняя)
        if all(self.table[i][i] == self.table[0][0] and self.table[i][i] is not None for i in range(3)):
            return True

        # Проверка побед по диагонали (правая верхняя - левая нижняя)
        if all(self.table[i][2-i] == self.table[0][2] and self.table[i][2-i] is not None for i in range(3)):
            return True

        # Если ни одна из комбинаций не была найдена, возвращаем False
        return False
