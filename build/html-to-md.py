#!/usr/bin/python3
from bs4 import BeautifulSoup
import sys
import os
import subprocess

def prepare_html(path, out_path):
    with open(path, 'r') as html_file:
        soup = BeautifulSoup(html_file.read(), 'html.parser')

        smallscreen_paragraphs = soup.find_all('p', 'mobile')
        bigscreen_paragraphs = soup.find_all('p', 'desktop')

        assert(len(smallscreen_paragraphs) == len(bigscreen_paragraphs))

        for s, b in zip(smallscreen_paragraphs, bigscreen_paragraphs):
            if s.string != b.string:
                new_tag_small = BeautifulSoup('<p><b>!small-screen-begin!</b>\n' + s.string + '\n<b>!small-screen-begin!</b></p>', 'html.parser')
                s.replace_with(new_tag_small)
                new_tag_big = BeautifulSoup('<p><b>!big-screen-begin!</b>\n' + b.string + '\n<b>!big-screen-end!</b></p>', 'html.parser')
                b.replace_with(new_tag_big)
            else:
                s.extract()
                new_tag = BeautifulSoup('<p><b>!screen-dependent-scale-begin!</b>\n' + b.string + '\n<b>!screen-dependent-scale-end!</b></p>', 'html.parser')
                b.replace_with(new_tag)
        
        with open(out_path, 'w', encoding='utf-8') as out_html:
            out_html.write(str(soup))

def convert_to_markdown(html_path, out_md_path, out_image_dir):
    script_path = os.path.realpath(__file__)
    script_dir = os.path.join(*os.path.split(script_path)[:-1])
    subprocess.call([
        'pandoc',
        '--lua-filter',
        os.path.join(script_dir, 'html-link-to-md.lua'),
        '-f',
        'html+tex_math_single_backslash+tex_math_double_backslash+tex_math_dollars',
        '-t',
        'markdown',
        '--extract-media={}'.format(out_image_dir),
        '-o',
        out_md_path,
        html_path])

def correct_image_links_in_md(md_path):
    with open(md_path, 'r') as file:
        md = file.read()
    

if __name__ == '__main__':
    input_html_path, output_md_path, output_img_dir = sys.argv[1:]
    temp_html = list(os.path.split(input_html_path))
    temp_html[-1] = '_temporary_' + temp_html[-1]
    temp_html = os.path.join(*temp_html)
    prepare_html(input_html_path, temp_html)
    convert_to_markdown(temp_html, output_md_path, output_img_dir)