<h1 align="center">POUPY</h1>

Jogo de pet virtual feito em **Python + pygame**, inspirado em Pou e Tamagotchi. Cuide do seu bichinho: dê comida, dê banho e faça carinho para mantê-lo feliz.

O projeto nasceu para praticar lógica de programação e orientação a objetos.

## Como jogar

O jogo é controlado apenas com o mouse:

| Ação | Como fazer |
| --- | --- |
| Alimentar | Clique no botão da maçã e leve a maçã até o bichinho |
| Dar banho | Clique no botão do sabão e passe o sabão sobre o bichinho |
| Fazer carinho | Mantenha o botão esquerdo pressionado sobre o bichinho |

As barras no canto superior esquerdo mostram **fome**, **limpeza** e **felicidade**. Elas diminuem com o tempo. O progresso é salvo automaticamente ao fechar a janela.

## Requisitos

- Python 3.10 ou superior
- [pygame](https://www.pygame.org/) 2.5 ou superior (instalado via `requirements.txt`)

## Instalação e execução

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd POUPY

# 2. Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o jogo (a partir da raiz do projeto)
python -m poupy
```

> O arquivo de save `save_bixinho.dat` é criado no diretório de onde o jogo é executado.

## Estrutura do projeto

```
POUPY/
├── poupy/                  # código do jogo
│   ├── __main__.py         # ponto de entrada e game loop
│   ├── constantes.py       # constantes, carga de sprites e save/load
│   └── entidades/          # classes do jogo
│       ├── bixinho.py      # o pet (Poupy)
│       ├── barras.py       # barras de fome, limpeza e felicidade
│       ├── comida.py       # maçã
│       ├── sabao.py        # sabão
│       ├── mouse.py        # cursor (mão)
│       ├── botao_comida.py # botão da maçã
│       └── botao_sabao.py  # botão do sabão
├── assets/
│   ├── sprites/            # imagens
│   └── musica/             # trilha sonora
├── requirements.txt
└── LICENSE
```

## Próximos passos (refactor)

- Tipar e documentar o código, seguindo a PEP 8.
- Trocar o save em `pickle` por JSON e tratar exceções específicas.
- Carregar assets fora do escopo de importação e encapsular o game loop em uma função/classe.
- Gerar um executável (`.exe`) para quem quiser jogar sem ter Python instalado.

## Notas do criador

- Todos os sprites usados neste momento são temporários; os finais serão inseridos ao fim do projeto.

## Créditos

- Música: *Young Love* — BoxCat Games.

## Licença

Distribuído sob a licença descrita em [LICENSE](LICENSE).
