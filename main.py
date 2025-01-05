import json

def load_animals(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def load_questions(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def ask_questions(animals, questions):
    remaining_animals = animals.copy()
    asked_questions = set()  # track asked questions

    while len(remaining_animals) > 1:
        effectiveness = []
        for question in questions:
            if question['question'] in asked_questions:
                continue  # skip already asked questions
            
            if question['attribute'] == "color":
                yes_count = sum(1 for animal in remaining_animals if question['yes_value'] in animal[question['attribute']])
            else:
                yes_count = sum(1 for animal in remaining_animals if animal[question['attribute']] == question['yes_value'])
            
            no_count = len(remaining_animals) - yes_count
            
            # question must eliminate at least one animal
            if yes_count > 0 and no_count > 0:
                effectiveness.append((question, yes_count, no_count))

        if not effectiveness:
            print("No more questions available to ask.")
            break

        effectiveness.sort(key=lambda x: x[1], reverse=True)
        best_question, yes_count, no_count = effectiveness[0]
        asked_questions.add(best_question['question'])
        print(best_question['question'])
        answer = input("Answer (yes/no/maybe): ").strip().lower()

        if answer == "yes":
            if best_question['attribute'] == "color":
                remaining_animals = [animal for animal in remaining_animals if best_question['yes_value'] in animal[best_question['attribute']]]
            else:
                remaining_animals = [animal for animal in remaining_animals if animal[best_question['attribute']] == best_question['yes_value']]
        elif answer == "no":
            if best_question['attribute'] == "color":
                remaining_animals = [animal for animal in remaining_animals if best_question['yes_value'] not in animal[best_question['attribute']]]
            else:
                remaining_animals = [animal for animal in remaining_animals if animal[best_question['attribute']] != best_question['yes_value']]
        elif answer == "maybe":
            remaining_animals = [animal for animal in remaining_animals if animal[best_question['attribute']] != best_question['yes_value']]
        else:
            print("Invalid answer. Please respond with 'yes', 'no', or 'maybe'.")
            continue

        # print(f"Remaining animals: {[animal['name'] for animal in remaining_animals]}")

    if remaining_animals:
        print("I guess the animal you are thinking of is: " + remaining_animals[0]['name'])
    else:
        print("I couldn't guess the animal. Please try again!")

def main():
    animals = load_animals('animals.json')
    questions = load_questions('questions.json')
    
    print("Think of an animal, and I will try to guess it!")
    ask_questions(animals, questions)

if __name__ == "__main__":
    main()