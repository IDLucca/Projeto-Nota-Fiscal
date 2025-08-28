# Sistema de Nota Fiscal

Um sistema simples e completo para geração e impressão de notas fiscais para sua empresa.

## Funcionalidades

- **Cadastro de Dados da Empresa**: Configure os dados da sua empresa (nome, CNPJ, endereço, etc.)
- **Gestão de Produtos**: Cadastre produtos com código, descrição, preço e unidade
- **Geração de Notas Fiscais**: Crie notas fiscais com dados do cliente e itens
- **Impressão**: Imprima notas fiscais diretamente na impressora configurada
- **Histórico**: Visualize e gerencie todas as notas fiscais emitidas
- **Reimpressão**: Reimprima notas fiscais anteriores

## Requisitos do Sistema

- Windows 10 ou superior
- Python 3.7 ou superior
- Impressora configurada no sistema

## Instalação

1. **Instale o Python** (se ainda não tiver):
   - Baixe o Python em: https://www.python.org/downloads/
   - Durante a instalação, marque "Add Python to PATH"

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o sistema**:
   ```bash
   python sistema_nota_fiscal.py
   ```

## Como Usar

### 1. Configuração Inicial

1. Abra o sistema
2. Vá para a aba "Dados da Empresa"
3. Preencha os dados da sua empresa:
   - Nome da Empresa
   - CNPJ
   - Endereço
   - Cidade/Estado
   - CEP
   - Telefone
4. Clique em "Salvar Dados da Empresa"

### 2. Cadastro de Produtos

1. Vá para a aba "Produtos"
2. Preencha os dados do produto:
   - Código (identificador único)
   - Descrição
   - Preço Unitário
   - Unidade (ex: UN, KG, L)
3. Clique em "Adicionar Produto"
4. Repita para todos os produtos da sua empresa

### 3. Gerando uma Nota Fiscal

1. Vá para a aba "Nova Nota Fiscal"
2. Preencha os dados do cliente:
   - Nome (obrigatório)
   - CPF/CNPJ (opcional)
   - Endereço (opcional)
3. Adicione itens à nota:
   - Selecione o produto no dropdown
   - Informe a quantidade
   - Clique em "Adicionar Item"
4. Repita para todos os itens
5. Clique em "Gerar e Imprimir NF"

### 4. Histórico e Reimpressão

1. Vá para a aba "Histórico"
2. Visualize todas as notas fiscais emitidas
3. Use o filtro por cliente se necessário
4. Selecione uma nota e clique em:
   - "Visualizar NF" para ver o PDF
   - "Reimprimir NF" para imprimir novamente

## Configuração da Impressora

O sistema usa a impressora padrão configurada no Windows. Para configurar:

1. Vá em "Configurações" > "Dispositivos" > "Impressoras e scanners"
2. Selecione sua impressora como padrão
3. Ou use "Impressoras e scanners" > "Gerenciar" para configurar

## Estrutura de Arquivos

- `sistema_nota_fiscal.py` - Sistema principal
- `requirements.txt` - Dependências do projeto
- `dados_sistema.json` - Dados salvos (criado automaticamente)
- `README.md` - Este arquivo

## Recursos Técnicos

- **Interface**: Tkinter (nativa do Python)
- **Geração de PDF**: ReportLab
- **Impressão**: Win32 API
- **Armazenamento**: JSON local
- **Sistema**: Windows

## Suporte

Para problemas ou dúvidas:
1. Verifique se todas as dependências estão instaladas
2. Certifique-se de que a impressora está configurada
3. Verifique se o Python está na versão correta

## Notas Importantes

- Este é um sistema simplificado para controle interno
- As notas fiscais geradas não são oficiais para fins fiscais
- Sempre mantenha backup dos dados (`dados_sistema.json`)
- O sistema salva automaticamente todos os dados

## Personalização

Você pode personalizar:
- Layout da nota fiscal editando o método `gerar_pdf()`
- Campos adicionais editando as estruturas de dados
- Estilo da interface modificando os widgets Tkinter 