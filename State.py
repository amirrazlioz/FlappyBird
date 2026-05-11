class State:
    def __init__(self, dist_x, dist_y, velocity):
        self.dist_x = dist_x  # מרחק אופקי לצינור הקרוב
        self.dist_y = dist_y  # מרחק אנכי למרכז הפתח
        self.velocity = velocity # מהירות הציפור
