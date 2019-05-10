import sys
def k_n(n):
    matrix = list()
    for i in range(0,n):
        matrix.append([1] * n)

    for i in range(0,n):
        matrix[i][i] = 0

    print(matrix)
    f = open("k"+str(n)+".json", mode="w")

    f.write(''' {
"version" : 1,
"adj_matrix" : %s
    }'''  % matrix)

    f.close()

if __name__ == "__main__":
    k_n(int(sys.argv[1]))

