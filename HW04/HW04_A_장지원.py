import random

NUMBER_OF_TRIALS = 10000


def matchTwoDecks():
    numMatches = 0

    # firstDeck과 secondDeck에는 각각 52장의 카드가 존재한다. (declare two decks)
    
    firstDeck = ['2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠','K♠', 'Q♠', 'A♠',
                 '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥', 'J♥', 'K♥', 'Q♥', 'A♥',
                 '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'K♣', 'Q♣', 'A♣',
                 '2◆', '3◆', '4◆', '5◆', '6◆', '7◆', '8◆', '9◆', '10◆', 'J◆', 'K◆', 'Q◆', 'A◆']
    
    secondDeck = firstDeck.copy()

    # firstDeck과 secondDeck의 카드를 잘 섞는다. (two shuffled decks of cards)

    random.shuffle(firstDeck)
    random.shuffle(secondDeck)

    # firstDeck과 secondDeck에서 각각 카트를 한 장씩 뽑아 같은 카드인지 비교한다.
    # (compares them and returns the number of matches)
    
    for i in range(52):
        if firstDeck[i] == secondDeck[i] :
            numMatches += 1

    return numMatches


def main():
     totalMatches = 0

     # 카드 비교를 총 10,000번 실행한다. 
     
     for i in range(NUMBER_OF_TRIALS):
         totalMatches += matchTwoDecks()

     # 같은 카드가 나오는 평균을 구한다.

     averageMatches = totalMatches / NUMBER_OF_TRIALS

     print("Average number of matched cards: {0:.3f}".format(averageMatches))

    

main()


    
