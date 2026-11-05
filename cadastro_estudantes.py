# -*- coding: utf-8 -*-
"""
PIM I - UNIP (ADS) - Plataforma de educação digital segura
Conecta Saber (organização fictícia)

Programa em modo console para cadastrar, consultar, alterar e excluir
estudantes, com armazenamento em arquivo JSON e estatísticas básicas.
"""

import json
import os
import statistics
from collections import Counter

ARQUIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usuarios.json")
IDADE_MINIMA = 10
IDADE_MAXIMA = 120
FAIXAS = [("10 a 14", 10, 14), ("15 a 19", 15, 19),
          ("20 a 29", 20, 29), ("30 ou mais", 30, IDADE_MAXIMA)]


# ---------------------------------------------------------------- arquivo
def carregar():
    """Lê o arquivo JSON e devolve a lista de estudantes."""
    if not os.path.exists(ARQUIVO):
        return []
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except (json.JSONDecodeError, OSError) as erro:
        print(f"Erro ao ler {ARQUIVO}: {erro}")
        print("Corrija ou renomeie o arquivo antes de continuar.")
        raise SystemExit(1)
    if not isinstance(dados, list):
        print("Formato inesperado no arquivo JSON (era esperada uma lista).")
        raise SystemExit(1)
    return dados


def salvar(estudantes):
    """Grava a lista em JSON (arquivo temporário + substituição)."""
    temporario = ARQUIVO + ".tmp"
    with open(temporario, "w", encoding="utf-8") as f:
        json.dump(estudantes, f, ensure_ascii=False, indent=4)
    os.replace(temporario, ARQUIVO)


# ---------------------------------------------------------------- entrada
def ler_texto(mensagem, atual=None):
    """Lê texto não vazio. Se 'atual' for informado, Enter mantém o valor."""
    while True:
        sufixo = f" [{atual}]" if atual else ""
        valor = input(f"{mensagem}{sufixo}: ").strip()
        if valor:
            return valor
        if atual:
            return atual
        print("O campo não pode ficar vazio.")


def ler_idade(atual=None):
    """Lê uma idade válida."""
    while True:
        sufixo = f" [{atual}]" if atual is not None else ""
        valor = input(f"Idade{sufixo}: ").strip()
        if not valor and atual is not None:
            return atual
        if valor.isdigit() and IDADE_MINIMA <= int(valor) <= IDADE_MAXIMA:
            return int(valor)
        print(f"Informe uma idade entre {IDADE_MINIMA} e {IDADE_MAXIMA} anos.")


def ler_id(mensagem):
    valor = input(mensagem).strip()
    return int(valor) if valor.isdigit() else None


def buscar(estudantes, id_estudante):
    for e in estudantes:
        if e["id"] == id_estudante:
            return e
    return None


def novo_id(estudantes):
    return max((e["id"] for e in estudantes), default=0) + 1


# ---------------------------------------------------------------- opções
def cadastrar(estudantes):
    print("\n--- Novo cadastro ---")
    estudante = {
        "id": novo_id(estudantes),
        "nome": ler_texto("Nome"),
        "idade": ler_idade(),
        "curso": ler_texto("Curso de interesse"),
    }
    estudantes.append(estudante)
    salvar(estudantes)
    print(f"Estudante cadastrado com o ID {estudante['id']}.")


def listar(estudantes):
    print("\n--- Estudantes cadastrados ---")
    if not estudantes:
        print("Nenhum estudante cadastrado.")
        return
    print(f"{'ID':<5}{'Nome':<30}{'Idade':<7}Curso")
    for e in estudantes:
        print(f"{e['id']:<5}{e['nome']:<30}{e['idade']:<7}{e['curso']}")


def alterar(estudantes):
    print("\n--- Alterar cadastro ---")
    e = buscar(estudantes, ler_id("ID do estudante: "))
    if e is None:
        print("Estudante não encontrado.")
        return
    print("Pressione Enter para manter o valor atual.")
    e["nome"] = ler_texto("Nome", e["nome"])
    e["idade"] = ler_idade(e["idade"])
    e["curso"] = ler_texto("Curso de interesse", e["curso"])
    salvar(estudantes)
    print("Cadastro atualizado.")


def excluir(estudantes):
    print("\n--- Excluir cadastro ---")
    e = buscar(estudantes, ler_id("ID do estudante: "))
    if e is None:
        print("Estudante não encontrado.")
        return
    if input(f"Excluir '{e['nome']}'? (s/n): ").strip().lower() == "s":
        estudantes.remove(e)
        salvar(estudantes)
        print("Cadastro excluído.")
    else:
        print("Operação cancelada.")


def estatisticas(estudantes):
    print("\n--- Estatísticas (dados agregados) ---")
    if not estudantes:
        print("Sem dados para analisar.")
        return
    idades = [e["idade"] for e in estudantes]
    total = len(idades)
    print(f"Total de estudantes: {total}")
    print(f"Idade média: {statistics.mean(idades):.1f} anos")
    print(f"Idade mediana: {statistics.median(idades):.1f} anos")
    print(f"Menor / maior idade: {min(idades)} / {max(idades)} anos")
    print("Distribuição por faixa etária:")
    for nome, minimo, maximo in FAIXAS:
        qtd = sum(1 for i in idades if minimo <= i <= maximo)
        print(f"  {nome:<11}{qtd:>4}  ({qtd / total * 100:.1f}%)")
    print("Cursos de maior interesse:")
    for curso, qtd in Counter(e["curso"] for e in estudantes).most_common(3):
        print(f"  {curso}: {qtd}")


# ---------------------------------------------------------------- menu
def menu():
    estudantes = carregar()
    opcoes = {"1": cadastrar, "2": listar, "3": alterar,
              "4": excluir, "5": estatisticas}
    while True:
        print("\n=== CONECTA SABER - Cadastro de estudantes ===")
        print("1 - Cadastrar\n2 - Listar\n3 - Alterar\n4 - Excluir")
        print("5 - Estatísticas\n0 - Sair")
        escolha = input("Opção: ").strip()
        if escolha == "0":
            print("Encerrando o programa.")
            break
        acao = opcoes.get(escolha)
        if acao:
            acao(estudantes)
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
