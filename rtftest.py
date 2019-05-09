# -*- coding: utf-8 -*-


def extract_text_from_rtf(element):
    """extract marked up text from rtf."""

    raw_rtf = element[1].text
    print('text = dedent("""')
    print(raw_rtf)
    print('""")')


if __name__ == "__main__":

    import xml.etree.ElementTree as ET
    tree = ET.parse('test-data/first-rtf-test.graffle/data.plist')
    root = tree.getroot()


    for element in root.findall(".//dict//key/.."):
        if element[0].text == "Text":
            extract_text_from_rtf(element)


"""
/*/dict/text


<dict>
                        <key>Text</key>
                        <string>{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
{\fonttbl\f0\fnil\fcharset0 HelveticaNeue;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\qc\partightenfactor0

\f0\fs32 \cf0 This is some 
\b styled
\b0  text}</string>

"""
