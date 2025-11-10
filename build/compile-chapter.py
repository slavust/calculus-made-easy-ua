#!/usr/bin/python3

import os.path
import subprocess
import sys

def postprocess_chapter(html_path):
    with open(html_path, 'r') as html:
        full_code = html.read()
    
    full_code = full_code.replace('<strong>!screen-dependent-scale-begin!</strong>', '<div class="scaled">')
    full_code = full_code.replace('<strong>!screen-dependent-scale-end!</strong>', '</div>')

    full_code = full_code.replace('<strong>!small-screen-begin!</strong>', '<div class="mobile">')
    full_code = full_code.replace('<strong>!small-screen-end!</strong>', '</div>')

    full_code = full_code.replace('<strong>!big-screen-begin!</strong>', '<div class="desktop">')
    full_code = full_code.replace('<strong>!big-screen-end!</strong>', '</div>')

    with open(html_path, 'w') as html:
        html.write(full_code)
    
def compile_chapter(input_dir, html_template_path, css_path, output_dir, chapter_number, chapter_name, next_chapter_name = None):
    html_path = os.path.join(output_dir, chapter_name + '.html')
    next_chapter_var = 'next-chapter-url=' + next_chapter_name + '.html' if next_chapter_name else 'dummy=0'
    script_path = os.path.realpath(__file__)
    script_dir = os.path.join(*os.path.split(script_path)[:-1])
    subprocess.call([
        'pandoc',
        '-f',
        'markdown+tex_math_dollars',
        '-t', 
        'html+tex_math_dollars',
        '--lua-filter',
        os.path.join(script_dir, 'md-link-to-html.lua'),
        '--mathjax', 
        '--standalone', 
        '--template='+html_template_path,
        '--css='+css_path,
        '--wrap=none',
        '-V',
        next_chapter_var,
        '-V',
        'chapter-number=' + str(chapter_number),
        '-o',
        html_path,
        os.path.join(input_dir, chapter_name + '.md')
        ])
    postprocess_chapter(html_path)


if __name__ == '__main__':
    input_dir = sys.argv[1]
    html_dir = sys.argv[2]
    chapter_number = sys.argv[3]
    chapter_name = sys.argv[4]
    next_chapter_name = sys.argv[5]
    if next_chapter_name == 'none':
        next_chapter_name = None
    html_template_path = os.path.join(input_dir, 'html-templates', 'chapter.template')
    css = 'screen.css'
    compile_chapter(
        input_dir, 
        html_template_path,
        css,
        html_dir,
        chapter_number,
        chapter_name,
        next_chapter_name)