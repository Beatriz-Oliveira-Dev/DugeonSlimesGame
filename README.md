# Dungeon Slimes – Roguelike em Python (PGZero)

Bem-vindo ao **Dungeon Slimes**, um mini-jogo estilo **roguelike** criado com **Python + Pygame Zero (PGZero)**.  
Seu objetivo é simples: **navegar pelo labirinto, desviar dos slimes, pegar o tesouro e escapar pela porta!**

O projeto segue todas as regras exigidas no teste:  
✔ PGZero  
✔ math e random  
✔ Rect do pygame  
✔ Sprite animation  
✔ Inimigos com movimento  
✔ Menu com botões clicáveis  
✔ Música e sons On/Off  
✔ Mecânica lógica clara  
✔ Totalmente escrito manualmente  

---

## Como Jogar

### Controles
| Ação | Tecla |
|------|--------|
| Mover para cima | ↑ |
| Mover para baixo | ↓ |
| Mover para esquerda | ← |
| Mover para direita | → |
| Confirmar (Game Over / Vitória) | ENTER |
| Clicar no menu | Mouse |

### Objetivo
1. Pegue o **tesouro** no canto superior esquerdo  
2. Vá até a **porta de saída**  
3. Não encoste nos **slimes**!

---

## Como Rodar o Projeto

### 1. Instalar Python
Baixe e instale o Python 3.10 ou superior  
https://www.python.org/downloads/

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
```

Windows:
```bash
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:
```bash
source .venv/bin/activate
```

### 3. Instalar o Pygame Zero

```bash
pip install pgzero
```

### 4. Estrutura de Pastas

```
Dungeon_Slimes/
│── game.py
│── images/
│── sounds/
```

### 5. Rodar o Jogo

```bash
pgzrun game.py
```

---

## Recursos

- Menu inicial (Play / Music ON-OFF / Exit)
- Música ambiente + efeitos sonoros
- Slimes inimigos com patrulha
- Animação de sprites
- Movimento suave por tiles (roguelike real)
- Colisões com paredes
- Tela de Game Over estilizada
- Tela de Vitória estilizada

---

## Tecnologias

- Python 3  
- Pygame Zero  
- math e random  

---
