class Ship:
    def __init__(self, type, size, N_of_ship):
        self.size = size
        self.type = type
        self.n_of_ship = N_of_ship

    def get_size(self):
        return self.size

    def get_type(self):
        return self.type

    def decrease_n_of_ship(self):
        self.n_of_ship -= 1

    def is_available(self):
        return self.n_of_ship > 0