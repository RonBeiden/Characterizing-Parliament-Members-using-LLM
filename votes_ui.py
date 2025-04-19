import gradio as gr
import pandas as pd

# Your existing functions
def get_person_id(members_df, first_name, last_name):
    filtered_df = members_df[(members_df['FirstName'] == first_name) & 
                           (members_df['LastName'] == last_name)]
    if len(filtered_df) > 0:
        return filtered_df.iloc[0]['mk_individual_id']
    return None

def filter_votes_by_mk(votes_df, mk_id):
    return votes_df[votes_df['mk_individual_id'] == mk_id]

def get_vote_result_by_name(members_df, votes_df, first_name, last_name, vote_title):
    id = get_person_id(members_df, first_name, last_name)
    if id is None:
        return f"Person {first_name} {last_name} not found."
    filtered_votes = filter_votes_by_mk(votes_df, id)
    result = filtered_votes[filtered_votes['sess_item_dscr'] == vote_title]
    if result.empty:
        return "No vote data found for this member and vote combination."
    vote_status = "In Favor" if result.iloc[0]['vote_result'] == 1 else "Against"
    return f"{first_name} {last_name} voted {vote_status} on {vote_title}"

# Demo function for Gradio
def lookup_vote(last_name, first_name, vote_title):
    # Load your data here
    try:
        members_df = pd.read_csv("members_df.csv")
        votes_df = pd.read_csv("votes_df.csv")
    except Exception as e:
        return f"Error loading data: {e}"
    
    return get_vote_result_by_name(members_df, votes_df, first_name, last_name, vote_title)

# Get your data for the dropdowns
try:
    members_df = pd.read_csv("members_df.csv")
    votes_df = pd.read_csv("votes_df.csv")
    last_names = sorted(members_df['LastName'].unique().tolist())
    first_names = sorted(members_df['FirstName'].unique().tolist())
    vote_titles = sorted(votes_df['sess_item_dscr'].unique().tolist())
except Exception as e:
    last_names = ["Error loading data"]
    first_names = ["Error loading data"]
    vote_titles = ["Error loading data"]

# Create the Gradio interface
demo = gr.Interface(
    fn=lookup_vote,
    inputs=[
        gr.Dropdown(choices=last_names, label="Last Name"),
        gr.Dropdown(choices=first_names, label="First Name"),
        gr.Dropdown(choices=vote_titles, label="Vote Title")
    ],
    outputs="text",
    title="Knesset Vote Lookup",
    description="Find out how Knesset members voted on specific issues"
)

demo.launch()