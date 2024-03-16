import re
from datetime import date, datetime

from util import *

def process_md_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    file_name = os.path.basename(file_path)
    file_name = file_name[:-3] # assumption is that file_path ends with .md

    # Extract tags
    tags = extract_tags(file_path)

    # Extract last practice date
    date_pattern = re.compile(r'Last Practice Date: (\d{4}-\d{2}-\d{2})')
    date_match = date_pattern.search(content)
    last_practice_date = datetime.strptime(date_match.group(1), '%Y-%m-%d') if date_match else None

    # Extract body of the .md: it is everything after ---\n.*---\n
    pattern = re.compile(r'---.*?---\s*(.*)', re.DOTALL)

    # Search for the body in the content
    match = pattern.search(content)
    if match:
        body = match.group(1).strip()
    else:
        print(f"No body found in file: {file_path}")
        body = ""


    # file_ref_pattern = re.compile(r'!\[\[.+\]\]')
    # body = file_ref_pattern.findall(content)

    return Reading(file_name, tags, last_practice_date, body, file_path)

    
class Reading:
    def __init__(self, name: str, tags: list[str], last_practice_date: date, body: str, file_path: str):
        self.name = name
        self.tags = tags
        self.last_practice_date = last_practice_date
        self.body = body
        self.file_path = file_path

    def __repr__(self):
        return f"Reading(name = {self.name}, tags={self.tags}, last_practice_date={self.last_practice_date}, body={self.body})"