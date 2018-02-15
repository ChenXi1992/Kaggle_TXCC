import preprocessor as p
import enchant
import wordninja
from string import digits
import re
from keras.preprocessing.text import text_to_word_sequence


class PreSentence2Vec:
    @staticmethod
    # replace double space with single space ecc.
    def preProcessing(tweet):
        tweet = tweet.replace("can\'t","can not")
        tweet = tweet.replace("shan\'t", "shall not")
        tweet = tweet.replace("won\'t","will not")
        tweet = tweet.replace("it's","it is")
        tweet = tweet.replace("It's", "it is")
        tweet = tweet.replace("=", " ")
        tweet = tweet.replace("I'm","I am")
        tweet = tweet.replace("I m", "I am")
        tweet = tweet.replace("i m", "I am")
        tweet = tweet.replace("that's","that is")
        tweet = tweet.replace("That's","That is")


        tweet = tweet.replace('!', ' ')
        tweet = tweet.replace(':', ' ')
        tweet = tweet.replace('.', ' ')
        tweet = tweet.replace('?', ' ')
        tweet = tweet.replace("/", " ")
        tweet = tweet.replace("-", " ")
        tweet = tweet.replace("|", " ")
        tweet = tweet.replace(",", " ")
        tweet = tweet.replace(".", " ")
        tweet = tweet.replace("%", " ")
        tweet = tweet.replace("\n"," ")
        tweet = tweet.replace("\""," ")
        tweet = tweet.replace("'"," ")
        tweet = tweet.replace("("," ")
        tweet = tweet.replace(")"," ")

        return tweet



    @staticmethod
    # replace apostrophes in negative words
    def preApostrophes(tweet):
        words = [i.strip().lower() for i in tweet.split()]
        processedTweet = ""
        words_dic = {
            "can\'t": "can not",
            "shan\'t": "shall not",
            "won\'t": "will not",
            "n\'t": " not",
            "it\'s": "it is",
            "\'ll": " will",
            "\'m": " am",
            "\'ve": " have",
        }
        for text in words:
            processedTweet += words_dic.get(text, text) + " "

        return processedTweet

    @staticmethod
    # preprocess hashtags, count the appearance and replace #
    def preHashtag(tweet):
        words = tweet.split()
        num_of_hashtag = 0
        for index, word in enumerate(words):
            if word[0] == '\#':
                words[index] = words[index].strip(',.').lower()
                remove_digits = str.maketrans('', '', digits)
                words[index] = words[index].translate(remove_digits)
                words[index] = wordninja.split(words[index])
                num_of_hashtag += 1
        new_tweet = " ".join(words)
        return new_tweet, num_of_hashtag

    @staticmethod
    # remove the url in tweets, because it does not change the outcome
    def preNumberLink(tweet):
        p.set_options(p.OPT.URL,p.OPT.NUMBER)
        tweet = p.clean(tweet)
        return tweet

    def preURL(tweet):
        p.set_options(p.OPT.URL)
        tweet = p.clean(tweet)
        return tweet

    @staticmethod
    # count user references in tweets and replace the user namce with @user
    def preAtUser(tweet):
        words = tweet.split()
        num_of_mentions = 0
        for index, word in enumerate(words):
            if word[0] == '@':
                if len(word) > 1:
                    # words[index] = word[1:len(word)]
                    words[index] = "@user"
                    num_of_mentions += 1
                else:
                    words[index] = 'at'
        new_tweet = " ".join(words)
        return new_tweet, num_of_mentions

    @staticmethod
    # replace smileys with their meaning according to the notation in the tweets starting with a colon and ending with another one.
    # f.ex. :smile:
    def replaceSmilies(tweet):
        words = [i.strip().lower() for i in tweet.split()]
        processed_tweet = ""
        smiley_dic = {
            # ":)": ":smile:",
            # ":-)": ":smile:",
            ":-E": ":vampire:",
            ">-)": ":evil_grin:",
            # "^.^": ":grin:",
            # ":(": ":sad:",
            # ":-(": ":sad:",
            ":-<": ":super_sad:",
            ":P": ":sticking_tongue_out:",
            ":-O": ":surprised:",
            ":-*": ":kissing:",
            ":-$": ":confused:",
            ":-\\": ":shifty:",
            ":-/": ":shifty:",
            ":-#": ":secret:",
            "(((H)))": ":hugs:",
            ":-X": ":kissing:",
            "`:-)": ":one_eybrow_raised:",

            ":^)": ":broken_nose:",
            ":-&": ":tongue_tied:",
            "<:-)": ":uni_brow:",
            ":->": ":big_grin:",
            "(-}{-)": ":couple_kissing:",
            ":-Q": ":smoking:",
            "$_$": ":greedy:",
            ":-!": ":foot_in_mouth:",
            ":-D": ":laughter:",
            ".o.": ":laughter:",
            ":*)": ":drunk_smile:",
            ":@": ":angry:",
            ":-@": ":angry:",
            ":-0": ":yelling:",
            ":-----)": ":liar:",
            "%-(": ":confused:",
            ":-.)": ":vip:",
            ":-($)": ":greedy:",
            "(:I": ":egghead:",
            "|-O": ":yawning:",
            ":@)": ":pig_smile:",
            "<(-_-)>": ":robot:",
            "d[-_-]b": ":dj:",
            "~:0": ":baby:",
            "-@--@-": ":eye_glasses:",
            "\VVV/": ":king:",
            "\%%%/": ":queen:",
            ":'-)": ":crying_happy:",
            "{:-)": ":toupee_smile:",
            ";)": ":winking_smile:",
            ";-)": ":winking_smile:",
            "O:-)": ":angel:",
            "O*-)": ":angel:",
            "(:-D": ":blabbermouth:",
            # "@>--;--": ":rose:",
            # "@-}---": ":rose:",
            "=^.^=": ":cat:",
            "O.o": ":confused:",
            "X-)": ":confused:",
        }
        for word in words:
            processed_tweet += smiley_dic.get(word,
                                              word) + " "  # if smiley in dic replace otherwise use the current word
        return processed_tweet

    @staticmethod
    # remove colons and split smiley words at the dash (_)
    def preEmoticons(tweet):
        count_emoticons = len(re.findall(':\w+:', tweet))
        words = [i.strip() for i in tweet.split()]
        processed_tweet = ""
        for word in words:
            # if not word.startswith("https") and not word.startswith("http"):
            word = word.replace(":", " ")

            word = word.replace("_", " ")
            processed_tweet += word + " "

        return processed_tweet.replace("  ", " "), count_emoticons

    @staticmethod
    # Remove repetitive letters and replace them with punctuations for example
    # Needs further testing to find the best way of doing
    def preRepetitiveLetter(tweet):
        # remove the same letters after each other and check with a dictionary and take the first word
        # check this new word against the old word and add exclamation marks at the end according to the difference of letters
        english_dictionary = enchant.Dict("en_US")
        words = [i.strip() for i in tweet.split()]
        processed_tweet = ""
        counter = 0
        for word in words:
            new_word = ""
            old_letter = ""
            if english_dictionary.check(word) is False:
                for letter in list(word):
                    if letter is not old_letter:
                        new_word += letter
                    old_letter = letter
                if len(new_word) > 0 and str("!") not in new_word and str("?") not in new_word:
                    if english_dictionary.check(new_word) is True:
                        if len(word) >= len(new_word):
                            difference = abs(len(word) - len(new_word))
                            for i in range(difference):
                                new_word.join("!")
                            word = new_word
                            counter += difference
                    else:
                        if len(english_dictionary.suggest(new_word)) > 0:
                            suggestion_word = english_dictionary.suggest(new_word)[0]

                            word_dic = dict((c, 0) for i, c in enumerate(word))
                            for i in range(len(word)):
                                if word[i] in word_dic:
                                    if word_dic[word[i]] > 0:
                                        word_dic[word[i]] += 0.001
                                    else:
                                        word_dic[word[i]] += 1
                            word_sum = sum(word_dic.values())

                            new_word_dic = dict((c, 0) for i, c in enumerate(suggestion_word))
                            for i in range(len(suggestion_word)):
                                if suggestion_word[i] in new_word_dic:
                                    if new_word_dic[suggestion_word[i]] > 0:
                                        new_word_dic[suggestion_word[i]] += 0.001
                                    else:
                                        new_word_dic[suggestion_word[i]] += 1
                            new_word_sum = sum(new_word_dic.values())

                            # print(str(round(word_sum, 0)) + " " + str(round(new_word_sum, 0)))

                            if round(word_sum, 0) <= round(new_word_sum, 0):
                                new_word = suggestion_word
                                if len(word) >= len(new_word):
                                    difference = abs(len(word) - len(new_word))
                                    for i in range(difference):
                                        new_word.join("!")
                                    word = new_word
                                    counter += difference
            processed_tweet += word + " "

        return processed_tweet, counter

    @staticmethod
    # count the appearance of !, ?, ., and "
    def prePunctuation(tweet):
        tweet = tweet.replace('!', '')
        tweet = tweet.replace('. ', '')
        tweet = tweet.replace('?', '')
        tweet = tweet.replace('"', ' ')
        return tweet
    # def prePunctuation(tweet):
    #     num_excl = tweet.count('!')
    #     tweet = tweet.replace('!', '')
    #     num_ellipsis = tweet.count('.')
    #     tweet = tweet.replace('. ', '')
    #     num_question = tweet.count('?')
    #     tweet = tweet.replace('?', '')
    #     num_quotaions = tweet.count('"')
    #     tweet = tweet.replace('"', ' ')
    #     return tweet, num_excl, num_ellipsis, num_question, num_quotaions

    @staticmethod
    # count appearance of numbers and remove them
    def preNumber(tweet):
        # numbers = len(re.findall(r'\.*\d+\.*', tweet))
        p.set_options(p.OPT.NUMBER)
        return p.clean(tweet)

    @staticmethod
    # Split the sentence to word list.
    # PS: It will delete some punctuation information
    def sentenceToWordList(tweet):
        rgx = re.compile("(\w[\w']*\w|\w)")
        tweet = rgx.findall(tweet)
        return tweet


        # @staticmethod
        # def spliteWords(tweet):
        #     for sentence in range(0,len(tweet)):
        #         for word in range(0,len(sentence)):
        #
        #     return tweet


class PreNN:
    @staticmethod
    def testData(pre_url=True, pre_processing=True, pre_apostrophes=True, pre_user=True, pre_emoticons=True,
                         pre_hashtag=True, pre_number=True, pre_repetitive=True, pre_punctuation=True):
        filename = "./SemEval2018-T3_input_test_taskA.txt"
        X = []  # complete input text

        smiley_count = []  # list of smiley counts per tweet
        user_count = []  # list of user mentions per tweet
        number_count = []
        repetitive_letters = []
        exclamation_count = []  # number of exclamation marks per tweet
        ellipsis_count = []  # number of dots per tweet
        quotations_count = []  # number of quotation marks per tweet
        question_count = []  # number of question marks per tweet
        hash_count = []  # number of hashtags

        max_length = 0
        with open(filename, 'rt', encoding='utf8') as data_in:
            for x, line in enumerate(data_in):
                if not line.startswith("Tweet index"):  # discard first line if it contains metadata
                    line = line.rstrip()  # remove trailing whitespace
                    index = int(line.split("\t")[0])
                    tweet = line.split("\t")[1]
                    if x % 100 == 0:
                        print("tweet: " + str(index))

                    if pre_url:
                        tweet = PreSentence2Vec.preURL(tweet)
                    if pre_processing:
                        tweet = PreSentence2Vec.preProcessing(tweet)
                    if pre_apostrophes:
                        tweet = PreSentence2Vec.preApostrophes(tweet)
                    if pre_user:
                        tweet, user = PreSentence2Vec.preAtUser(tweet)
                    else:
                        user = 0
                    if pre_emoticons:
                        tweet = PreSentence2Vec.replaceSmilies(tweet)
                        tweet, smiley = PreSentence2Vec.preEmoticons(tweet)
                    else:
                        smiley = 0
                    if pre_hashtag:
                        tweet, hashtags = PreSentence2Vec.preHashtag(tweet)
                    else:
                        hashtags = 0
                    if pre_number:
                        tweet, numbers = PreSentence2Vec.preNumber(tweet)
                    else:
                        numbers = 0
                    if pre_repetitive:
                        tweet, repetitive = PreSentence2Vec.preRepetitiveLetter(tweet)
                    else:
                        repetitive = 0
                    if pre_punctuation:
                        tweet, num_excl, num_ellipsis, num_question, num_quotations = PreSentence2Vec.prePunctuation(tweet)
                    else:
                        num_excl = 0
                        num_ellipsis = 0
                        num_question = 0
                        num_quotations = 0

                    X.append(line)
                    smiley_count.append(smiley)
                    user_count.append(user)
                    number_count.append(numbers)
                    repetitive_letters.append(repetitive)
                    exclamation_count.append(num_excl)
                    ellipsis_count.append(num_ellipsis)
                    quotations_count.append(num_quotations)
                    question_count.append(num_question)
                    hash_count.append(hashtags)

                    words = text_to_word_sequence(tweet)
                    if len(words) > max_length:
                        max_length = len(words)

        return X, max_length, smiley_count, user_count, number_count, repetitive_letters, exclamation_count, ellipsis_count, question_count, quotations_count


    @staticmethod
    def preProcessTweets(do_preprocessing=True, pre_url=True, pre_processing=True, pre_apostrophes=True, pre_user=True, pre_emoticons=True,
                         pre_hashtag=True, pre_number=True, pre_repetitive=True, pre_punctuation=True):
        # source text
        filename = "./SemEval2018-T4-train-taskA.txt"
        preprocessed_dir = "./preprocessed_files/"
        additional_information = ""
        X = []  # complete input text
        y = []  # complete output categories

        smiley_count = []  # list of smiley counts per tweet
        user_count = []  # list of user mentions per tweet
        number_count = []
        repetitive_letters = []
        exclamation_count = []  # number of exclamation marks per tweet
        ellipsis_count = []  # number of dots per tweet
        quotations_count = []  # number of quotation marks per tweet
        question_count = []  # number of question marks per tweet
        hash_count = []  # number of hashtags

        max_length = 0
        iterations = 0
        if do_preprocessing:
            with open(filename, 'rt', encoding='utf8') as data_in:
                for x, line in enumerate(data_in):
                    if not line.startswith("Tweet index"):  # discard first line if it contains metadata
                        if iterations > 0:
                            action = "a+"
                        else:
                            action = "w+"
                            iterations += 1
                        line = line.rstrip()  # remove trailing whitespace
                        index = int(line.split("\t")[0])
                        label = int(line.split("\t")[1])
                        tweet = line.split("\t")[2]
                        if x % 100 == 0:
                            print("tweet: " + str(index))

                        if pre_url:
                            tweet = PreSentence2Vec.preURL(tweet)
                        if pre_processing:
                            tweet = PreSentence2Vec.preProcessing(tweet)
                        if pre_apostrophes:
                            tweet = PreSentence2Vec.preApostrophes(tweet)
                        if pre_user:
                            tweet, user = PreSentence2Vec.preAtUser(tweet)
                            with open(preprocessed_dir + "processedUserCount" + additional_information + ".txt", action, encoding='utf8') as file:
                                file.write(str(user) + "\n")
                        else:
                            with open(preprocessed_dir + "processedUserCount" + additional_information + ".txt", action, encoding='utf8') as file:
                                file.write(str(0) + "\n")
                        if pre_emoticons:
                            tweet = PreSentence2Vec.replaceSmilies(tweet)
                            tweet, smiley = PreSentence2Vec.preEmoticons(tweet)
                            with open(preprocessed_dir + "processedEmoticonsCount" + additional_information + ".txt", action, encoding='utf8') as file:
                                file.write(str(smiley) + "\n")
                        else:
                            with open(preprocessed_dir + "processedEmoticonsCount" + additional_information + ".txt", action, encoding='utf8') as file:
                                file.write(str(0) + "\n")
                        if pre_hashtag:
                            tweet, hashtags = PreSentence2Vec.preHashtag(tweet)
                            with open(preprocessed_dir + "processedHashtagCount" + additional_information + ".txt", action, encoding='utf8') as file:
                                file.write(str(hashtags) + "\n")
                        else:
                            with open(preprocessed_dir + "processedHashtagCount" + additional_information + ".txt", action, encoding='utf8') as file:
                                file.write(str(0) + "\n")
                        if pre_number:
                            tweet, numbers = PreSentence2Vec.preNumber(tweet)
                            with open(preprocessed_dir + "processedNumberCount" + additional_information + ".txt", action, encoding='utf8') as file:
                                file.write(str(numbers) + "\n")
                        else:
                            with open(preprocessed_dir + "processedNumberCount" + additional_information + ".txt", action, encoding='utf8') as file:
                                file.write(str(0) + "\n")
                        if pre_repetitive:
                            tweet, repetitive = PreSentence2Vec.preRepetitiveLetter(tweet)
                            with open(preprocessed_dir + "processedRepetitiveCount" + additional_information + ".txt", action, encoding='utf8') as file:
                                file.write(str(repetitive) + "\n")
                        else:
                            with open(preprocessed_dir + "processedRepetitiveCount" + additional_information + ".txt", action, encoding='utf8') as file:
                                file.write(str(0) + "\n")
                        if pre_punctuation:
                            tweet, num_excl, num_ellipsis, num_question, num_quotations = PreSentence2Vec.prePunctuation(tweet)
                            with open(preprocessed_dir + "processedExclamationCount" + additional_information + ".txt", action, encoding='utf8') as file:
                                file.write(str(num_excl) + "\n")
                            with open(preprocessed_dir + "processedQuestionCount" + additional_information + ".txt", action, encoding='utf8') as file:
                                file.write(str(num_question) + "\n")
                            with open(preprocessed_dir + "processedEllipsisCount" + additional_information + ".txt", action, encoding='utf8') as file:
                                file.write(str(num_ellipsis) + "\n")
                            with open(preprocessed_dir + "processedQuotationCount" + additional_information + ".txt", action, encoding='utf8') as file:
                                file.write(str(num_quotations) + "\n")
                        else:
                            with open(preprocessed_dir + "processedExclamationCount" + additional_information + ".txt", action, encoding='utf8') as file:
                                file.write(str(0) + "\n")
                            with open(preprocessed_dir + "processedQuestionCount" + additional_information + ".txt", action, encoding='utf8') as file:
                                file.write(str(0) + "\n")
                            with open(preprocessed_dir + "processedEllipsisCount" + additional_information + ".txt", action, encoding='utf8') as file:
                                file.write(str(0) + "\n")
                            with open(preprocessed_dir + "processedQuotationCount" + additional_information + ".txt", action, encoding='utf8') as file:
                                file.write(str(0) + "\n")

                        tweet = tweet.lower()

                        with open(preprocessed_dir + "processedTweets" + additional_information + ".txt", action, encoding='utf8') as file:
                            file.write(tweet + "\n")
                        with open(preprocessed_dir + "processedLabels" + additional_information + ".txt", action, encoding='utf8') as file:
                            file.write(str(label) + "\n")

        with open(preprocessed_dir + "processedTweets" + additional_information + ".txt", 'rt', encoding='utf8') as data_in:
            for line in data_in:
                X.append(line)
                words = text_to_word_sequence(line)
                if len(words) > max_length:
                    max_length = len(words)
        with open(preprocessed_dir + "processedLabels" + additional_information + ".txt", 'rt', encoding='utf8') as data_in:
            for line in data_in:
                y.append(int(line))
        with open(preprocessed_dir + "processedUserCount" + additional_information + ".txt", 'rt', encoding='utf8') as data_in:
            for line in data_in:
                user_count.append(int(line))
        with open(preprocessed_dir + "processedEmoticonsCount" + additional_information + ".txt", 'rt', encoding='utf8') as data_in:
            for line in data_in:
                smiley_count.append(int(line))
        with open(preprocessed_dir + "processedNumberCount" + additional_information + ".txt", 'rt', encoding='utf8') as data_in:
            for line in data_in:
                number_count.append(int(line))
        with open(preprocessed_dir + "processedRepetitiveCount" + additional_information + ".txt", 'rt', encoding='utf8') as data_in:
            for line in data_in:
                repetitive_letters.append(int(line))
        with open(preprocessed_dir + "processedExclamationCount" + additional_information + ".txt", 'rt', encoding='utf8') as data_in:
            for line in data_in:
                exclamation_count.append(int(line))
        with open(preprocessed_dir + "processedEllipsisCount" + additional_information + ".txt", 'rt', encoding='utf8') as data_in:
            for line in data_in:
                ellipsis_count.append(int(line))
        with open(preprocessed_dir + "processedQuestionCount" + additional_information + ".txt", 'rt', encoding='utf8') as data_in:
            for line in data_in:
                question_count.append(int(line))
        with open(preprocessed_dir + "processedQuotationCount" + additional_information + ".txt", 'rt', encoding='utf8') as data_in:
            for line in data_in:
                quotations_count.append(int(line))
        with open(preprocessed_dir + "processedHashtagCount" + additional_information + ".txt", "rt", encoding='utf8') as data_in:
            for line in data_in:
                hash_count.append(int(line))

        return X, y, max_length, smiley_count, user_count, number_count, repetitive_letters, exclamation_count, ellipsis_count, question_count, quotations_count
