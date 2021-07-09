# write your code here
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

if os.path.exists('flashcard.db'):
    os.remove('flashcard.db')

engine = create_engine('sqlite:///flashcard.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Flashcard(Base):
    __tablename__ = 'flashcard'
    question_id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)

    def __repr__(self):
        return f"Flashcard {self.question_id}"


Base.metadata.create_all(engine)


def add_flash_card():
    flag_add_flash_card_question = True
    flag_add_flash_card_answer = True
    while flag_add_flash_card_question:
        question = input('Question:\n')
        if len(question) != 0:
            flag_add_flash_card_question = False
            while flag_add_flash_card_answer:
                answer = input('Answer:\n')
                if len(answer) != 0:
                    flash_card = Flashcard(question=question, answer=answer)
                    session.add(flash_card)
                    session.commit()
                    flag_add_flash_card_answer = False
        else:
            pass



def menu_add_flash_card():
    flash_add_flag = True
    while flash_add_flag:
        print("1. Add a new flashcard\n2. Exit")
        user_choice = input()
        if user_choice == '1':
            add_flash_card()
        elif user_choice == '2':
            flash_add_flag = False
        else:
            print(f'{user_choice} is not an option')


def get_all_card():
    flash_cards = session.query(Flashcard).all()
    return flash_cards


def count_flash_card():
    count_flash_card = session.query(Flashcard).count()
    return count_flash_card


def menu_practice_flash_card():
    query = get_all_card()
    count_flash_cards = count_flash_card()
    if query is not None:
        questions = [query[x].question for x in range(count_flash_cards)]
        answers = [query[x].answer for x in range(count_flash_cards)]
        flash_cards = [zip(questions, answers)]
        for flash_card in flash_cards:
            for question, answer in flash_card:
                user_choice = input(f"""Question: {question}
Please press "y" to see the answer or press "n" to skip: """)
                if user_choice == 'y':
                    print(f"Answer: {answer}")
                else:
                    pass
    else:
        print('There is no flashcard to practice!')


def menu_main():
    while True:
        print("""1. Add flashcards
2. Practice flashcards
3. Exit """)
        user_choice = input()
        if user_choice == '1':
            menu_add_flash_card()
        elif user_choice == '2':
            menu_practice_flash_card()
        elif user_choice == '3':
            print('Bye!')
            exit()
        else:
            print(f'{user_choice} is not an option')


def main():
    menu_main()


if __name__ == '__main__':
    main()
