# AGENTS.md — POUPY

Instruções para agentes de IA que trabalham neste repositório. Leia tudo antes de agir.

## Visão geral

POUPY é um jogo de pet virtual (estilo Pou / Tamagotchi) feito em **Python + pygame**, criado para praticar lógica de programação e orientação a objetos.

- `main.py` — ponto de entrada e game loop. Rode com `python main.py`.
- `constantes.py` — constantes (janela, cores, fontes, relógio) e funções de save/load.
- `classe_*.py` — classes do jogo (Poupy, Barras, Comida, Sabão, Mouse, botões).
- `sprites/` e `trilha sonora/` — assets binários.
- `save_bixinho.dat` — save local do jogador (pickle). **Não versionar.**
- Branch de trabalho atual: `refactor/v2`. Branch principal: `main`.
- Idioma do código, comentários e mensagens: **português**. Mantenha o padrão existente.

## Regras de Git (CRÍTICAS)

1. **NUNCA faça commit sozinho.** Só rode `git commit` quando o usuário pedir explicitamente, naquela mensagem. Autorização para um commit não vale para os seguintes.
2. **NUNCA** rode sem pedido explícito: `git push`, `git merge`, `git rebase`, `git reset --hard`, `git checkout -- <arquivo>`, `git restore` (que descarte mudanças), `git clean`, `git stash drop`, `git branch -D`, `git commit --amend`, `--force`, `--no-verify`, `git tag`.
3. Comandos somente leitura são livres: `git status`, `git diff`, `git log`, `git show`, `git blame`, `git branch` (listar).
4. Não use `git add` por conta própria. Quando pedirem commit, adicione arquivos **por nome**; nunca `git add -A` / `git add .` às cegas.
5. Nunca commite: `save_bixinho.dat`, `.env`, segredos, `__pycache__/`, venvs ou arquivos gerados.
6. Não commite direto em `main`. Não reescreva histórico já publicado.
7. Não altere `.gitignore` nem a configuração do git sem pedir.
8. Quando pedirem commit: commits pequenos e focados, mensagem no imperativo, curta e clara, em português (ex.: `Corrige decaimento da barra de fome`).
9. Ao terminar uma tarefa, deixe as mudanças no working tree e resuma o que mudou. Se achar que vale commitar, **sugira** — não execute.

## Regras de Python

- Siga a **PEP 8**: `snake_case` para funções/variáveis, `PascalCase` para classes, `UPPER_SNAKE_CASE` para constantes (centralizadas em `constantes.py`).
- Use **type hints** e docstrings curtas em código novo.
- Imports ordenados: biblioteca padrão, terceiros (`pygame`), locais. Evite `from x import *` em código novo.
- Use `with open(...)` para arquivos; nunca abrir/fechar manualmente.
- Nunca use `except:` nu. Capture exceções específicas (`FileNotFoundError`, `pickle.UnpicklingError`, `EOFError`...).
- Sem números mágicos: extraia para constantes nomeadas.
- Funções pequenas, com uma responsabilidade. Prefira composição a lógica duplicada.
- Use `pathlib.Path` para caminhos.
- `pickle` só com dados confiáveis; para formatos de save novos, prefira JSON.
- Proteja o ponto de entrada com `if __name__ == "__main__":`.
- Encerre com `pygame.quit()` seguido de `sys.exit()`.
- Não adicione dependências novas sem perguntar.
- Sem código morto, prints de debug ou código comentado deixados para trás.

## Regras de pygame

- Chame `pygame.init()` **uma vez**, no `main`.
- Um único game loop: **eventos → update → draw → flip/update → `clock.tick(FPS)`**.
- Limite o FPS com `pygame.time.Clock`; use delta time para movimento/decaimento. Nunca use `time.sleep` nem loops bloqueantes.
- Carregue imagens, sons e fontes **uma vez**, fora do loop, com `convert()` / `convert_alpha()`. Nunca crie superfícies ou fontes a cada frame.
- Use `pygame.sprite.Sprite` e `Group` (ex.: `LayeredUpdates`); separe `update()` (lógica) de desenho.
- Colisão com `pygame.Rect`, `colliderect` e `pygame.sprite.spritecollide`.
- Trate `pygame.QUIT` e salve o progresso antes de sair.
- Consuma eventos apenas via `pygame.event.get()` no loop principal.
- Caminhos de assets relativos ao arquivo (`Path(__file__).parent`), não ao diretório atual.
- Dimensões, FPS, cores e fontes ficam em `constantes.py`.
- Mantenha o volume de áudio moderado e não bloqueie o loop ao tocar sons.

## Fluxo de trabalho do agente

- Leia o código relevante antes de editar. Faça mudanças **mínimas e focadas** no pedido.
- Não refatore nem renomeie fora do escopo sem pedir.
- Não crie arquivos extras (docs, testes, scripts) sem pedir.
- Valide quando possível: `python -m py_compile <arquivo>.py` e/ou rodar o jogo.
- Em caso de ambiguidade, pergunte em vez de assumir.
- Não modifique `sprites/` nem `trilha sonora/` (binários) sem pedido explícito.
- Ao final, explique de forma breve o que foi alterado e por quê.
