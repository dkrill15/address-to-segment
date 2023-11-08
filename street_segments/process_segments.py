#!/usr/bin/env python3

import json
import math
import pandas as pd
import matplotlib.pyplot as plt


with open('segments.json', 'r') as file:
    streets = json.load(file)

with open('mod_Attom.csv', 'r') as file:
    ogdf = pd.read_csv('./mod_Attom.csv')
print(ogdf.shape[0])


#get list of distances form  only two coordiantes
coord_list = []
segment_count = 0
for item in streets:
    segment_count += 1
    length = len(streets[item]['coordinates'])
    if length <= 80:
        coord_list.append(length)

# You can adjust the number of bins as needed
plt.hist(coord_list, bins=20, edgecolor='black')

# Set labels and title
plt.xlabel('Coordinate Pairs')
plt.ylabel('Frequency')
plt.title('Number of Coordinate Pairs per Street Segment')

# Show the histogram
plt.show()

print(segment_count)
