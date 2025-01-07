from random import randint

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
    text = text.replace('ভারতীয় বিদ্যমান', '')
    text = text.replace('ভারতীয় বিদ্যমানের জন্য', '')
    text = text.replace('জেলার প্রধান বিভাগের', '')
    # text = bnpunct.add_punctuation(text)
    return text

def random_n(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)