

def clear_spe_tokens(response:str=""):

    spe_tokens = r'[UNUSED_TOKEN_145]\n'
    response = response.replace(spe_tokens, '')

    return response