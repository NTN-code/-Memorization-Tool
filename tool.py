# write your code here
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# if os.path.exists('flashcard.db'):
#     os.remove('flashcard.db')

engine = create_engine('sqlite:///flashcard.db',  echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Flashcard(Base):
    __tablename__ = 'flashcard'
    question_id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box_number = Column(Integer)

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
                    flash_card = Flashcard(question=question, answer=answer, box_number=1)
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


def menu_update_delete(flash_card):
    print("""press "d" to delete the flashcard:
press "e" to edit the flashcard:""")
    flag_menu_update_delete = True
    while flag_menu_update_delete:
        user_choice = input()
        if user_choice == 'd':
            delete_flash_card(flash_card)
            flag_menu_update_delete = False
        elif user_choice == 'e':
            update_flash_card(flash_card)
            flag_menu_update_delete = False
        else:
            print(f'{user_choice} is not an option')


def update_flash_card(flash_card):
    print(f"current question: {flash_card.question}")
    print("please write a new question:")
    new_question = input()
    if new_question != ' ':
        flash_card.question = new_question
    print(f"current answer: {flash_card.answer}")
    print("please write a new answer:")
    new_answer = input()
    if new_answer != ' ':
        flash_card.answer = new_answer
    session.commit()
    

def delete_flash_card(flash_card):
    session.delete(flash_card)
    session.commit()


def menu_user_choice_correct(flash_card):
    flag_menu_user_user_correct = True
    while flag_menu_user_user_correct:
        print('press "y" if your answer is correct:')
        print('press "n" if your answer is wrong:')
        user_correct = input()
        if user_correct == "y":
            flash_card.box_number += 1
            flag_menu_user_user_correct = False
            session.commit()
        elif user_correct == "n":
            if flash_card.box_number != 1:
                flash_card.box_number -= 1
                session.commit()
            flag_menu_user_user_correct = False
        else:
            print(f'{user_correct} is not an option')
    if flash_card.box_number == 4:
        session.delete(flash_card)
        session.commit()


def menu_practice_flash_card():
    query = get_all_card()
    if query is not None:
        for flash_card in query:
            if flash_card.box_number != 4:
                question = flash_card.question
                answer = flash_card.answer
                flag_menu_practice_flash_card = True
                while flag_menu_practice_flash_card:
                    print(f"Question: {question}")
                    print('press "y" to see the answer:')
                    print('press "n" to skip:')
                    print('press "u" to update:')
                    user_choice = input()
                    if user_choice == 'y':
                        print(f"Answer: {answer}")
                        flag_menu_practice_flash_card = False
                        menu_user_choice_correct(flash_card)
                    elif user_choice == 'n':
                        flag_menu_practice_flash_card = False
                        menu_user_choice_correct(flash_card)
                        pass
                    elif user_choice == 'u':
                        menu_update_delete(flash_card)
                        flag_menu_practice_flash_card = False
                    else:
                        print(f'{user_choice} is not an option')
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
            if session.query(Flashcard).all():
                menu_practice_flash_card()
            else:
                print("There is no flashcard to practice!")
        elif user_choice == '3':
            print('Bye!')
            exit()
        else:
            print(f'{user_choice} is not an option')


def main():
    menu_main()


if __name__ == '__main__':
    main()
