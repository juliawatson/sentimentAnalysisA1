import csv
import NLPlib
import sys
import re
import HTMLParser
import string


### twtt functions 1-9 ###

def twtt1(tweet):
    """
    (str) -> str
    Returns tweet with all HTML tags and attributes (i.e., /<[^>]+>/) removed.

    >>> twtt1('<a href=\"hope.html\">Computer Hope</a>')
    'Computer Hope'
    """
    return re.sub("<[^<]+>", "", tweet)

def twtt2(tweet):
    """
    (str) -> str
    Returns tweet with HTML character codes (i.e., &...;) replaced with an ASCII
    equivalent.

    >>> twtt2("Can you believe it&#33;&#63;")
    'Can you believe it!?'
    """
    html_parser = HTMLParser.HTMLParser()
    return str(html_parser.unescape(tweet))

def twtt3(tweet):
    """
    (str) -> str
    Returns tweet with URLs (i.e., tokens beginning with http or www) removed.

    >>> twtt3("Check out this link! www.smbc-comics.com")
    'Check out this link! '
    """
    return re.sub("((www)|(http))[^ ]+", "", tweet)

def twtt4(tweet):
    """
    (str) -> str
    Returns tweet with the first character in Twitter user names and hash tags
    (i.e., @ and #) removed

    >>> twtt4("@CaliM Thanks for telling me about that podcast #MFEO")
    'CaliM Thanks for telling me about that podcast MFEO'
    """
    split = tweet.split()
    for i in range(len(split)):
        if split[i][0] in ["@", "#"]:
            split[i] = split[i][1:]
    return ' '.join(split)

def twtt5(tweet):
    """
    (str) -> str
    Returns tweet with each sentence within a tweet is on its own line.

    >>> twtt5("I'll ask Dr. Phil about the Jan. fifth party on Colorodo Blvd.")
    "I'll ask Dr. Phil about the Jan. fifth party on Colorodo Blvd."
    >>> twtt5("Sounds like a good idea to me")
    'Sounds like a good idea to me'
    """

    sentences = []
    start = 0
    end = 0
    while end < len(tweet):

        # check for sentence boundaries when you see punctuation
        if tweet[end] in ".?!":

            if len(tweet) > end + 1 and tweet[end + 1] in string.punctuation:
                end += 1
                continue

            punctuation = tweet[end]
            preceeding_word = get_preceeding_word(tweet, end)

            # extend sentence boundary if punctuation is followed by quote
            if end + 1 < len(tweet) and tweet[end + 1] in ['\'', '\"']:
                end += 1

            # disqualify period boundaries when
            if punctuation == '.':
                next_c = next_non_blank_char(tweet, end)

                # known non-sent-final abbreviation
                if next_c is not None and \
                     preceeding_word in ABBRV_PN:
                    end += 1
                    continue

                # known abbreviation and next char is not lower
                elif preceeding_word in ABBRV and \
                    next_c is not None and next_c.islower():
                    end += 1
                    continue
            #TODO: discuss what to do with this section: textbook includes it as
            #TODO: q step, but I think it's not compatible with the twet corpus
            # disqualify ?! boundaries when next char is not lower
            #else:    # punctuaiton is ? or !
            #    next_c = next_non_blank_char(tweet, end)
            #    if next_c is not None and next_c.islower():
            #        end += 1
            #        continue

            sentences.append(tweet[start:end + 1])
            start = end + 1

        end += 1

    if start != end:
        sentences.append(tweet[start:end + 1])

    return '\n'.join(sentences)

def twtt7(tweet):
    """
    (str) -> str
    Returns a new version of tweet where each token, including punctuation and
    clitics, is separated by spaces.

    Note that:
        - Clitics are contracted forms of words, such as n't, that are
          concatenated with the previous word.
        - The possessive 's has its own tag and is distinct from the clitic 's,
          but nonetheless must be separated by a space; likewise, the possessive
          on plurals must be separated (e.g., dogs ').
        - ellipsis (i.e., '...'), and other kinds of multiple
          punctuation (e.g., '!!!') are not split.

    >>> twtt7("I'm so excited!!!")
    "I \'m so excited !!!"
    """

    abbreviations = ABBRV + ABBRV_PN

    sentences = tweet.split("\n")
    result = []

    # for each sentence
    for sent in sentences:
        sent_split = sent.split()
        new_sent_split = []

        # break apart each word
        for token in sent_split:
            leading_punctuation = []
            following_punctuation = []

            while token != "" and token[0] in string.punctuation and token not in abbreviations:
                leading_punctuation.append(token[0])
                token = token[1:]

            # separate punction if it's not an abbreviation
            while token != "" and token[-1] in string.punctuation and token not in abbreviations:
                following_punctuation.insert(0, token[-1])
                token = token[:-1]

            # merge occurrences of multiple punctuation
            leading_punctuation = merge_multiple_punctuation(leading_punctuation)
            following_punctuation = merge_multiple_punctuation(following_punctuation)

            # split on clitics if applicable
            token_parts = split_on_clitics(token)

            new_sent_split.extend(leading_punctuation)
            new_sent_split.extend(token_parts)
            new_sent_split.extend(following_punctuation)

        result.append(' '.join(new_sent_split))

    return '\n'.join(result)

def twtt8(tweet):
    """
    (str) -> str
    Returns sent with each token tagged with its part-of-speech.

    A tagged token consists of a word, the '/' symbol, and the tag
    (e.g., dog/NN)
    """
    sentences = tweet.split("\n")
    result = []
    for sent in sentences:
        sent = sent.split()
        tags = TAGGER.tag(sent)
        tagged_sent = []
        for word, tag in zip(sent, tags):
            tagged_sent.append(word + "/" + tag)
        result.append(' '.join(tagged_sent))
    return '\n'.join(result)

def twtt9(tweet, demarcation):
    """
    (str) -> str
    Returns sent with its demarcation '<A=#>', which occurs on its own lines,
    where # is the numeric class of the tweet (0 or 4).
    """
    demarcation_code = '<A=' + demarcation + ">\n"
    return demarcation_code + tweet

### twtt helper functions ###

def split_on_clitics(token):
    CLITICS = ["n\'t", "\'re", "\'m", "\'s", "\'ve", "\'d", "\'ll"]

    for chars in CLITICS:
        if re.search(chars + "$", token) is not None:
            return [token[:-len(chars)], chars]

    return [token]

def merge_multiple_punctuation(list_of_punct):
    """
    (list of str) -> list of str
     Returns a modified version of list_of_punct, where consecutive occurrences
     of the same punctuation are grouped together.

     >>> merge_multiple_punctuation([".", ".", ".", "," ,"!", "!", "!"])
     ['...', ',', '!!!']
    """
    result = []
    i = 0
    curr = ""
    while i < len(list_of_punct):
        if curr == "":
            curr = list_of_punct[i]
        elif curr[0] == list_of_punct[i]:
            curr = curr + list_of_punct[i]
        else:
            result.append(curr)
            curr = list_of_punct[i]
        i += 1
    if curr != "":
        result.append(curr)

    return result


def is_abbreviation(token):
    """
    (str) -> bool

    Returns True iff token is in abbreviation format.
    >>> is_abbreviation('twinkle.')
    False
    >>> is_abbreviation("e.")
    False
    >>> is_abbreviation("U.S.")
    True
    """
    return re.search("([a-zA-z]\.)([a-zA-z]\.)+", token) is not None


def next_non_blank_char(s, i):
    """
    (str, int) -> str or None

    Returns the first char in s after i that is not ' '. If there
    is no such character, returns None.

    >>> next_non_blank_char('Oh. Can I go home now?', 2)
    'C'
    """

    if i == len(s) - 1:
        return None

    i = i + 1
    while s[i] == ' ':
        if i == len(s) - 1:
            return None
        i += 1

    return s[i]

def get_preceeding_word(s, i):
    """
    (str int) -> str
    Returns the word in s that ends at index i.
    Precondition: len(s) >= 1
    Precondition: s[i] != ' '

    >>> get_preceeding_word('Oh. Can I go home now?', 2)
    'Oh.'
    """

    end = i
    start = i
    while start >= 0 and s[start] != ' ':
        start -= 1
    return s[start + 1 : end + 1]

def read_wordlist(file_path):
    """
    (str) -> list of str

    Returns a list containing the entries of a wordlist stored at
    file_path.
    """
    with open(file_path) as word_list_file:
        result = word_list_file.readlines()
    return [word_entry.strip() for word_entry in result]

### main helper functions ###

def twtt_all(tweet, demarcation):
    """
    (str, str) -> str
    Applies all
    """
    result = twtt1(tweet)
    result = twtt2(result)
    result = twtt3(result)
    result = twtt4(result)
    result = twtt5(result)
    result = twtt7(result)
    result = twtt8(result)
    result = twtt9(result, demarcation)
    return result

def get_start_line(csv_filename, student_id):

    with open(csv_filename) as open_csv:
        num_lines = sum(1 for line in open_csv)

    if num_lines >= 1600000:
        x = int(student_id) % 80
        return x * 10000

    return 0

def skip_x_lines(x, csv_lines):
    for i in range(x):
        temp = next(csv_lines)

def read_x_lines(x, lines):
    # save information from relevant lines
    tweets_result = []
    tweet_polarities_result = []
    i = 0
    for line in lines:
        if i > x:
            break
        tweet_text = line[5]
        tweet_polarity = line[0]
        tweets_result.append(tweet_text)
        tweet_polarities_result.append(tweet_polarity)
        i += 1
    return tweets_result, tweet_polarities_result

def get_tweets_and_polarities(input_lines):
    tweets_result = []
    tweet_polarities_result = []
    for line in input_lines:
        tweet_text = line[5]
        tweet_polarity = line[0]
        tweets_result.append(tweet_text)
        tweet_polarities_result.append(tweet_polarity)
    return tweets_result, tweet_polarities_result


def read_input_file(csv_filename, student_id):
    # calculate start line and end line from student number
    start_line = get_start_line(csv_filename, student_id)

    tweets = []
    tweet_polarities = []
    input_file = open(csv_filename)
    lines = list(csv.reader(input_file))
    input_file.close()

    if start_line > 0:
        relevant_lines = lines[start_line : start_line + 10000] + \
            lines[start_line + 800000 : start_line + 800000 + 10000]
    else:
        relevant_lines = lines[: min(len(lines), 20000)]

    for i in range(len(relevant_lines)):
        relevant_lines[i][5] = ''.join(char for char in relevant_lines[i][5] if ord(char) < 128)

    tweets, tweet_polarities = get_tweets_and_polarities(relevant_lines)

    return tweets, tweet_polarities

def main():

    # read in arguments
    if len(sys.argv) != 4:
        print("usage: python twtt.py csv_filename student_id output_filename")
    csv_filename = sys.argv[1]
    student_id = sys.argv[2]
    output_filename = sys.argv[3]

    # read input file
    tweets, tweet_polarities = read_input_file(csv_filename, student_id)

    # process each tweet from input file
    tted_tweet_data = []
    for i in range(len(tweets)):
        tted_tweet = twtt_all(tweets[i], tweet_polarities[i])
        tted_tweet_data.append(tted_tweet)

    # write all tweet data to output_file
    with open(output_filename, 'w') as output_file:
        for item in tted_tweet_data:
            output_file.write(item + "\")


if __name__ == "__main__":
    # initialize constants
    ABBRV = read_wordlist("abbrev.english")
    ABBRV_PN = read_wordlist("pn_abbrev.english")
    TAGGER = NLPlib.NLPlib()

    main()






