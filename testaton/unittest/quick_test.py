from pretty_reports import generate_html_report
from test_sql import TestScript, TestResult
import markdown

def mark(report_title, airline_code, text):
    html_header = '''
    <html>
        <head>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
            <style>body{ margin:0 100; background:whitesmoke; }</style>
        </head>
        <body>'''

    html_title = '<h1>' + report_title + ' ' + airline_code + ' ' + '</h1>'

    html_body = markdown.markdown(text)

    html_footer = '</body></html>'

    return html_header + html_title + html_body + html_footer


v1 = 23231
v2 = 22

md =  """
* Item """ + str(v1) + """
* Item """ + str(v2) + """
"""

r = mark("Test", "XX", md)


f = open('test_file.html', 'w')
f.write(r)
f.close()
