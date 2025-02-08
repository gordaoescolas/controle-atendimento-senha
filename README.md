# Sistema de Controle de Atendimento por Senha

Sistema web para gerenciamento de filas de atendimento com emissão e chamada de senhas.

## Funcionalidades

- Emissão de senhas normais e preferenciais
- Painel de chamada de senhas com interface para atendentes 
- Display para visualização das senhas chamadas com efeitos visuais e sonoros
- Histórico das últimas chamadas
- Suporte a impressão de senhas via USB
- Reprodução de vídeos no display

## Tecnologias Utilizadas

- Python/Flask para o backend
- HTML/CSS/JavaScript para o frontend
- Server-Sent Events (SSE) para atualizações em tempo real
- WebUSB API para comunicação com impressoras

## Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

1. Inicie o servidor:
```bash
python app.py
```
2. Acesse as interfaces:
- Emissão de senhas: http://localhost/
- Painel do atendente: http://localhost/call
- Display de chamadas: http://localhost/display

### **Você também pode utilizá-lo em uma VPS**
**(para execução em rede, trocar localhost pelo IP do dispositivo onde está rodando o servidor)**

## Configuração da Impressora

Para usar a impressão de senhas, configure o VendorID da sua impressora USB no arquivo [emit.html]. Use o utilitário [update_vendor_id].py para atualizar o ID.

## Estrutura de Arquivos
.
├── app.py
├── requirements.txt
├── static/
│   ├── sounds/
│   └── video/
└── templates/
    ├── call.html
    ├── display.html
    └── emit.html

## Licença

Este projeto está sob a licença MIT.
