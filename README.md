# Projeto de Inteligência Artificial desenvolvido para a disciplina de Inteligência Artificial do curso de Ciências da Computação da UFRPE- Busca Clássica (Opção C)

Este projeto implementa e valida uma série de problemas clássicos de Inteligência Artificial utilizando a biblioteca de busca base fornecida (`search_lib`, disponível [neste repositório do GitHub](https://github.com/GustavoFelipeM/search_lib)). O objetivo é garantir a robustez e a corretude das estratégias de busca através de testes automatizados e estruturados.

## Problemas Implementados
Foram modeladas as classes abstratas `State`, `Action` e `Problem` para 3 cenários distintos:
1. **Sliding Puzzle (Quebra-cabeça Deslizante):** Suporte a tabuleiros dinâmicos (3x3, 4x4, etc).
2. **Navegação de Robô em Grid:** Movimentos relativos (girar, avançar) com validação de limites de mapa.
3. **N-Rainhas (N-Queens):** Colocação sequencial com validação de ataques (linha e diagonal).

## Tecnologias e Estrutura
- **Linguagem:** Python 3.12+ (com Anotações de Tipo).
- **Testes:** Framework `pytest`.
- **Estratégias de Busca Testadas:** `BFS` (Busca em Largura) e `DFS` (Busca em Profundidade).

## Como executar os testes
A bateria de testes foi construída para cobrir os "caminhos felizes" (encontrar soluções ótimas) e "casos de falha/limite" (como bater nas paredes do grid e evitar movimentos inválidos).

Na raiz do projeto, com o ambiente virtual ativado, execute:
```bash
python3 -m pytest testes/
