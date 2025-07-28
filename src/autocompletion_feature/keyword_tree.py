import unicodedata

class Node:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0


class KeywordTree:
    def __init__(self):
        self.root = Node()
        self.nb_keyword = 0

    def insert(self, word: str) -> None:
        current_node = self.root
        for character in unicodedata.normalize('NFD', word).encode('ascii', 'ignore').decode('utf-8').lower():
            if character not in current_node.children:
                current_node.children[character] = Node()
            current_node = current_node.children[character]
        current_node.frequency += 1
        current_node.is_end_of_word = True
        self.nb_keyword += 1

    def _recursive_search_suffix(self, node: Node, prefix: str) -> list[str]:
        words = []
        if node.is_end_of_word:
            words.append((prefix, node.frequency))

        for char, child_node in node.children.items():
            words.extend(self._recursive_search_suffix(child_node, prefix + char))

        return words

    def search(self, prefix : str) -> list[str]:
        current_node = self.root

        for character in prefix:
            if character in current_node.children:
                current_node = current_node.children[character]
            else :
                return []

        return self._recursive_search_suffix(current_node, prefix)
