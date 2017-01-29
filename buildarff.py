import re
import sys
import csv

def feat1(tweet):
    return 0

def feat2(tweet):
    return 0

def feat3(tweet):
    return 0

def feat4(tweet):
    return 0

def feat5(tweet):
    return 0

def feat6(tweet):
    return 0

def feat7(tweet):
    return 0

def feat8(tweet):
    return 0

def feat9(tweet):
    return 0

def feat10(tweet):
    return 0

def feat11(tweet):
    return 0

def feat12(tweet):
    return 0

def feat13(tweet):
    return 0

def feat14(tweet):
    return 0

def feat15(tweet):
    return 0

def feat16(tweet):
    return 0

def feat17(tweet):
    return 0

def feat18(tweet):
    return 0

def feat19(tweet):
    return 0

def feat20(tweet):
    return 0

def get_tweet_features(tweets):

    tweet_feature_matrix = []

    tweet_feature_matrix.append([feat1(t) for t in tweets])
    tweet_feature_matrix.append([feat2(t) for t in tweets])
    tweet_feature_matrix.append([feat3(t) for t in tweets])
    tweet_feature_matrix.append([feat4(t) for t in tweets])
    tweet_feature_matrix.append([feat5(t) for t in tweets])
    tweet_feature_matrix.append([feat6(t) for t in tweets])
    tweet_feature_matrix.append([feat7(t) for t in tweets])
    tweet_feature_matrix.append([feat8(t) for t in tweets])
    tweet_feature_matrix.append([feat9(t) for t in tweets])
    tweet_feature_matrix.append([feat10(t) for t in tweets])
    tweet_feature_matrix.append([feat11(t) for t in tweets])
    tweet_feature_matrix.append([feat12(t) for t in tweets])
    tweet_feature_matrix.append([feat13(t) for t in tweets])
    tweet_feature_matrix.append([feat14(t) for t in tweets])
    tweet_feature_matrix.append([feat15(t) for t in tweets])
    tweet_feature_matrix.append([feat16(t) for t in tweets])
    tweet_feature_matrix.append([feat17(t) for t in tweets])
    tweet_feature_matrix.append([feat18(t) for t in tweets])
    tweet_feature_matrix.append([feat19(t) for t in tweets])
    tweet_feature_matrix.append([feat20(t) for t in tweets])

    return tweet_feature_matrix


def read_tweet_file(tweet_filename):
    """
    (str) -> (list of str, list of int)

    Returns tweets and polarities where tweets is a list of
    str containing tokenized tweets and polarities is a list of
    int denoting the polarities of the tweets at the same indices
    in tweets.
    """
    tweets = []
    polarities = []
    with open(tweet_filename) as tweet_file:
        for line in tweet_file:
            if search("<A=[0-9]>", line.strip()):
                polarities.append(int(line.strip()[3]))
                curr_tweet = ""
                while re.search("<A=[0-9]>", line.strip()) is None:
                    curr_tweet = curr_tweet + line
                tweets.append(curr_tweet)
    return tweets, polarities

def write_arff_file(tweet_feature_matrix, output_filename):
    """
    (list of list of int, str) -> None

    Write tweet_feature_matrix to csv output_filename with
    columns as rows.
    """

    if len(tweet_feature_matrix) == 0:
        return
    with open(output_filename) as output_file:
        csv_writer = csv.writer(output_file)
        for i in range(len(tweet_feature_matrix[0])):
            row = [tweet_feature_matrix[i] for feat in tweet_feature_matrix]
            csv_writer.writerow(row)

def main():
    # read in arguments
    if len(sys.argv) != 3:
        print("usage: python buildarff.py tweet_file.twt feature_output.arff")
    tweet_filename = sys.argv[1]
    output_filename = sys.argv[2]

    # read in input file
    tweets, polarities = read_tweet_file(tweet_filename)

    # construct output feature matrix
    tweet_feature_matrix = get_tweet_features(tweets)
    tweet_feature_matrix.append([int(p) for p in polarities])

    # write feature matrix to file
    write_arff_file(tweet_feature_matrix, output_filename)


if __name__ == "__main__":
    main()

