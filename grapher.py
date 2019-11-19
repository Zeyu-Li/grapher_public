''''
Grapher - By Andrew Li
graphing program that graphs data in data.json as a pie graph with labels
'''

# matplotlib + numpy
import matplotlib.pyplot as plt
import numpy as np
import json

def main():
    ''' main function
    '''


    # inits categories and the colors corresponding to each category
    categories = ['Homework', 'School', 'Coding', 'Workout/Sport', 'Misc', 'YouTube', 'Wasted', 'Food', 'Sleep']
    colors = ['blue', 'purple', 'orange', 'gold', 'green', 'red', 'darkgray', 'magenta', 'gray']

    # if data.json exists, get data as data_set, else return gile not found and exit
    try:
        with open('data.json', 'r') as fp:
            data_set = json.load(fp)
    except:
        print("File not found")
        return 1

    # formate labels such that it is formated as 'category: # hours'
    for index, category in enumerate(categories):
        categories[index] += (': ' + str(data_set[index]) + ' hours')

    matplot(data_set, categories, colors)


def matplot(data_set, categories, colors):
    ''' matplots the given data
    * data_set - set to be ploted
    * categories - categories of the given data set
    * colors - of the categories '''
    
    # if there are more labels, change the first number in figsize
    # otherwise, this code is copyed from:
    # https://matplotlib.org/3.1.1/gallery/pie_and_polar_charts/pie_and_donut_labels.html
    fig, ax = plt.subplots(figsize=(8, 3), subplot_kw=dict(aspect="equal"))

    wedges, texts = ax.pie(data_set, wedgeprops=dict(width=1), startangle=-60, colors = colors, shadow=True)


    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(categories[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment, **kw)

    # show chart
    plt.show()

# main function call
if __name__ == '__main__':
    main()
