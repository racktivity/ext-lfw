__author__ = "incubaid"


def main(q, i, params, tags):

    l ={"action": [
        {"name": "Print", "description": "Print this page", "uri": "javascript:print();", "target": "", "icon": "ui-icon-print"},
        {"name": "Google", "description": "Go To Google", "uri": "http://www.google.com", "target": "_blank", "icon": "ui-icon-link"},        
    ]}

    params['result'] = l

def match(q, i, params, tags):
    return True
