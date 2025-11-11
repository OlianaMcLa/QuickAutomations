from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

# --- Core Content Blocks ---

@dataclass
class Text:
    """Represents the lowest level text content."""
    text: str
    type: str = "text"
    # Optional marks like 'strong' or 'em' could go here, but omitted for simplicity

@dataclass
class Paragraph:
    """Represents a paragraph, which holds text/inline content."""
    content: List[Text]
    type: str = "paragraph"

# --- Table Components ---

@dataclass
class TableCell:
    """Represents a single data cell (tableCell or tableHeader)."""
    content: List[Paragraph]
    type: str = field(default="tableCell") # Can be overridden to 'tableHeader'

@dataclass
class TableRow:
    """Represents a row in the table."""
    content: List[TableCell]
    type: str = "tableRow"

@dataclass
class TableAttrs:
    """Attributes for the main table block."""
    isNumberColumnEnabled: bool = False
    layout: str = "default"

@dataclass
class Table:
    """Represents the table element."""
    content: List[TableRow]
    attrs: TableAttrs = field(default_factory=TableAttrs)
    type: str = "table"

# --- Main Document Structure ---

@dataclass
class Doc:
    """Represents the root of the Atlassian Document Format (ADF)."""
    content: List[Any]  # Can hold Table, Paragraph, etc.
    version: int = 1
    type: str = "doc"
    
def create_adf_table(data= [], headers = []) -> Doc:
    """Creates an ADF table from given data and headers."""
    table_rows = []

    # Create header row if headers are provided
    if headers:
        header_cells = [TableCell(content=[Paragraph(content=[Text(text=header)])], type="tableHeader") for header in headers]
        table_rows.append(TableRow(content=header_cells))

    # Create data rows
    for row in data:
        data_cells = [TableCell(content=[Paragraph(content=[Text(text=str(cell))])]) for cell in row]
        table_rows.append(TableRow(content=data_cells))

    # Create the table
    table = Table(content=[table_rows])

    # Create the document
    doc = Doc(content=[table])
    
    return doc

def headers_and_cells_to_v2_string(header=[], cells=[]) -> str:
    mainString = ""
    for head in header:
        mainString += "||"+head
    mainString += "||"
    for cellRow in cells:
        mainString += "\n|"
        for cell in cellRow:
            mainString += str(cell)+"|"
    return mainString
    