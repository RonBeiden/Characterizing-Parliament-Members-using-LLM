from chat import *
import pandas as pd
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


# if __name__ == '__main__':
#     names = ["Miri_Regev", "Yair_Lapid"]
#     for name in names:
#       vote_titles = get_vote_titles_from_csv(f"const/{name}.csv")
#       kns_dict = eval_laws(vote_titles, name)
#       print(f"Evaluated laws for {name}:")