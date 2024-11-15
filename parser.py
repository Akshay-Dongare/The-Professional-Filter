## Script to parse the emails in the dataset
import pandas as pd

def get_message(Series: pd.Series):
    result = pd.Series(index=Series.index)
    for row, message in enumerate(Series):
        message_words = message.split('\n')
        del message_words[:15]
        result.iloc[row] = ''.join(message_words).strip()
    return result

def get_date(Series: pd.Series):
    result = pd.Series(index=Series.index)
    for row, message in enumerate(Series):
        message_words = message.split('\n')
        del message_words[0]
        del message_words[1:]
        result.iloc[row] = ''.join(message_words).strip()
        result.iloc[row] = result.iloc[row].replace('Date: ', '')
    print('Done parsing, converting to datetime format..')
    return pd.to_datetime(result)

def get_sender_and_receiver(Series: pd.Series):
    sender = pd.Series(index = Series.index)
    recipient1 = pd.Series(index = Series.index)
    recipient2 = pd.Series(index = Series.index)
    recipient3 = pd.Series(index = Series.index)
    
    for row,message in enumerate(Series):
        message_words = message.split('\n')
        sender[row] = message_words[2].replace('From: ', '')
        recipient1[row] = message_words[3].replace('To: ', '')
        recipient2[row] = message_words[10].replace('X-cc: ', '')
        recipient3[row] = message_words[11].replace('X-bcc: ', '')
        
    return sender, recipient1, recipient2, recipient3

def get_subject(Series: pd.Series):
    result = pd.Series(index = Series.index)
    
    for row, message in enumerate(Series):
        message_words = message.split('\n')
        message_words = message_words[4]
        result[row] = message_words.replace('Subject: ', '')
    return result

def get_folder(Series: pd.Series):
    result = pd.Series(index = Series.index)
    
    for row, message in enumerate(Series):
        message_words = message.split('\n')
        message_words = message_words[12]
        result[row] = message_words.replace('X-Folder: ', '')
    return result
