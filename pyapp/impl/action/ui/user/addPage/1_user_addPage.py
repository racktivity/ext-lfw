

def main(q, i, p, params, tags):

    user = p.api.model.ui.user.get(params['userguid'])
    user.pages.append(params['page'])
    params['result'] = True
    
def match(q, i, p, params, tags):
	return True
