from docutils import nodes
from docutils.parsers.rst import directives
import os
import re
import codecs
import yaml
from collections import OrderedDict

import sphinx
from sphinx.ext.graphviz import render_dot_html, render_dot_latex, \
    render_dot_texinfo, figure_wrapper
from sphinx.pycode import ModuleAnalyzer
from sphinx.util import force_decode
from sphinx.util.compat import Directive

re_relation = re.compile('^\s*(.*)\s(\*|\+|\?|[0-9])?(->|<-|--|<->)(\*|\+|\?|[0-9])?\s(.*)$')

yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    lambda loader, node: OrderedDict(loader.construct_pairs(node)))

class er_diagram(nodes.General, nodes.Element):
    """
    A docutils node to use as a placeholder for the er diagram.
    """
    pass

class ErDiagram(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    """
    Run when the er_diagram directive is first encountered.
    """
    option_spec = {
    }

    def run(self):
        node = er_diagram()
        if self.arguments:
            file = self.arguments[0]
            path = (self.get_directive_path(file))
            content = self.get_file_content(path)
        else:
            content = self.content

        node['content'] = content
        node['font_path'] = self.get_fontpath()
        node['font_name'] = 'ipagp'

        return [node]

    def get_fontpath (self):
         script_path = os.path.dirname(__file__)
         return os.path.join(script_path, 'fonts/ipagp00303')

    def get_directive_path(self, path):
        source = self.state_machine.input_lines.source(self.lineno - self.state_machine.input_offset - 1)
        source_dir = os.path.dirname(os.path.abspath(source))
        path = os.path.normpath(os.path.join(source_dir, path))
        return path

    def get_file_content(self, path):
        content = codecs.open(path, 'r', 'utf_8')
        temp_content = []
        for line in content:
            temp_content.append(line.replace(('¥r'or'¥n' or '\r\n'),''))
        return temp_content

class Digraph:
    def __init__(self, node):
        self.content = node['content']
        self.font_path = node['font_path']
        self.font_name = node['font_name']

    def get_diagraph(self, context):
        return 'digraph ERDiagram { \n' + context + '}'

    def get_graph_property(self):
        str = '''graph[
        labelloc = "t",
        labeljust = "c",
        charset="UTF-8",
        fontsize=12,
        rankdir=LR,
        nodesep=1,
        '''
        str += 'fontpath="%s"' % self.font_path
        str += 'fontname="%s"' % self.font_name
        str += '];'
        return str

    def get_node_property(self):
        str = '''
        node[
               shape=plaintext,
               style="solid",
               layout=dot,
               fontsize=12,
               margin = 0,
        '''
        str += 'fontpath="%s"' % self.font_path
        str += 'fontname="%s"' % self.font_name
        str += '];'
        return str

    def get_edge_property(self):
        str = '''
        edge [
            fontsize=11
        '''
        str += 'fontpath="%s"' % self.font_path
        str += 'fontname="%s"' % self.font_name
        str += '];'
        return str

    def generate_header(self):
        return self.get_graph_property() + self.get_node_property() + self.get_edge_property()

    def generate_dot(self):
        dot_context = self.generate_header()

        entities = Entities()
        relations = Relations()
        yml = yaml.load('\n'.join(self.content))

        for name, contents in yml['entities'].items():
            entities.append(name, contents['columns'])

        dot_context += entities.dot_string()

        if 'relations' in yml:
            for relation in yml['relations']:
                relations.append(relation)

            dot_context += relations.dot_string()

        return self.get_diagraph(dot_context)

'''
エンティティの関係のリストを保存するクラス
'''
class Relations(object):
    list = []

    def __init__(self):
        self.list = []

    def append(self, relation):
        self.list.append(Relation(relation))

    def dot_string(self):
        dot = ''
        for relation in self.list:
            dot = dot + relation.dot_string()
        return dot

'''
関連を表現するクラス
'''
class Relation(object):
    dir_map = { '->': 'forward', '<-':'back', '<->': 'both', '--': 'none' }
    relation_map = { '*': '0..*', '+': '1..*', '1' : '1', '?': '0..1' }

    def __init__(self, relation):
        if isinstance(relation, str):
            str_relation = relation
            options = None
        else:
            for name, option in relation.items():
                str_relation = name
                options = option
        match_relation = re_relation.match(str_relation)
        self.source = match_relation.group(1).replace(' ', '_')
        self.target = match_relation.group(5).replace(' ', '_')
        self.set_option(options, match_relation)

    def set_option (self, options, match_relation):
        temp_options = options if options else {}

        #arrow
        if match_relation.group(3):
            temp_options['dir'] = self.dir_map[match_relation.group(3)]

        #headelabel
        if match_relation.group(4):
            temp_options['headlabel'] = '"' + self.relation_map[match_relation.group(4)] + '"'
        #taillabel
        if match_relation.group(2):
            temp_options['taillabel'] = '"' + self.relation_map[match_relation.group(2)] + '"'

        str_option = '['
        for key, value in temp_options.items():
            str_option = str_option + key + '=' + value + ','

        str_option = str_option + ']'
        self.option = str_option


    def dot_string(self):
        dot =  self.source + ' -> ' + self.target + self.option
        return dot

class Entities(object):

    def __init__(self):
        self.list = []

    def append(self, name, columns):
        self.list.append(Entity(name, columns))

    def dot_string(self):
        dot = ''
        for entity in self.list:
            dot = dot + entity.dot_string()
        #for i in range(len(self.list)-1):
        #    dot = dot +  (self.list[i].rel_name + ' -> ' + self.list[i+1].rel_name + '[color="white"]')
        return dot


'''
エンティティを表すクラス
'''
class Entity(object):

    def __init__(self, name, columns):
        self.name = name
        self.rel_name = name.replace(' ', '_')
        self.columns = Columns(columns)

    def dot_string(self):
        dot = '"' + self.rel_name + '" [label = < <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">'
        dot = dot + '<TR><TD BGCOLOR="#A3A3A3" ALIGN="midle"><B>' + self.name + '</B></TD></TR>'
        if len(self.columns.pk_list) > 0:
            dot = dot + '<TR ><TD MARGIN="0"><TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">'
            for column in self.columns.pk_list:
                dot = dot + column.dot_string()
            dot = dot + '</TABLE></TD></TR>'
        if len(self.columns.list) > 0:
            dot = dot + '<TR><TD><TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">'
            for column in self.columns.list:
                dot = dot + column.dot_string()
            dot = dot + '</TABLE></TD></TR>'
        dot = dot + '</TABLE> >];'
        return dot

'''
エンティティの行のリストを表すクラス
'''
class Columns(object):

    def __init__(self, columns):
        self.pk_list = []
        self.list = []
        for ymlColumn in columns:
            if isinstance(ymlColumn, OrderedDict) :
                for name, options in ymlColumn.items():
                    column = Column(name, options)
            else:
                column = Column(ymlColumn, None)

            if column.is_pk:
                self.pk_list.append(column)
            else:
                self.list.append(column)

    def dot_string(self):
        dot = ''
        for column in self.list:
            dot += column.dot_string()
        return dot


'''
エンティティの行を表すクラス
'''
class Column(object):

    def __init__(self, name, options):
        self.name = name
        if options:
            self.label = options['label'] if 'label' in options else ''
            self.is_pk = options['pk'] if 'pk' in options else False
            self.is_fk = options['fk'] if 'fk' in options else False
            self.is_not_null = options['notnull'] if 'notnull' in options else False
        else:
            self.label = ''
            self.is_pk = False
            self.is_fk = False
            self.is_not_null = False

    def dot_string(self):
        dot ='<TR><TD ALIGN="left">'

        temp_col_name = self.name
        if self.is_pk:
            temp_col_name = '<U>%s</U>' % temp_col_name
        if self.is_not_null:
            temp_col_name = '<B>%s</B>' % temp_col_name
        if self.is_fk:
            temp_col_name = '<I>%s</I>' % temp_col_name
        if self.label:
            temp_col_name += ' </TD><TD><FONT POINT-SIZE="10" ALIGN="right">[%s]</FONT>' % self.label

        dot += temp_col_name + '</TD></TR>'
        return dot


def html_visit_er_diagram(self, node):
    digraph = Digraph(node)
    dotcode = digraph.generate_dot()
    render_dot_html(self, node, dotcode, {}, 'ERDiagram', 'ERDiagram',
                    alt='ER図')
    raise nodes.SkipNode

def skip(self, node):
    raise nodes.SkipNode

def setup(app):
    app.setup_extension('sphinx.ext.graphviz')
    app.add_node(
        er_diagram,
        latex=(skip, None),
        html=(html_visit_er_diagram, None),
        text=(skip, None),
        man=(skip, None),
        texinfo=(skip, None))
    app.add_directive('er-diagram', ErDiagram)
    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}