from chat import *
import pandas as pd
import os
import time

eval_dict = {}

def get_vote_titles_from_csv(file_path: str) -> list:
    """
    Read a CSV file and return a list of unique values from the 'sess_item_dscr' column.

    Parameters:
    -----------
    file_path : str
        Path to the CSV file.

    Returns:
    --------
    list
        List of unique values from the 'sess_item_dscr' column.
    """
    df = pd.read_csv(file_path)
    return df['sess_item_dscr'].dropna().unique().tolist()

def eval_laws(queries, name):
    add = """תענה רק בעד או נגד בלי לפרט"""
    # Define the prompt for evaluating laws
    for query in queries:
        eval_dict[query] = chatbot(query+add, name)
    # Save the eval_dict to a CSV file
    eval_df = pd.DataFrame(eval_dict.items(), columns=['Query', 'Response'])
    eval_df.to_csv(f'{name}_bot.csv', index=False, encoding='utf-8-sig')
    return eval_dict

def get_abs_path(relative_path):
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def eval_laws_to_full_kns(query, name):
    eval_dict[name] = chatbot(query, name)
    clear_memory()

def eval_laws_from_csv(file_path, description):
    file_path_abs = get_abs_path(os.path.join("..", "eval", "laws", file_path))
    description_path_abs = get_abs_path(os.path.join("..", "eval", "laws", description))
    
    df = pd.read_csv(file_path_abs)
    kns_names = df["english_name"].tolist()
    kns_names = [name.replace(" ", "_") for name in kns_names]
    
    with open(description_path_abs, "r", encoding="utf-8") as file:
        description_law = file.read()
    
    query = (
        "The title of the law is: " + description[:-4] + "\n"
        "The description of the law is: " + description_law + "\n"
        "What is your opinion about this law?\n"
    )
    add = "תענה רק בעד או נגד בלי לפרט ותענה בעברית"
    query = query + add
    kns_names = kns_names
    for name in kns_names:
        print(f"Evaluating {name}...")
        if not collection_exists(name):
            continue
        eval_laws_to_full_kns(query, name)
        time.sleep(1)
    eval_df = pd.DataFrame(eval_dict.items(), columns=['Name', 'Response'])
    output_path = get_abs_path(f"{description[:-4]}_res.csv")
    eval_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    eval_dict.clear()

if __name__ == '__main__':
    # 1: law = "חוק לתיקון פקודת המשטרה (מס' 37)"
    law = "חוק-יסוד השפיטה (תיקון מס' 4)"
    file_path = law + ".csv"
    description = law + ".txt"
    eval_laws_from_csv(file_path, description)
    