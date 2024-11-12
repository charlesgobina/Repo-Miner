"""
This module filters the files from scc to remove non-programming languages
"""

import json

# Recognized programming languages
RECOGNIZED_LANGUAGES = {
    "Visual FoxPro", "1C", "4th Dimension", "ABAP", "ABC", "ActionScript", "Ada", 
    "Agilent VEE", "Algol", "Alice", "Angelscript", "Apex", "APL", "Applescript",
    "Arc", "AspectJ", "Assembly language", "ATLAS", "AutoHotkey", "AutoIt", "AutoLISP",
    "Awk", "Bash", "Basic", "bc", "BCPL", "BETA", "Bourne shell", "Brainfuck", "C shell",
    "C#", "C++", "C", "Caml", "Carbon", "Ceylon", "CFML", "Chapel", "CHILL", "CIL", 
    "Clojure", "COBOL", "CoffeeScript", "Crystal", "Curl", "D", "Dart", "Delphi/Object Pascal",
    "DiBOL", "Dylan", "E", "ECMAScript", "Eiffel", "Elixir", "Elm", "Emacs Lisp", "Erlang", 
    "F#", "Factor", "Falcon", "Fantom", "Forth", "Fortran", "FreeBASIC", "GAMS", "GLSL", 
    "Go", "Groovy", "Hack", "Harbour", "Haskell", "Haxe", "Heron", "Icon", "IDL", "Idris",
    "Io", "J", "JADE", "Java", "JavaScript", "Julia", "Korn shell", "Kotlin", "LabVIEW",
    "Ladder Logic", "Lasso", "Lingo", "Lisp", "Logo", "LotusScript", "Lua", "MAD", "Magic",
    "Magik", "MANTIS", "Maple", "MATLAB", "Max/MSP", "MAXScript", "MEL", "Mercury", "ML",
    "Modula-2", "Modula-3", "Monkey", "MQL5", "MS-DOS batch", "MUMPS", "NATURAL", "Nim",
    "NQC", "Objective-C", "OCaml", "OpenCL", "OpenEdge ABL", "OPL", "Oz", "Pascal", "Perl",
    "PHP", "Pike", "PostScript", "PowerBasic", "PowerShell", "Processing", "Prolog", "PureBasic",
    "Python", "R", "Racket", "REBOL", "Red", "REXX", "Ring", "RPG", "Ruby", "Rust", "SAS",
    "Scala", "Scheme", "sed", "Seed7", "Simula", "Simulink", "Smalltalk", "Smarty", "Solidity",
    "SPARK", "SPSS", "SQL", "SQR", "Squirrel", "Standard ML", "Stata", "Swift", "SystemVerilog",
    "Tcl", "Transact-SQL", "TypeScript", "Uniface", "Vala/Genie", "VBScript", "VHDL",
    "Visual Basic", "WebAssembly", "Wolfram", "X++", "X10", "XBase", "XBase++", "XC", "Xen", "Xojo",
    "XQuery", "XSLT", "Xtend", "Z shell", "Zig"
}

# Load SCC JSON data
scc_files = [

    'c:/Users/houci/OneDrive/Bureau/New folder (2)/Untitled-1.json'

]

filtered_data = []

for file_path in scc_files:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

        # Filter out non-programming languages
        for entry in data:
            language = entry.get("Name")
            if language in RECOGNIZED_LANGUAGES:
                filtered_data.append(entry)

# Save the filtered data to a new JSON file
OUTPUT_FILE = "c:/Users/houci/OneDrive/Bureau/New folder (2)/filtered_scc_output.json"
with open(OUTPUT_FILE, 'w', encoding='utf8') as file:
    json.dump(filtered_data, file, indent=4)

print(f"Filtered data saved to {OUTPUT_FILE}")
