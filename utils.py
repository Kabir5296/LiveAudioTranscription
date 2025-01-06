def post_process_bn(text: str) -> str:
    '''
    Post process Bengali transcripted string.
    
    Arguements:
    -----------
        text (str): String need to be post processed.
    
    Returns:
    --------
        Post processed Bengali string.
    '''
    if len(text) <= 1:
        text = ''
        
    text = text.replace('ট্রেনিং প্রেসিডেন্ট','')
    text = text.replace('ট্রেনিং প্রেসিডেন্ট','')
    text = text.replace('প্রেসিডেন্ট প্রেসিডেন্ট','')
    text = text.replace('প্রেসিডেন্ট প্রেসিডেন্ট প্রেসিডেন্ট','')
    text = text.replace('আসসালামু আলাইকুম','')
    # text = bnpunct.add_punctuation(text)
    return text