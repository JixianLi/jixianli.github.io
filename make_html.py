import pandas as pd
import numpy as np

df = pd.read_csv("publication_list.csv", skipinitialspace=True)[::-1]
column_names = ['authors', 'title', 'venue', 'year', 'arxiv', 'github', 'doi', 'img']

for i, row in df.iterrows():
    authors = row['authors'].replace("Jixian Li", "<b>Jixian Li</b>")
    html = f'<div class=\"paper\"><img class=\"teaser\"src=\"{row['img']}\"/><br/>{authors}. \"{row["title"]}.\" {row["venue"]}, {row["year"]}<br/>'
    if not isinstance(row['arxiv'], float):
        html += f'<a href=\"{row["arxiv"]}\">arxiv</a> '
    if not isinstance(row['github'], float):
        html += f'<a href=\"{row["github"]}\">project</a> '
    if not isinstance(row['doi'], float):
        html += f'<a href=\"{row["doi"]}\">{"/".join(row["doi"].split('/')[-2:])}</a> '
    html += '</div><p onmouseover=\"meow(this)\" onmouseout=\'unmeow(this)\' style=\'color:white\'> *** MEOW *** </p>'
    print(html)