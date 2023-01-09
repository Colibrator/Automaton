
def rules(x, y, button_list, col1="black", col2="white") -> int:
    for i in range(x):
        for j in range(y):
            adjace_life = 0
            if i > 0 and button_list[i - 1][j]["bg"] == col2:
                adjace_life += 1
            if i > 0 and j < y - 1 and button_list[i - 1][j + 1]["bg"] == col2:
                adjace_life += 1
            if j < y - 1 and button_list[i][j + 1]["bg"] == col2:
                adjace_life += 1
            if i < x - 1 and j < y - 1 and button_list[i + 1][j + 1]["bg"] == col2:
                adjace_life += 1
            if i < x - 1 and button_list[i + 1][j]["bg"] == col2:
                adjace_life += 1
            if i < x - 1 and j > 0 and button_list[i + 1][j - 1]["bg"] == col2:
                adjace_life += 1
            if j > 0 and button_list[i][j - 1]["bg"] == col2:
                adjace_life += 1
            if i > 0 and j > 0 and button_list[i - 1][j - 1]["bg"] == col2:
                adjace_life += 1
            if (adjace_life < 2 or adjace_life > 3) and button_list[i][j]["bg"] == col2:
                button_list[i][j]["fg"] = col1
            elif adjace_life == 3 and button_list[i][j]["bg"] == col1:
                button_list[i][j]["fg"] = col2
    return adjace_life