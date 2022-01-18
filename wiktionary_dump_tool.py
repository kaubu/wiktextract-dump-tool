import json

DEBUG = True

print("Importing Wiktionary data...")

with open("data.json", "r", encoding="utf-8") as f:
    print("Data opened, loading entries.")

    while True:
        print("""[Wiktionary Dump Tool]
[1] Search word by word
[2] Search word by word in a specific language
[3] Search for a specific word
[4] Search word by word for words that have a translation
[5] Get translations word by word
[6] Get translations for a specific word
[q] Quit""")
        option = input(">> ")

        if option == "q":
            break
        elif option == "1":
            for line in f:
                # print(f"Type of f: {type(f)}") # <class '_io.TextIOWrapper'>
                data = json.loads(line)
                # print(f"Type of data: {type(data)}") # <class 'dict'>
                print(json.dumps(data, indent=2, sort_keys=True))
                input("Continue to next word")

        elif option == "2":
            lang = input("Language: ").lower()
            for line in f:
                data = json.loads(line)
                if data["lang"].lower() == lang:
                    print(json.dumps(data, indent=2, sort_keys=True))
                    input("Continue to next word")

        elif option == "3":
            word = input("Word: ")
            print("Searching...")
            for idx, line in enumerate(f):
                data = json.loads(line)
                data_word = data.get("word")
                if data_word == None:
                    continue
                if DEBUG: print(f"Progress: [{idx}, word: {data_word}]")
                
                if word == data_word:
                    print(json.dumps(data, indent=2, sort_keys=True))
                    break

        elif option == "4":
            for line in f:
                data = json.loads(line)
                if "translations" in data:
                    print(json.dumps(data, indent=2, sort_keys=True))
                    input("Continue to next word")
        
        elif option == "5":
            for line in f:
                data = json.loads(line)
                if "translations" in data:
                    quit_option = 0
                    senses = []
                    for translation in data["translations"]:
                        senses.append(translation["sense"])
                    
                    # Get rid of duplicates
                    translations = list(dict.fromkeys(senses))

                    while True:
                        print(f"['{data['word']}' Translations]")
                        for idx, translation in enumerate(translations):
                            print(f"[{idx+1}] {translation}")
                        print("""[w] Next word
[q] Exit""")

                        option = input("> ")

                        if option == "q":
                            quit_option = 1
                            break
                        if option == "w":
                            break
                        else:
                            dashes = "=" * 60
                            print(dashes)
                            print("{:<25s}{:<35s}".format("Language", "Translation"))
                            print(dashes)
                            for translation in data["translations"]:
                                if translation["sense"] == translations[int(option)-1]:
                                    # print(f"{translation['lang']}:\t\t\t\t{translation['word']}")
                                    print("{:<25s}{:<35s}".format(translation['lang'], translation['word']))

                    if quit_option == 1:
                        break

        elif option == "6":
            word = input("Word: ")
            print("Searching...")
            translation_found = False
            for idx, line in enumerate(f):
                data = json.loads(line)
                data_word = data.get("word")
                if data_word == None:
                    continue
                if DEBUG: print(f"Progress: [{idx}, word: {data_word}]")
                
                if word == data_word: # Keep going until it doesn't equal it
                    # print(json.dumps(data, indent=2, sort_keys=True))
                    if "translations" in data:
                        translation_found = True
                        senses = []
                        for translation in data["translations"]:
                            senses.append(translation["sense"])
                        
                        # Get rid of duplicates
                        translations = list(dict.fromkeys(senses))

                        while True:
                            print(f"['{data['word']}' Translations]")
                            for idx, translation in enumerate(translations):
                                print(f"[{idx+1}] {translation}")
                            print("[q] Next/Exit")

                            option = input("> ")

                            if option == "q":
                                break # Keeps going, since there are multiple definitions of words
                            else:
                                dashes = "=" * 60
                                print(dashes)
                                print("{:<25s}{:<35s}".format("Language", "Translation"))
                                print(dashes)
                                for translation in data["translations"]:
                                    if translation["sense"] == translations[int(option)-1]:
                                        print("{:<25s}{:<35s}".format(translation['lang'], translation['word']))
                        continue
                    else:
                        if translation_found:
                            print(f"No more translations available for '{word}'\n")
                        else:
                            print(f"No translations available for '{word}'\n")
                    break

print("All entries finished. Program ended.")