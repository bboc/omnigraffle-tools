# ogtrans - Translate OmniGraffle files

Right now that is relevant for Hebrew, Dutch and Russian translations of the S3 illustrations, however I doubt that I can get the posters translated in time. So focus on the simple use case.

# Reading an Omnigraffle Document

After some experiments with XML libraries it's clear that Python's [plistlib](https://docs.python.org/3/library/plistlib.html) is the way to go. Traverse the plist and identify all strings that start with "{\rtf1}". 

Strings are located in the following elements in subelements Text/Text (String):

- class LineGraphic
- class ShapedGraphic

And not in: 

- class Group
- class GraffleShapes.CanvasBackgroundGraphic
- class TableGroup

Here's all of the full paths I have found so far:

- document{MasterSheets}[0]{GraphicsList}[0]{Text}{Text}
- document{Sheets}[12]{GraphicsList}[6]{Graphics}[1]{Graphics}[0]{Text}{Text}
- document{Sheets}[9]{GraphicsList}[5]{Graphics}[1]{Text}{Text}
- document{Sheets}[9]{GraphicsList}[6]{Text}{Text}


# Working with RTF

An rtf document has a header with several blocks, and then the text starts, typically with a few control words setting fonts and colors. In all examples I looked at, the test started after the foreground color `\cf0`

    {\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
    {\fonttbl\f0\fnil\fcharset0 OpenSans;}
    {\colortbl;\red255\green255\blue255;}
    {\*\expandedcolortbl;;}
    \deftab720
    \pard\pardeftab720\partightenfactor0
         
    \f0\fs14\fsmilli7446 \cf0 here starts the text }


The `\fonttbl` control word introduces the font table group. Unique `\fN` control words define each font available in the document, and are used to reference that font throughout the document. 

The following example defines a block of text in color (where supported). Note that the cf/cb index is the index of an entry in the color table, which represents a red/green/blue color combination.

    {\f1\cb1\cf2 This is colored text. The background is color
    
    1 and the foreground is color 2.}


## Some real-life examples

### Example 1: Text with special characters in another font

	{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
	{\fonttbl\f0\fnil\fcharset0 OpenSans-Light;\f1\fnil\fcharset77 ZapfDingbatsITC;}
	{\colortbl;\red255\green255\blue255;\red64\green64\blue64;}
	{\*\expandedcolortbl;;\csgray\c31800;}
	\deftab720
	\pard\pardeftab720\sl280\sa80\partightenfactor0
	
	\f0\fs18 \cf2 Dom\'e4nen werden an Gruppen (z.B. an Abteilungen / Teams) oder Einzelpersonen (
	\f1 \cf2 \uc0\u10148 
	\f0 \cf2 Rolle) delegiert, die - innerhalb der Grenzen des Einfluss- und Autonomiebereiches der Dom\'e4ne -  Verantwortung f\'fcr diese Dom\'e4ne \'fcbernehmen.\
	Die Delegierende einer Dom\'e4ne tr\'e4gt weiterhin Verantwortung  f\'fcr diese Dom\'e4ne. }

### Example 2: List  and bold text using Open Sans Regular

`\f0` is OpenSans (bold text), `\f1` is the list marker `\uc0\u9642`, and `\f2` is regular text (OpenSans light)

	{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
	{\fonttbl\f0\fnil\fcharset0 OpenSans;\f1\fnil\fcharset0 LucidaGrande;\f2\fnil\fcharset0 OpenSans-Light;
	}
	{\colortbl;\red255\green255\blue255;\red64\green64\blue64;}
	{\*\expandedcolortbl;;\csgray\c31800;}
	{\*\listtable{\list\listtemplateid1\listhybrid{\listlevel\levelnfc23\levelnfcn23\leveljc0\leveljcn0\levelfollow0\levelstartat1\levelspace360\levelindent0{\*\levelmarker \{square\}}{\leveltext\leveltemplateid1\'01\uc0\u9642 ;}{\levelnumbers;}\fi-360\li720\lin720 }{\listname ;}\listid1}}
	{\*\listoverridetable{\listoverride\listid1\listoverridecount0\ls1}}
	\pard\tx26\tx280\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\li286\fi-286\sa60\pardirnatural\partightenfactor0
	\ls1\ilvl0
	\f0\fs18 \cf2 {\listtext	
	\f1 \uc0\u9642 
	\f0 	}wichtige Anforderungen
	\f2  an delegierte Aufgaben und Entscheidungen
	\f0  \
	{\listtext	
	\f1 \uc0\u9642 
	\f0 	}Grenzen
	\f2  von Autonomie und Einfluss (z.B. Budget, Ressourcen, Reports)}

## A simple RTF parser 

From the examples I looked at, it's pretty simple to parse the RTF: 

- simply ignore most headers by looking at the first few characters, if it starts with `\f…` it's probably the start of the text, so extract everything until the last `}` as the text
- parse the header starting with `{\fonttbl` to find: 
	- lists: ListMarker has font LucidaGrande
	- special symbols: have ZapfDingbats
	- optional (when using OpenSans: bold and regular fonts)
- extract the control words at the beginning of the text to see if the font starts with bold or normal 
- extract the text and use regex to convert to Markdown
- when inserting, insert the new text after the control words, and use the font table to set the correct fonts. Colors should not matter, as the illustrations use just one color for each text
- the conversion should use minimal whitespace, spaces instead of tabs, but preserve line breaks

# How to store and retrieve translations

Notes: Crowdin treats each multiline string in a POT file as one single string, i.e. all small changes require a full re-translation. Also there's no support for Markdown content on POT-files, so that translators have to take care to write correct Markdown. For HTML tags there's at least a way to copy them from source to translation. So it's essential to only have simple formatting in the po-files (bold, italics), and put longer texts into am Markdown file

## Example Text

    This is a paragraph of text, with some **bold** and some _italic_ text. Also there's a list with two elements:

    - one list item
    - another list item

    After the list, there's another sentence for good measure, complete with a **bold part**.```

## Approach 1: Translation Memory

-   Create a Markdown-based translation memory from the PO file (source --> translation)
-   go through the document and convert each text to Markdown
-   go through that text and translate each sentence/list item through the translation memory
-   convert the resulting Markdown document to RTF and inject back into the document 

**Benefits:**

-   simple to implement
-   I can touch up the English translations and simply re-translate with the existing translation memory as long as I don't change the text

**Challenges:**

-   one string can only have one translation in one file
-   structure of complex texts might be hard to track in Crowdin, as list items and individual sentences might be ripped apart

## Approach 2: IDs

-   on extraction: when extracting text as Markdown, make a copy of the Omnigraffle document and inject autogenerated IDs into each the content part of each text element that a re stored with the extracted content
-   on translation: convert Markdown to rtf, and insert in place of ID in the copy 

**Benefits:**

-   one string can have several in one file
-   structure of complex texts is simpler to track down

**Challenges:**

- every change to the source requires a round trip through the translation platform (but maybe that can be fully automated so that it just takes time, but no interaction)

## Approach 3: Translation memory and Markdown files

A simple translation memory based on po-files is used to translate most texts, longer texts are dumped in separate Markdown files (`<document-name>\<canvas-name>\<file-name>.md`). Filename is stored in user data, so the author of the document can decide which strings will be stored in dedicated files.

**Benefits**: 

- larger texts can be translated in context, and Crowdin translation memory can still be used as each sentence will become a separate string.
- short strings can still be translated via translation memory
- no IDs necessary, because larger texts are simply identified by the filename stored in user data

**Challenges**:

- none identified so far


# Resources

**PO-Files:** http://pology.nedohodnik.net/doc/user/en_US/ch-poformat.html

## RTF Resources, Converters and Libraries

- [RTF 1.5 spec](http://www.biblioscape.com/rtf15_spec.htm#Heading9)
- [wikipedia entry](https://en.wikipedia.org/wiki/Rich_Text_Format)
- [writing your own RTF converter](https://www.codeproject.com/Articles/27431/Writing-Your-Own-RTF-Converter)
- [RTF Pocket Guide](https://www.oreilly.com/library/view/rtf-pocket-guide/9781449302047/ch01.html)

### Python Libraries

- [writing unicode to rtf](https://www.zopatista.com/python/2012/06/06/rtf-and-unicode/)
- Python [striprtf](https://gist.github.com/gilsondev/7c1d2d753ddb522e7bc22511cfb08676)
- PyRTF (examples: https://github.com/grangier/pyrtf/blob/master/examples/examples.py) (Python 2 or 3)
- [pyth](https://en.wikipedia.org/wiki/Rich_Text_Format) (Python 2.7)

## Converters 

- convert via [textutil](https://ss64.com/osx/textutil.html)
- [textract - extract text from rtf](https://textract.readthedocs.io/en/stable/)
- [unrtf - extract text from rtf](https://www.gnu.org/software/unrtf/)
- [rtf2xml](http://rtf2xml.sourceforge.net/docs/man-page.html)

# Discussion of architecture

## Strategy 1:

**NOTE: this appears to work good enough for now, ignore the second strategy for now.**
Parse save OmnigraffleDocuments which are XML (plist file) uncompressed, either as flat file or as package,  and then extract rich text to markdown (and back). To allow for a simple parser, the amount of Markup possible needs to be limited!

####Supported Markup:

1.   one text element contains only one font, and only standard formatting (bold, italics, links)
2.   Support bullet pints (but no nested bullent points)
3.   Extend that to support using light and regular fonts as normal and bold (looks better with Open Sans)

**Benefits:**

-   works with Python, so development is pretty fast 
-   no bugs need to be solved in OmniGraffle

**Challenges:**

-   parsing RTF might turn out to become interesting (seems ok though)
-   how to find out which text goes where? (maybe copy file and replace text with ID??, set those in user data or something)

**Estimate:** After proof of principle, it looks like it might take 2-3 days to get this working.

## Strategy 2: @later

**Looks like strategy 1 is good enough already.**
Write an OmniGraffle Plugin that extracts the text without any formatting. That would work with 90% of the illustrations (but not with posters and primer)

**Benefits**:

- simple

**Challenges:**

-   not all illustrations can be translated that way
-   scripting an omni graffle plugin from outside through script links is not very elegant
-   might require some retouching of the illustrations

**Estimate:** Who knows? Not important right now

## plist Structure

Plist as XML is such a massively bad idea. Why create something that looks like XML, but cannot make use of all the tools XML provides navigate complexity: XPATH and XSLT. And why on earth is RTF in an XML document, when HTML is a much more logical and equally powerful choice?

	<dict>
		…	
		<key>Class</key>
		<string>ShapedGraphic</string>
		<key>ID</key>
		<integer>7</integer>
		<key>Name</key>
		<string>foo</string>
		…
		<key>Text</key>
		<dict>
			<key>Text</key>
			<string>{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
				…
				}</string>
			<key>TextAlongPathGlyphAnchor</key>
			<string>center</string>
		</dict>
		<key>UserInfo</key>
		<dict>
			<key>filename</key>
			<string>textbox-a</string>
		</dict>
	</dict>
	
