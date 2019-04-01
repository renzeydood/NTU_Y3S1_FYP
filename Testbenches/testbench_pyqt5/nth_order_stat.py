import numpy

print("Hello")

def main():
    inArr = [1, 6, 3, 9, 8, 5, 7]
    print("Ans:", minOfArr(inArr, 5))


def minOfArr(arr, pos):
    temp = arr[0]
    order = []

    for z in range(pos):
        for i in range(len(arr)):
            if(arr[i] < temp):
                temp = arr[i]
        order.append(temp)
    
    return temp

if __name__ == "__main__":
    main()