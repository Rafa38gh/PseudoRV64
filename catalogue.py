"""Ponto de implementação das regras declarativas do enunciado."""

import load_previous
from ast_nodes import (BinaryExpr, BinaryOperator, BoolLiteral, CallExpr, IdentifierExpr, TypeName, UnaryExpr, UnaryOperator)
from patterns import (COND, EFFECT, IMM12, POW2, REG, Args, Need, Pattern, Rule, imm12, neg_imm12, pow2, signed_literal)

def is_signed_literal(node):
    """Literal inteiro com sinal"""
    return signed_literal(node) is not None

def is_bool(node):
    """Expressão booleana"""
    return node.metadata.get("type") is TypeName.BOOL

def returns_value(node):
    """Chamada de função não void"""
    return node.metadata.get("type") is not TypeName.VOID

TWO_REGS = (Need(REG), Need(REG))
TWO_CONDS = (Need(COND), Need(COND))

def catalogue():
    """Codifique o catálogo do enunciado com Rule e Pattern."""
    raise NotImplementedError("implemente o catálogo")
