#!/usr/bin/python3

def square(num):
    sq = num * num
    return rq
    

def cube(num):
    return num * num * num
    

def main():
    n = int(input('Enter a number: '))
    seq = 1
    while seq <= n:
        squ = square(seq, 2)
        cub = cube(seq, 3)
        print(f'The number is {seq}, its square is {squ} and its cube is {cub}.')
        seq += 1
        

if __name__ == '__main__':
    main()