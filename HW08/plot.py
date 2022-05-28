import matplotlib.pyplot as plt
# import numpy as np

# the objective value of the current point at every iteration is recorded in a text file.


def main():
    first_y = []
    anneal_y = []

    first_infile = open('first.txt', 'r')
    anneal_infile = open('anneal.txt', 'r')
    
    plt.figure(figsize=(10, 10))
    plt.title("Search Performance (TSP-100)")
    plt.xlabel('Number of evaluations') 
    plt.ylabel('Tour Cost')   

    line = first_infile.readline()
    while line != '':
        first_y.append(float(line))  
        line = first_infile.readline()
    first_infile.close()

    line2 = anneal_infile.readline()
    while line2 != '':
        anneal_y.append(float(line2))
        line2 = anneal_infile.readline()  
    anneal_infile.close()

    first_x = [i for i in range(len(first_y))]
    anneal_x = [i for i in range(len(anneal_y))]

    plt.xticks(range(0, 60000, 10000))   
    plt.yticks(range(0, 6000, 1000))         
    plt.plot(first_x, first_y, label='First-Choice HC')
    plt.plot(anneal_x, anneal_y, label='Simulated Annealing')
    plt.gca().invert_yaxis()
    plt.gca().invert_yaxis()   


    plt.legend(loc='upper right')
    plt.show()


main()