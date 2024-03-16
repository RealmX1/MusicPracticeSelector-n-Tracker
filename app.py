import os
import json
import re
import warnings
import tkinter as tk
import pandas as pd
from tkinter import filedialog
from datetime import datetime, timedelta

from reading import *
from util import *

# check if config.json exist, if not create it
if not os.path.isfile('config.json'):
    with open('config.json', 'w') as f:
        json.dump({}, f)

# check if config.json has non-empty "VaultPath" field, if not create it
with open('config.json', 'r') as f:
    config = json.load(f)

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        print(f"Folder selected: {folder_selected}")
        # Update config.json with the selected folder path
        with open('config.json', 'w') as f:
            config['VaultPath'] = folder_selected
            json.dump(config, f)

def set_vault_path():
    root = tk.Tk()
    root.title("Folder Selector")

    select_button = tk.Button(root, text="Select Folder", command=select_folder)
    select_button.pack(pady=20)

    root.mainloop()

def get_vault_path(force = False):
    if not config.get('VaultPath') or force:
        config['VaultPath'] = ''
        set_vault_path()
        with open('config.json', 'w') as f:
            json.dump(config, f)
    
    return config['VaultPath']

def tag_format_check(vault_path):
    tag_folder_path = os.path.join(vault_path, 'Tags')

    # Check if "Tags" folder exists
    if not os.path.isdir(tag_folder_path):
        warnings.warn(f"'Tags' folder does not exist in the directory '{vault_path}'.")
        return

    # Check if "Tags" folder has files
    files = [f for f in os.listdir(tag_folder_path) if os.path.isfile(os.path.join(tag_folder_path, f))]
    if not files:
        warnings.warn(f"'Tags' folder in '{vault_path}' is empty.")
        return

    # Check file format
    front_matter_pattern = re.compile(r'^---\ntags:\n(  - .+\n)+---', re.MULTILINE)
    for file in files:
        file_path = os.path.join(tag_folder_path, file)
        with open(file_path, 'r') as f:
            content = f.read()
            if not front_matter_pattern.match(content):
                warnings.warn(f"File '{file}' in 'Tags' folder does not follow the specified format.")

cached_searched_df = None
vault_path = ""


def update_last_practice_date(md_file_path):
    # Read the current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Read the content of the Markdown file
    with open(md_file_path, 'r') as file:
        content = file.read()

    # Define a regular expression pattern to find the "Last Practice Date" line
    date_pattern = re.compile(r'Last Practice Date:.*')

    # Replace the existing date with the current date
    new_content = date_pattern.sub(f'Last Practice Date: {current_date}', content)

    # Write the updated content back to the file
    with open(md_file_path, 'w') as file:
        file.write(new_content)

def export_to_pdf(date_str, selected_tags, df):
    global cached_searched_df
    if not date_str:
        # default to 10 days ago
        date_str = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
    date = datetime.strptime(date_str, '%Y-%m-%d')
    if cached_searched_df is None or cached_searched_df.empty:
        warnings.warn("No search results to export.")
        return
    
    # filter out all readings that are not practiced after the date
    filtered_df = cached_searched_df[cached_searched_df['last_practice_date'] < date]

    print(filtered_df)


    # Example usage
    global vault_path
    # output path is output.pdf under current directory
    current_time_str = datetime.now().strftime('%Y-%m-%d')
    
    # create a string of all selected tags (value is true) connected by "_"
    print('\nselected_tags', selected_tags, '\n')
    selected_tags_str = '_'.join([tag for tag, value in selected_tags.items() if value.get()])
    output_pdf_path_template = 'output_{selected_tags_str}_{current_time_str}{tail}.pdf'.format(selected_tags_str=selected_tags_str, current_time_str=current_time_str, tail = "{}")
    output_pdf_path = output_pdf_path_template.format("")
    i = 1
    while os.path.exists(output_pdf_path):
        output_pdf_path = output_pdf_path_template.format("_" + str(i))
        i += 1

    md_strings = []
    for index, row in filtered_df.iterrows():
        md_string = f"Name: {row['name']}\nTags: {row['tags']}\nLast Practice Date: {row['last_practice_date'].strftime('%Y-%m-%d')}\n\n{row['body']}"
        md_strings.append(md_string)
        
    convert_markdown_to_pdf(md_strings, vault_path, output_pdf_path)

    for index, row in filtered_df.iterrows():
        path = row['path']
        update_last_practice_date(path)

        df.loc[index, 'last_practice_date'] = current_time_str
    



# GUI Creation
def create_gui(tags, df):
    tag_to_type = {tag: tag_type for tag_type, tag_list in tags.items() for tag in tag_list}

    root = tk.Tk()
    root.title("Tag Selector")
    root.geometry("1500x700")

    # Configure row and column weights
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Result display frame
    result_frame = tk.Frame(root)
    result_frame.grid(row=0, column=1, padx=20, pady=20)

    result_label = tk.Label(result_frame, text="Search Results", font=("Helvetica", 16),padx=40, pady=40)
    result_label.pack()
    
    result_listbox = tk.Listbox(result_frame, height=80, width=80)
    result_listbox.pack()


    selected_tags = {tag: tk.BooleanVar() for tag_type in tags.values() for tag in tag_type}

    # date selection frame
    date_frame = tk.Frame(root)
    date_frame.grid(row=1, column=1, padx=20, pady=10)

    date_label = tk.Label(date_frame, text="Enter Export Til Last Practice Date (YYYY-MM-DD):")
    date_label.pack(side=tk.LEFT, padx=5, pady=5)

    date_entry = tk.Entry(date_frame)
    date_entry.pack(side=tk.LEFT, padx=5, pady=5)

    # Tag selection frame
    tag_frame = tk.Frame(root)
    tag_frame.grid(row=0, column=0, padx=10, pady=10)

    for tag_type, tag_list in tags.items():
        frame = tk.Frame(tag_frame)
        frame.pack(side=tk.LEFT, padx=10, pady=10)

        label = tk.Label(frame, text=tag_type)
        label.pack()

        tag_list.sort()
        for tag in tag_list:
            checkbutton = tk.Checkbutton(frame, text=tag, variable=selected_tags[tag])
            checkbutton.pack()

    

    # Search button
    search_button = tk.Button(root, text="Search", command=lambda: search_and_display(df, selected_tags, result_listbox, tag_to_type))
    search_button.grid(row=0, column=2, padx=10, pady=10)

    # export button
    export_button = tk.Button(root, text="Export", command=lambda: export_to_pdf(date_entry.get(), selected_tags, df))
    export_button.grid(row=1, column=2, padx=10, pady=10)

    root.mainloop()

def filter_dataframe(df, selected, tag_to_type):
    grouped_selected = {}
    for selected_tag in selected:
        tag_type = tag_to_type[selected_tag]
        if not grouped_selected.get(tag_type):
            grouped_selected[tag_type] = []
        grouped_selected[tag_type] = grouped_selected[tag_type] + [selected_tag]
    combined_mask = pd.Series([True] * len(df))

    masks = []
    for tag_type, tag_list in grouped_selected.items():
        if tag_list:
            # Create a mask for each non-empty tag list
            type_mask = df[tag_list[0]]
            for tag in tag_list[1:]:
                type_mask |= df[tag]
            masks.append(type_mask)

    if masks:
        # Combine masks using logical "AND"
        combined_mask = masks[0]
        for mask in masks[1:]:
            combined_mask &= mask
        return df[combined_mask]
    else:
        return df

def search_and_display(df, selected_tags, result_listbox, tag_to_type):
    selected = {tag for tag, var in selected_tags.items() if var.get()}

    if not selected:
        result_listbox.delete(0, tk.END)
        result_listbox.insert(tk.END, "No tags selected.")
        return

    filtered_df = filter_dataframe(df, selected, tag_to_type)

    # Sort by last_practice_date in descending order
    sorted_df = filtered_df.sort_values(by= ['last_practice_date','name'], ascending=True)
    global cached_searched_df
    cached_searched_df = sorted_df

    # Display results
    result_listbox.delete(0, tk.END)
    for index, row in sorted_df.iterrows():
        true_tags = [tag for tag in selected if row[tag]]
        formatted_result = f"Date: {row['last_practice_date'].strftime('%Y-%m-%d')}, Tags: {true_tags}, Name: {row['name']}"
        result_listbox.insert(tk.END, formatted_result)


selected_tags = []

def main():
    global vault_path
    vault_path = get_vault_path()
    # check if user want to change vault path; if user input Y or yes, then change vault path
    while input(f"Vault path is set to '{vault_path}'.\nDo you want to change it? Reply yes/y to change, otherwise this path will be used: ").lower() in ['y', 'yes']:
        vault_path = get_vault_path(force=True)

    try:
        tag_format_check(vault_path)
    except UserWarning as e:
        print(e)

    # extract all tags from the tags folder
    tags = {}
    tag_folder_path = os.path.join(vault_path, 'Tags')
    tag_files = [f for f in os.listdir(tag_folder_path) if os.path.isfile(os.path.join(tag_folder_path, f))]
    for file in tag_files:
        file_path = os.path.join(tag_folder_path, file)        
        file_name = file.split('.')[0]
        tags[file_name] = extract_tags(file_path)
    
    # print(f"Tag files: {tag_files}")
    # for tag_type, tag in tags.items():
    #     print(tag_type, tag)
        

    # recursively process all file in folder "Readings" of the vault (and maybe subfolder of reading); ones that ends with .md
    readings_folder_path = os.path.join(vault_path, 'Readings')
    md_file_paths = []
    for dirpath, dirnames, filenames in os.walk(readings_folder_path):
        for filename in filenames:
            if filename.endswith('.md'):
                file_path = os.path.join(dirpath, filename)
                md_file_paths.append(file_path)
    
    readings = []
    for file_path in md_file_paths:
        # print(file_path)
        reading = process_md_file(file_path)
        readings.append(reading)
    # print(readings)

    # convert readings to pandas dataframe with one-hot columns for all potential tags
    tmp = list(tags.values())
    tags_lst = [item for sublist in tmp for item in sublist]
    
    df = pd.DataFrame(columns=["name", "last_practice_date","tags"] + tags_lst + ["body"])
    print("\n\n", df, "\n\n")
    for idx, reading in enumerate(readings):
        row_data = {
            "name": reading.name,
            "last_practice_date": reading.last_practice_date,
            "tags": reading.tags,
            "body": reading.body,
            "path": reading.file_path
        }
        if row_data['last_practice_date'] is None:
            row_data['last_practice_date'] = datetime.strptime('2000-01-01', '%Y-%m-%d')
        for tag in tags_lst:
            row_data[tag] = tag in reading.tags
        df = df._append(pd.Series(row_data, name=idx))
    df["last_practice_date"].fillna(pd.Timestamp('2000-01-01'), inplace=True)

    # fill last_practice_date where it is NaT with 2000-01-01

    # turn the readings list into a pandas dataframe, with one-hot columns for all potential tags
    # each row is a reading
    # readings_df = pd.
    
    create_gui(tags,df)

if __name__ == '__main__':

    main()