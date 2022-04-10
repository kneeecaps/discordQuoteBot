#commandFunctions.py

from sqlFunctions import create_db_connection, execute_query

from dataclasses import dataclass

@dataclass
class quote:
    quote: str
    author: str

quotes = []
def load_quotes():
    with open('quotes.data', 'r') as f:
        for line in f:
            quoteStart = find_nth(line, '"', 1) + 1
            quoteEnd = find_nth(line, '"', 2)
            authorStart = find_nth(line, '"', 3) + 1
            authorEnd = find_nth(line, '"', 4)

            quotes.append(quote(line[quoteStart:quoteEnd], line[authorStart:authorEnd]))

def restore_quotes():
    load_quotes()
    serverID = 906306805842456596 #change this number to the id of the server you want to restore quotes to
    sql_command = f'''CREATE TABLE {'sID' + str(serverID)} (
        id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
        quote varchar(255) NOT NULL,
        author varchar(255) NOT NULL
    );
    '''
    execute_query(connection, sql_command, 0)
    for i in quotes:
        add_quote(i, serverID)

connection = create_db_connection('localhost', 'root', 'root', 'quotes')

def filter_content(content):
    content = content.replace('“', '"')
    content = content.replace('”', '"')
    content = content.replace('‘', '"')
    content = content.replace('’', '"')

    return content

def add_table(serverID):
    sql_command = f'''CREATE TABLE {serverID} (
        id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
        quote varchar(255) NOT NULL,
        author varchar(255) NOT NULL
        );
    '''
    execute_query(connection, sql_command, 0)

def add_quote(quote, serverID):
    db = 'sID' + str(serverID)
    sql_command = f'''INSERT INTO {db}
        (quote, author)
        VALUES ("{quote.quote}", "{quote.author}");
    '''
    if execute_query(connection, sql_command, 0) == 0:
        add_table(db)
        add_quote(quote, serverID)
        return
    print(f'Quote added: "{quote.quote}", {quote.author}')

def search_quotes(search, serverID):
    db = 'sID' + str(serverID)
    sql_command = f'''SELECT * FROM {db}
    WHERE INSTR(quote, "{search}") > 0
    OR INSTR(author, "{search}") > 0;
    '''

    result = execute_query(connection, sql_command, 1)
    if result == 0:
        return 0
    result = list(result)

    return result

def get_quote(id, serverID):
    db = "sID" + str(serverID)
    sql_command = f'''SELECT quote, author FROM {db}
        WHERE id = {id};
    '''

    foundQuote = execute_query(connection, sql_command, 2)

    editedQuote = quote(foundQuote[0], foundQuote[1])

    return editedQuote

def count_quotes(serverID):
    db = "sID" + str(serverID)
    sql_command = f'''SELECT COUNT(*) FROM {db};'''

    count = execute_query(connection, sql_command, 2)
    if count == 0:
        return 0
    count = count[0]

    return count

def find_nth(string, substr, n):
    if n == 0:
        return
    elif n == 1:
        return string.find(substr)
    else:
        return string.find(substr, find_nth(string, substr, n - 1) + 1)
