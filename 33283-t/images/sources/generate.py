#!/usr/bin/python3

import os
import sys
import subprocess
import tempfile

OUT_DIR = '..'

with tempfile.TemporaryDirectory() as tempdir:
    for file in os.listdir('.'):
        name, ext = os.path.splitext(file)
        if ext != '.xp':
            continue
        print(file)
        pdf_file_path = os.path.join(tempdir, name + '.pdf')
        subprocess.run(
            ['elaps', '--preamble', 'config.tex', '-v', '--pdf', '--ps2eps', '-I.', '-o', pdf_file_path, file], 
            stdout=subprocess.DEVNULL, 
            stderr=sys.stderr)
        assert os.path.exists(pdf_file_path)

        temp_svg_file_path = os.path.join(tempdir, name + '.svg')
        subprocess.run(
            ['pdf2svg', pdf_file_path, temp_svg_file_path],
            stdout=subprocess.DEVNULL,
            stderr=sys.stderr)
        assert os.path.exists(temp_svg_file_path)
        
        result_svg_file_path = os.path.join(OUT_DIR, name + '.svg')
        subprocess.run(
            ['rsvg-convert', '--format=svg', '--zoom=2', temp_svg_file_path],
            stdout=open(result_svg_file_path, 'wt'),
            stderr=sys.stderr
        )
        assert os.path.exists(result_svg_file_path)