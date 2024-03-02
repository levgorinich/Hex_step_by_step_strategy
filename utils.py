def oddq_offset_neighbor(self, hex, direction):
    oddq_direction_differences = [
        # even cols
        [[+1, 0], [+1, -1], [0, -1],
         [-1, -1], [-1, 0], [0, +1]],
        # odd cols
        [[+1, +1], [+1, 0], [0, -1],
         [-1, 0], [-1, +1], [0, +1]],
    ]


    parity = hex[0] & 1
    diff = oddq_direction_differences[parity][direction]
    return (hex[0] + diff[0], hex[1] + diff[1])
