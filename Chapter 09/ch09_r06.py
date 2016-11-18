"""Python Cookbook

Chapter 9, recipe 6.

Parse the HTML file and produce the JSON
and XML files.
"""
from bs4 import BeautifulSoup
from pathlib import Path

def null_int(text):
    if text:
        return int(text)


def clean_leg(text):
    leg_soup = BeautifulSoup(text, 'html.parser')
    return leg_soup.text


def get_html():
    source_path = Path("Volvo Ocean Race.html")
    with source_path.open(encoding='utf8') as source_file:
        soup = BeautifulSoup(source_file, 'html.parser')

    legs = []
    thead = soup.table.thead.tr
    for tag in thead.find_all('th'):
        if 'data-title' in tag.attrs:
            leg_description_text = clean_leg(tag.attrs['data-title'])
            legs.append(leg_description_text)
        else:
            print(tag.attrs, tag.string)

    teams = []
    tbody = soup.table.tbody
    for row in tbody.find_all('tr'):
        team = {'name': None, 'position': []}
        for col in row.find_all('td'):
            if 'ranking-team' in col.attrs.get('class'):
                team['name'] = col.string
            elif 'ranking-number' in col.attrs.get('class'):
                team['position'].append(null_int(col.string))
            else:
                print(col.attrs, col.string)
        # Totals may be included.
        team['position'] = team['position'][:len(legs)]
        teams.append(team)

    document = {
        'legs': legs,
        'teams': teams,
    }
    return document

def show_json(document):
    import json
    print(json.dumps(document, indent=2))

def show_xml(document):
    from xml.etree import ElementTree as XML

    xml_document = XML.Element("results")
    legs_xml = XML.SubElement(xml_document, 'legs')
    for n, leg in enumerate(document['legs'], start=1):
        leg_xml = XML.SubElement(legs_xml, 'leg', n=str(n))
        leg_xml.text = leg

    teams_xml = XML.SubElement(xml_document, 'teams')
    for team in document['teams']:
        team_xml = XML.SubElement(teams_xml, "team")
        name_xml = XML.SubElement(team_xml, "name")
        name_xml.text = team['name']
        position_xml = XML.SubElement(team_xml, "position")
        for n, position in enumerate(team['position'], start=1):
            leg_xml = XML.SubElement(position_xml, "leg", n=str(n))
            leg_xml.text = str(position)

    pi = XML.ProcessingInstruction("xml", 'version="1.0"')
    XML.dump(pi)
    XML.dump(xml_document)

if __name__ == "__main__":

    document = get_html()

    print("-"*20)

    show_json(document)

    print("-"*20)

    show_xml(document)
