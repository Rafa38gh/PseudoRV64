"""Ponto de implementação do reconhecimento de padrões e custos mínimos."""

from patterns import *


class Selector:
    """Selecione coberturas sem executar expressões ou emitir instruções."""

    def __init__(self, rules):
        self.rules = tuple(rules)

    def analyze(self, expr):
        """Calcule mínimos por nó/classe sem emitir instruções."""
        table = SelectionTable()
        self._visit(expr, table)
        return table
    
    def _match(self, pattern, node):
        """Devolve a lista [(subnó, classe)] exigida ou None"""
        if pattern.kind is not None and not isinstance(node, pattern.kind):     # Tipo do nó
            return None
        
        if pattern.operator is not None:                                        # Operador
            if getattr(node, "operator", None) != pattern.operator:
                return None
            
        if pattern.predicate is not None and not pattern.predicate(node):       # Predicado
            return None
        
        if not pattern.children and pattern.predicate is not None:              # Predicado sem filhos
            return []
        
        node_children = children(node)

        if len(pattern.children) == 1 and isinstance(pattern.children[0], Args): # Argumentos de chamada
            result_class = pattern.children[0].result
            return [(arg, result_class) for arg in node_children]
        
        if len(node_children) != len(pattern.children):                         # Caso geral
            return None
        
        needs = []
        for spec, child in zip(pattern.children, node_children):
            if isinstance(spec, Need):
                needs.append((child, spec.result))
            elif isinstance(spec, Pattern):
                inner = self._match(spec, child)
                
                if inner is None:
                    return None
                needs.extend(inner)
            else:
                raise TypeError(f"Padrão de filho inválido: {spec!r}")
        
        return needs
    
    def _visit(self, node, table):
        """Pós-ordem: Resolve os filhos antes de avaliar as regras do nó"""
        for child in children(node):
            self._visit(child, table)

        for rule in self.rules:
            needs = self._match(rule.pattern, node)
            if needs is None:
                continue

            total = rule.cost
            
            for subnode, result_class in needs:
                sub_choice = table.lookup(subnode, result_class)
                if sub_choice is None:
                    break
                total += sub_choice.cost
            else:
                current = table.lookup(node, rule.result)
                if current is None or total < current.cost:
                    table.put(node, rule.result, Choice(total, rule, tuple(needs)))
                    