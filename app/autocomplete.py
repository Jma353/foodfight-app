import os
import base64
import json
import urllib2

file1 = urllib2.urlopen('https://s3.amazonaws.com/stantemptesting/arizona_categories.json')
file2 = urllib2.urlopen('https://s3.amazonaws.com/stantemptesting/arizona_features.json')
arizona_categories = json.load(file1,encoding='utf8')
arizona_features = json.load(file2,encoding='utf8')

words = arizona_categories+arizona_features
def levenshtein( word1, word2 ):
    columns = len(word1) + 1
    rows = len(word2) + 1

    # build first row
    currentRow = [0]
    for column in xrange( 1, columns ):
        currentRow.append( currentRow[column - 1] + 1 )

    for row in xrange( 1, rows ):
        previousRow = currentRow
        currentRow = [ previousRow[0] + 1 ]

        for column in xrange( 1, columns ):

            insertCost = currentRow[column - 1] + 1
            deleteCost = previousRow[column] + 1

            if word1[column - 1] != word2[row - 1]:
                replaceCost = previousRow[ column - 1 ] + 1
            else:                
                replaceCost = previousRow[ column - 1 ]

            currentRow.append( min( insertCost, deleteCost, replaceCost ) )

    return currentRow[-1]
    
def run(input_val):
    TARGET = input_val
    results = []
    for word in words:
        cost = levenshtein(TARGET, word )
        if cost <= 1:
            results.append( (word, cost) )

    return results[0:5]