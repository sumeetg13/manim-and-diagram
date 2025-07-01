from graphviz import Digraph

def draw_user_table(filename="user_table"):
    graph = Digraph('ER Diagram', format='png')
    graph.attr(rankdir='LR')

    graph.node('User', '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
      <TR><TD COLSPAN="2"><B>User</B></TD></TR>
      <TR><TD>user_id</TD><TD>PK</TD></TR>
      <TR><TD>name</TD><TD></TD></TR>
      <TR><TD>email</TD><TD></TD></TR>
      <TR><TD>user_name</TD><TD></TD></TR>
      <TR><TD>password</TD><TD></TD></TR>
    </TABLE>
    >''')

    graph.render(filename, view=True)
# draw_user_table()

def create_table_node(graph, table_name, columns):
    table_html = f'''
    <<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
    <TR><TD COLSPAN="2"><B>{table_name}</B></TD></TR>
    '''
    for col, attr in columns:
        table_html += f'<TR><TD>{col}</TD><TD>{attr}</TD></TR>'
    table_html += '</TABLE>>'
    graph.node(table_name, table_html)

def draw_schema():
    g = Digraph('ER', format='png')
    g.attr(rankdir='LR')
    create_table_node(g, 'User', [
        ('user_id', 'PK'),
        ('name', ''),
        ('email', ''),
        ('user_name', ''),
        ('password', '')
    ])
    g.render('user_schema', view=True)

draw_schema()


