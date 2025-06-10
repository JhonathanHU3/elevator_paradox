# Elavator ParadoxZ

**Elevator Paradox** é um jogo desenvolvido em **Pygame**, onde o jogador deve sobreviver a um apocalipse zumbi dentro de uma faculdade. O jogo desafia o jogador a escolher entre usar o elevador ou as escadas para escapar dos zumbis, com o objetivo de sobreviver o maior tempo possível.

## História

O mundo está em caos! Uma infestação de zumbis tomou conta de uma faculdade e você, o jogador, está preso dentro do prédio. Seu objetivo é escapar, mas há um grande dilema: você deve escolher entre usar o **elevador** ou as **escadas** enquanto os zumbis se aproximam. Ambas as opções têm seus riscos, e suas decisões podem determinar o seu destino.

## Mecânicas do Jogo

- **Escolhas Estratégicas**: O jogador precisa decidir rapidamente entre usar o elevador ou as escadas. Cada escolha tem consequências diferentes.
- **Zumbis**: Os zumbis se aproximam do jogador conforme o tempo passa. A presença deles torna a decisão mais difícil, já que as opções de fuga podem ser comprometidas.
- **Ação e Sobrevivência**: O jogo é uma corrida contra o tempo e exige agilidade e bom senso estratégico para maximizar suas chances de sobrevivência.

## Como Jogar

- **Movimento**: Use as setas do teclado ou as teclas WASD para mover seu personagem.
- **Escolha de Fuga**: Durante o jogo, você será apresentado com uma escolha: usar o **elevador** ou as **escadas**. Cada escolha afetará seu progresso e as ações dos zumbis.
- **Objetivo**: Sobreviva o maior tempo possível, tomando decisões rápidas e estratégicas.

## Arquitetura

O jogo é estruturado seguindo a arquitetura **MVC** (Model-View-Controller), com as seguintes classes principais:

- **Personagem**: Representa o personagem principal e os inimigos do jogo.
- **Jogador**: Controla as ações do personagem do jogador e interage com os elementos do jogo.
- **Inimigo**: Define os zumbis e suas interações com o jogador.
- **Projetil**: Lida com os projéteis disparados durante o jogo.
- **Carta**: Representa eventos e interações do jogo.
- **Round**: Controla o progresso de cada rodada.
- **Run**: Gerencia a execução geral do jogo.

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/elevator-paradox.git
   pip install pygame
   python main.py

## Contribuição

Se você quiser contribuir para o projeto, fique à vontade para abrir um **pull request** ou relatar **issues**. Toda contribuição é bem-vinda!

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
