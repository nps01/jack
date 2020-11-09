# 1)
def grid_repr(grid)->str:
    return "\n".join([" ".join([str(j) for j in i]) for i in grid])

print(grid_repr([[1,2,3],[3,4,5],[9,9,10]]))
# 2)

def is_even_list(int_list)->list:
    return [i % 2 == 0 for i in int_list]