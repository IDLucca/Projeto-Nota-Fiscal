# 🥖 Sistema de NFC-e - Padaria Quero Mais

Sistema completo de gestão de NFC-e (Nota Fiscal de Consumidor Eletrônica) desenvolvido para padarias e estabelecimentos similares, com interface gráfica moderna e funcionalidades avançadas.

## ✨ Funcionalidades Principais

### 🔐 Sistema de Login
- Interface de login profissional com design moderno
- Autenticação segura de usuários
- Tela de boas-vindas personalizada

### 🏢 Gestão de Dados da Empresa
- Cadastro completo de dados da empresa
- Validação automática de CNPJ
- Armazenamento persistente de informações

### 📦 Gestão de Produtos
- Cadastro de produtos com código, descrição e preço
- Edição e remoção de produtos
- Lista organizada com busca e filtros

### 🧾 Geração de NFC-e
- Interface intuitiva para criação de NFC-e
- Validação automática de CPF/CNPJ do cliente
- Cálculo automático de impostos (ICMS, PIS, COFINS)
- Geração de DANFE NFC-e conforme NT 2020.004
- Geração de XML NFC-e conforme padrão SEFAZ (modelo 65)

### 📋 Histórico e Gestão
- Histórico completo de NFC-e
- Filtros por cliente
- Status de NFC-e (Pendente/Concluída)
- Reimpressão de NFC-e
- Visualização de DANFE

### 🖨️ Impressão e Exportação
- Impressão automática de NFC-e
- Geração de DANFE em pasta organizada
- Geração de XMLs NFC-e para integração com SEFAZ
- QR Code para consulta de autenticidade

## 🛠️ Tecnologias Utilizadas

- **Python 3.13+** - Linguagem principal
- **Tkinter** - Interface gráfica
- **ReportLab** - Geração de PDFs
- **Pillow (PIL)** - Manipulação de imagens
- **QRCode** - Geração de códigos QR
- **Cryptography** - Criptografia e certificados digitais
- **PyWin32** - Integração com Windows
- **XML** - Geração de documentos NFC-e

## 📋 Pré-requisitos

- Python 3.13 ou superior
- Windows 10/11
- Impressora configurada (opcional)

## 🚀 Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/IDLucca/Projeto-Nota-Fiscal.git
cd Projeto-Nota-Fiscal
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Execute o sistema:**
```bash
python sistema_nota_fiscal.py
```

## 📁 Estrutura do Projeto

```
Sistema de nota fiscal/
├── sistema_nota_fiscal.py      # Arquivo principal
├── requirements.txt            # Dependências
├── dados_sistema.json         # Dados salvos do sistema
├── pdfs/                      # Pasta com PDFs gerados
├── xmls/                      # Pasta com XMLs NF-e
├── Guia e tutoriais/          # Documentação
└── README.md                  # Este arquivo
```

## 🔧 Configuração Inicial

1. **Primeiro acesso:**
   - Usuário: `admin1`
   - Senha: `admin123`

2. **Configure os dados da empresa:**
   - Acesse a aba "Dados da Empresa"
   - Preencha todas as informações
   - Clique em "Salvar Dados da Empresa"

3. **Cadastre os produtos:**
   - Acesse a aba "Produtos"
   - Adicione os produtos da sua padaria
   - Inclua código, descrição, preço e unidade

## 📖 Como Usar

### Criando uma NFC-e

1. Acesse a aba "Nova NFC-e"
2. Preencha os dados do cliente
3. Adicione os produtos desejados
4. Clique em "Gerar e Imprimir NFC-e"

### Gerenciando o Histórico

1. Acesse a aba "Histórico"
2. Use os filtros para encontrar NFC-e específicas
3. Visualize, reimprima ou altere o status das NFC-e

## 🔒 Segurança e Conformidade

- Validação automática de CPF/CNPJ
- Geração de XML NFC-e conforme padrão SEFAZ
- Suporte a certificados digitais
- Criptografia de dados sensíveis
- Backup automático de dados

## 📊 Recursos Avançados

### Geração de XML NFC-e
- Conformidade com padrão SEFAZ (modelo 65)
- Chave de acesso automática
- Protocolo de autorização
- QR Code para consulta conforme NT 2020.004

### Sistema de Impressão
- Impressão automática
- Suporte a múltiplas impressoras
- Preview antes da impressão
- Configuração de margens

## 🐛 Solução de Problemas

### Erro de Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Erro de Impressão
- Verifique se a impressora está conectada
- Configure a impressora padrão no Windows
- Use "Visualizar PDF" para impressão manual

### Erro de Certificado Digital
- O sistema funciona sem certificado em modo homologação
- Para produção, configure certificado A1/A3

## 📞 Suporte

Para suporte técnico ou dúvidas:
- Abra uma issue no GitHub
- Consulte a pasta "Guia e tutoriais"
- Verifique os logs de erro no console

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🎯 Roadmap

- [ ] Integração com sistemas contábeis
- [ ] Relatórios gerenciais
- [ ] Backup na nuvem
- [ ] Versão mobile
- [ ] Integração com balanças
- [ ] Sistema de estoque

---

**Desenvolvido com ❤️ para padarias e estabelecimentos similares** 