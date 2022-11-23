#!/usr/bin/env python3

import argparse
from datetime import datetime
from pathlib import PurePath

import pandas as pd
import yaml

from transformers.age import ParsedAge
from transformers.name import latinize_name
from transformers.string import latinize_sentence, clean_persian_string


def read_people_from_spreadsheet(spreadsheet):
    result = []
    df = pd.read_excel(spreadsheet)
    for i, row in df.iterrows():
        data = normalize_row(row)
        data["datasource"] = spreadsheet
        result.append(data)
    return result


def normalize_row(df_row):
    data = dict(
        type="victim", incident="bloody-november", ref_in_datasource=df_row["ID"]
    )
    data["name_fa"] = clean_persian_string(df_row["Full Name"])
    data["name_en"] = latinize_name(data["name_fa"])
    age = ParsedAge(df_row["Age"])
    data["age_fa"] = age.persian
    data["age"] = age.latin
    data["cause_of_death_fa"] = clean_persian_string(df_row["Cause"])
    data["cause_of_death_en"] = latinize_sentence(data["cause_of_death_fa"])
    data["location_of_death_fa"] = normalize_location(
        clean_persian_string(df_row["Location"])
    )
    data["date_of_death_fa"] = clean_persian_string(df_row["Date"])
    data["image_48px"] = df_row["Image (48px)"]
    data["image_350px"] = df_row["Image (350px)"]
    return data


def normalize_location(location):
    location = location.strip()
    location = location.replace("_", "")
    location = location.replace(" ،", "،")
    return location


def write_people_as_jekyll_data(people, directory):
    for person in people:
        path = data_file_path(directory, person["ref_in_datasource"])
        with open(path, "w") as f:
            yaml.safe_dump(person, f, encoding="utf-8", allow_unicode=True)


def write_posts(people, data_directory, date=None, layout="person"):
    project_path = PurePath(__file__).parent.parent.parent.parent.parent
    posts_dir = project_path / "_posts"
    layout_file = project_path / "_layouts" / f"{layout}.html"
    with open(layout_file, "r") as layout_f:
        layout_content = layout_f.read()
    if date is None:
        date = datetime.now().date().isoformat()
    for person in people:
        data_path = data_file_path(data_directory, person["ref_in_datasource"])
        post_dir = (
            posts_dir / f"{date}-aban-hackathon-{person['ref_in_datasource']}.html"
        )
        with open(post_dir, "w") as post_f:
            post_f.write("---\n")
            with open(data_path, "r") as data_f:
                post_f.write(data_f.read())
            # FIXME: it seems we cannot use person as a layout. here we still
            # use post as a layout and copy person HTML
            post_f.write("layout: post\n")
            post_f.write(f"title: {person['name_fa']} | {person['name_en']}\n")
            post_f.write("---\n")
            post_f.write(layout_content)


def data_file_path(directory, person_id):
    return PurePath(directory) / f"{person_id}.yaml"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This script process data from Aban Hackathon round 1 data"
    )
    parser.add_argument("spreadsheet_file", help="Spreedsheet file to read data from")
    parser.add_argument("data_dir", help="Directory to write generated data")
    parser.add_argument(
        "--create-posts",
        action="store_true",
        help="Set to create posts for each person",
    )
    parser.add_argument(
        "--post_date",
        type=str,
        help="If asked to create posts, use this date instead of now",
    )
    args = parser.parse_args()
    people = read_people_from_spreadsheet(args.spreadsheet_file)
    write_people_as_jekyll_data(people, args.data_dir)
    if args.create_posts:
        write_posts(people, args.data_dir, date=args.post_date)
