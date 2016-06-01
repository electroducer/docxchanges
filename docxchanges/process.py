## This class processes data from the xml tree of a docx file.

from lxml import etree

class DocxProcess:
    word_schema = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    doc_etree = None

    # Initialiser for object
    def __init__(self, tree=None):
        assert tree, "No valid etree assigned"
        self.doc_etree = tree

    # prototype, not currently in use
    def _itertext(self):
        """Iterator to go through xml tree's text nodes"""
        for node in self.doc_etree.iter(tag=etree.Element):
            if self._check_element_is(node, 't'):
                yield (node, node.text)

    def get_text(self):
        """Returns all text as a single string"""
        text = ""
        for node in self.doc_etree.iter(tag=etree.Element):
            if self._check_element_is(node, 't'):
                text += node.text
        return text

    # used for extracting only text
    def get_paragraphs(self,):
        """Returns a list of the text of all paragraphs"""
        paragraphs = []
        idx = -1
        for node in self.doc_etree.iter(tag=etree.Element):
            if self._check_element_is(node, 'p'):
                idx += 1
                paragraphs.append("")
            if self._check_element_is(node, 't'):
                paragraphs[idx] += node.text
        return paragraphs


    def _check_element_is(self, element, type_char):
        """Determines the type of an openxml tag"""
        return element.tag == '{%s}%s' % (self.word_schema, type_char)


    def convert_tag(self, type_char):
        """Returns a word schema tag"""
        return "{" + self.word_schema + "}" + type_char

    # Simplifies the tree but ignores changes
    def simplify_tree(self):
        """Returns an etree using only relevant data"""
        root = etree.Element("d")
        for node in self.doc_etree.iter(tag=etree.Element):
            if self._check_element_is(node, 'p'):
                current_p = etree.SubElement(root, "p")
            elif self._check_element_is(node, 't'):
                current_t = etree.SubElement(current_p, "t")
                current_t.text = node.text
        return root

    def simplify_tree_changes(self):
        """Returns a simplified etree that retains tracked changes"""
        root = etree.Element("d")
        iterator = self.doc_etree.iter()
        for node in iterator:
            if self._check_element_is(node, 'p'):
                current_p = etree.SubElement(root, 'p')
                t_parent = current_p
            elif self._check_element_is(node, 'ins'):
                t_parent = etree.SubElement(current_p, 'ins')
                for child in node.iterdescendants():
                    iterator.next()
                    if self._check_element_is(child, 't'):
                        current_t = etree.SubElement(t_parent, 't')
                        current_t.text = child.text
                t_parent = current_p
            elif self._check_element_is(node, 'del'):
                del_parent = etree.SubElement(current_p, 'del')
                for child in node.iterdescendants():
                    iterator.next()
                    if self._check_element_is(child, 'delText'):
                        delText = etree.SubElement(del_parent, 'delText')
                        delText.text = child.text
            elif self._check_element_is(node, 't'):
                current_t = etree.SubElement(t_parent, 't')
                current_t.text = node.text
        return root

    def get_deletions(self):
        """Returns an array of all deleted tokens according to del tag"""
        deltext = []
        prev_token = ""
        prev_del = ""
        for node in self.doc_etree.iter(self.convert_tag('t'), self.convert_tag('delText')):
            if self._check_element_is(node, 't'):
                skip = False
                for parent in node.iterancestors(self.convert_tag('ins')):
                    skip = True
                if not skip:
                    if node.text[-1].isspace():
                        prev_token = ""
                    else:
                        prev_token = node.text.rsplit(None, 1)[-1]
                    if prev_del and not node.text[0].isspace():
                        deltext[-1] = deltext[-1] + node.text.split(None, 1)[0]
                    prev_del = ""
            else:
                if prev_token and not node.text[0].isspace():
                    deltext.append(prev_token + node.text)
                else:
                    deltext.append(node.text)
                prev_token = ""
                if node.text[-1].isspace():
                    prev_del = ""
                else:
                    prev_del = node.text.rsplit(None, 1)[-1]

        return deltext

    def get_insertions(self):
            """Returns an array of all deleted tokens according to del tag"""
            instext = []
            prev_token = ""
            prev_ins = ""
            for node in self.doc_etree.iter(self.convert_tag('t')):
                ins_tag = False
                for parent in node.iterancestors(self.convert_tag('ins')):
                    ins_tag = True
                if not ins_tag:
                    if node.text[-1].isspace():
                        prev_token = ""
                    else:
                        prev_token = node.text.rsplit(None, 1)[-1]
                    if prev_ins and not node.text[0].isspace():
                        instext[-1] = instext[-1] + node.text.split(None, 1)[0]
                    prev_ins = ""
                else:
                    if prev_token and not node.text[0].isspace():
                        instext.append(prev_token + node.text)
                    else:
                        instext.append(node.text)
                    prev_token = ""
                    if node.text[-1].isspace():
                        prev_ins = ""
                    else:
                        prev_ins = node.text.rsplit(None, 1)[-1]

            return instext


    # Changed this to add the original deletions and insertions
    def get_changes(self):
        """Returns a list of lists for all ins/del pairs"""
        changes = []     # List of 4-lists
                        # x[0] = del, x[1] = ins (surrounding word)
                        # x[2] = del, x[3] = ins (exact original)
        prev_token = ""
        prev_ins = ""
        prev_del = ""
        after_first_ins = False
        after_first_del = False
        for node in self.doc_etree.iter(self.convert_tag('t'), self.convert_tag('delText')):
            if self._check_element_is(node, 't'):
                ins_tag = False
                for parent in node.iterancestors(self.convert_tag('ins')):
                    ins_tag = True
                if not ins_tag: # Case of regular text
                    if node.text[-1].isspace():
                            prev_token = ""
                    else:
                        prev_token = node.text.rsplit(None, 1)[-1]
                    if not node.text[0].isspace():
                        if prev_ins and changes[-1][1]:
                            changes[-1][1] = changes[-1][1] + node.text.split(None, 1)[0]
                        if prev_del and changes [-1][0]:
                            changes[-1][0] = changes[-1][0] + node.text.split(None, 1)[0]
                    prev_ins = ""
                    prev_del = ""
                    after_first_ins = False
                    after_first_del = False

                else: #Case of insertion
                    if after_first_ins:
                        prev_token = ""
                    else:
                        after_first_ins = True
                    if prev_token and not node.text[0].isspace():
                        insertion = prev_token + node.text
                    else:
                        insertion = node.text
                    if node.text[-1].isspace():
                        prev_ins = ""
                    else:
                        prev_ins = node.text.rsplit(None, 1)[-1]
                    if after_first_del:
                        prev_token = ""
                        changes[-1][1] = insertion
                        changes[-1][3] = node.text
                    else:
                        changes.append(["", insertion, "", node.text])
            else: # Case of deleted text
                if after_first_del:
                    prev_token = ""
                else:
                    after_first_del = True
                if prev_token and not node.text[0].isspace():
                    deletion = prev_token + node.text
                else:
                    deletion = node.text
                if node.text[-1].isspace():
                    prev_del = ""
                else:
                    prev_del = node.text.rsplit(None, 1)[-1]
                if after_first_ins:
                    prev_token = ""
                    changes[-1][0] = deletion
                    changes[-1][2] = node.text
                else:
                    changes.append([deletion, "", node.text, ""])
        return changes
