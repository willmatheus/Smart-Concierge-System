# Portaria Inteligente com ESP32, Raspberry Pi e Reconhecimento Facial

Este projeto implementa uma solução de portaria inteligente utilizando microcontroladores ESP32 e Raspberry Pi 3B+, integrados via Node-RED, com funcionalidades de reconhecimento facial, notificações em tempo real e controle automatizado.

## **Pré-requisitos**

1. **Docker**: Certifique-se de ter o Docker instalado para gerenciamento do banco de dados.
2. **Node-RED**: Deve estar configurado e rodando no fundo.
3. **Simulador de Hardware (Wokwi)**: Execute o link do Wokwi para simular o hardware.
4. **Python 3.8+**: Para execução dos scripts `main.py` e `recogface.py`.

---

## **Passos para Execução**

### 1. **Iniciar o Banco de Dados**
   - Inicialize o container Docker:
     ```bash
     docker-compose up -d
     ```
   - Execute os comandos de setup do banco de dados:
     ```bash
     flask db init
     flask db upgrade
     ```

### 2. **Configurar e Rodar o Node-RED**
   - Certifique-se de que o Node-RED está em execução e com o fluxo correto configurado.

### 3. **Simular o Hardware no Wokwi**
   - Acesse o link de simulação do Wokwi e inicie o projeto de hardware.

---

## **Execução do Sistema**

### 1. **Cadastro de Usuário e Treinamento da IA**
   - Execute `main.py` para abrir a interface de cadastro:
     ```bash
     python main.py
     ```
   - Realize o cadastro facial dos moradores, que irá treinar o modelo de IA.

### 2. **Reconhecimento Facial**
   - Execute `recogface.py` para iniciar o reconhecimento:
     ```bash
     python recogface.py
     ```
   - O sistema detecta moradores registrados. Caso não detecte ninguém por 5 segundos, abrirá automaticamente a tela de visitante.

---

## **Notificação para o APK**
- Após inserir as informações do visitante e o apartamento desejado, uma notificação será enviada para o aplicativo disponível no repositório.

---

## **Estrutura do Projeto**

```
/projeto-portaria-inteligente
├── docker-compose.yml
├── main.py               # Tela de cadastro e treinamento facial
├── recogface.py           # Script de reconhecimento facial
├── Node-RED/              # Fluxos Node-RED
└── README.md              # Documentação do projeto
```

---
