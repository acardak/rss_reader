# Simple RSS article reader application

Python2 and Python3 compatible simple RSS article reader application

## Features
- Parsing articles from RSS feeds or from a text file (in certain formats)
- Formatting fetched articles as groups of `title` & `body` for processing
- Converting (replacing) keywords from pre-defined keyword map
- Cutting (limiting) title and body in certain length
- Writes the output in a YAML format text file or as stdout

## Reqired packages
<pre>
pip install beautifulsoup4
pip install six
pip install validators
</pre>

## Sample usages:
Check `output` folder for the output samples
<pre>
# From web:
python3 rss_reader.py -i http://tech.uzabase.com/ -o output/articles_from_web.yml
python3 rss_reader.py -i http://tech.uzabase.com/ -c convert -o output/articles_from_web_converted.yml
python3 rss_reader.py -i http://tech.uzabase.com/ -c cut,convert -o output/articles_from_web_converted_cut.yml

# From file:
python3 rss_reader.py -i articles.txt -o output/articles_from_file.yml
python3 rss_reader.py -i articles.txt -c convert -o output/articles_from_file_converted.yml
python3 rss_reader.py -i articles.txt -c cut,convert -o output/articles_from_file_converted_cut.yml
</pre>
