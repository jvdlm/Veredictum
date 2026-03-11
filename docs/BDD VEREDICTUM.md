Histórias de Usuário e Cenários de Validação (BDD)  
Projeto: Veredictum  
Sistema de gestão de processos jurídicos para escritórios de advocacia.

**História 1 — Cadastro de Processos Jurídicos**

### **História de Usuário**

**Como** advogado  
 **Quero** cadastrar processos jurídicos no sistema  
 **Para que** eu possa organizar e acompanhar os casos do escritório.

### **Cenários de Validação (BDD)**

**Cenário 1 — Cadastro de processo com sucesso**

Dado que o advogado está na tela de cadastro de processos  
 Quando ele preencher corretamente os campos obrigatórios  
 E clicar em "Salvar"  
 Então o sistema deve cadastrar o processo com sucesso  
 E exibir uma mensagem de confirmação.

**Cenário 2 — Cadastro com campo obrigatório vazio**

Dado que o advogado está na tela de cadastro de processos  
 Quando ele deixar algum campo obrigatório em branco  
 E clicar em "Salvar"  
 Então o sistema deve impedir o cadastro  
 E exibir uma mensagem informando que há campos obrigatórios não preenchidos.

**Cenário 3 — Cadastro de processo duplicado**

Dado que já existe um processo cadastrado com determinado número  
 Quando o advogado tentar cadastrar um processo com o mesmo número  
 Então o sistema deve impedir o cadastro duplicado  
 E informar que o processo já está registrado.

**História 2 — Gerenciamento de Clientes**

### **História de Usuário**

**Como** advogado  
 **Quero** cadastrar e gerenciar clientes  
 **Para que** eu possa associar clientes corretamente aos processos.

### **Cenários de Validação (BDD)**

**Cenário 1 — Cadastro de cliente com sucesso**

Dado que o advogado está na tela de cadastro de clientes  
 Quando ele preencher os dados obrigatórios do cliente  
 E clicar em "Salvar"  
 Então o sistema deve cadastrar o cliente com sucesso.

**Cenário 2 — Cadastro de cliente com CPF/CNPJ duplicado**

Dado que já existe um cliente cadastrado com determinado CPF ou CNPJ  
 Quando o advogado tentar cadastrar outro cliente com o mesmo documento  
 Então o sistema deve impedir o cadastro duplicado  
 E informar que o documento já está registrado.

**Cenário 3 — Atualização de dados do cliente**

Dado que o cliente já está cadastrado no sistema  
 Quando o advogado editar seus dados  
 E salvar as alterações  
 Então o sistema deve atualizar as informações do cliente.

# 

# **História 3 — Exibição de Relatórios**

### **História de Usuário**

**Como** advogado  
 **Quero** visualizar relatórios sobre os processos  
 **Para que** eu possa acompanhar o desempenho e a situação dos casos.

### **Cenários de Validação (BDD)**

**Cenário 1 — Visualização de relatório geral**

Dado que existem processos cadastrados no sistema  
 Quando o advogado acessar a seção de relatórios  
 Então o sistema deve exibir um relatório com informações dos processos.

**Cenário 2 — Relatório filtrado por status**

Dado que existem processos com diferentes status  
 Quando o advogado aplicar um filtro por status  
 Então o sistema deve exibir apenas os processos com o status selecionado.

**Cenário 3 — Relatório sem dados**

Dado que não existem processos cadastrados  
 Quando o advogado acessar a área de relatórios  
 Então o sistema deve informar que não há dados disponíveis.

# 

# **História 4 — Gerenciamento de Prazos e Compromissos**

### **História de Usuário**

**Como** advogado  
 **Quero** registrar prazos e compromissos dos processos  
 **Para que** eu possa acompanhar datas importantes.

### **Cenários de Validação (BDD)**

**Cenário 1 — Cadastro de prazo**

Dado que o advogado está na área de prazos  
 Quando ele registrar um novo prazo para um processo  
 Então o sistema deve armazenar o prazo corretamente.

**Cenário 2 — Visualização de prazos**

Dado que existem prazos cadastrados para um processo  
 Quando o advogado acessar o processo  
 Então o sistema deve exibir os prazos associados.

**Cenário 3 — Data inválida**

Dado que o advogado está cadastrando um prazo  
 Quando ele informar uma data inválida  
 Então o sistema deve impedir o cadastro  
 E exibir uma mensagem de erro.

# 

# **História 5 — Gestão Financeira de Processos**

### **História de Usuário**

**Como** advogado  
 **Quero** registrar valores financeiros relacionados aos processos  
 **Para que** eu possa acompanhar honorários e custos.

### **Cenários de Validação (BDD)**

**Cenário 1 — Registro de honorários**

Dado que existe um processo cadastrado  
 Quando o advogado registrar um valor de honorários  
 Então o sistema deve salvar a informação financeira.

**Cenário 2 — Visualização financeira**

Dado que existem registros financeiros associados ao processo  
 Quando o advogado acessar o resumo financeiro  
 Então o sistema deve exibir os valores registrados.

**Cenário 3 — Valor inválido**

Dado que o advogado está registrando uma movimentação financeira  
 Quando ele informar um valor inválido  
 Então o sistema deve impedir o cadastro.

# 

# **História 6 — Upload de Documentos para Processos**

### **História de Usuário**

**Como** advogado  
 **Quero** enviar documentos para um processo  
 **Para que** eu possa armazenar arquivos importantes no sistema.

### **Cenários de Validação (BDD)**

**Cenário 1 — Upload de documento**

Dado que o advogado está na área de documentos do processo  
 Quando ele selecionar um arquivo válido  
 E clicar em "Enviar"  
 Então o sistema deve anexar o documento ao processo.

**Cenário 2 — Upload sem arquivo**

Dado que o advogado está na área de upload  
 Quando ele clicar em enviar sem selecionar um arquivo  
 Então o sistema deve solicitar a seleção de um arquivo.

**Cenário 3 — Formato inválido**

Dado que o sistema possui restrições de formato  
 Quando o advogado tentar enviar um arquivo inválido  
 Então o sistema deve impedir o upload.

# 

# 

# **História 7 — Arquivar Processos**

### **História de Usuário**

**Como** advogado  
 **Quero** arquivar processos encerrados  
 **Para que** a lista de processos ativos fique organizada.

### **Cenários de Validação (BDD)**

**Cenário 1 — Arquivar processo**

Dado que existe um processo ativo  
 Quando o advogado selecionar a opção "Arquivar"  
 Então o sistema deve alterar o status do processo para arquivado.

**Cenário 2 — Processo removido da lista ativa**

Dado que o processo foi arquivado  
 Quando o advogado visualizar a lista de processos ativos  
 Então o processo arquivado não deve aparecer.

# 

# 

# 

# 

# **História 8 — Reabertura de Processos Arquivados**

### **História de Usuário**

**Como** advogado  
 **Quero** reabrir processos arquivados  
 **Para que** eu possa voltar a trabalhar nesses casos.

### **Cenários de Validação (BDD)**

**Cenário 1 — Reabrir processo**

Dado que existe um processo arquivado  
 Quando o advogado selecionar a opção "Reabrir processo"  
 Então o sistema deve alterar o status do processo para ativo.

**Cenário 2 — Retorno à lista ativa**

Dado que o processo foi reaberto  
 Quando o advogado acessar a lista de processos ativos  
 Então o processo deve aparecer novamente na lista.

# 

# 

# **História 9 — Visualização de Documentos Jurídicos**

### **História de Usuário**

**Como** advogado  
 **Quero** visualizar documentos anexados aos processos  
 **Para que** eu possa consultar arquivos sempre que necessário.

### **Cenários de Validação (BDD)**

**Cenário 1 — Listagem de documentos**

Dado que existem documentos anexados a um processo  
 Quando o advogado acessar a área de documentos  
 Então o sistema deve exibir a lista de arquivos.

**Cenário 2 — Abertura de documento**

Dado que existe um documento anexado  
 Quando o advogado clicar no documento  
 Então o sistema deve abrir ou exibir o arquivo.

# 

# 

# 

# 

# **História 10 — Filtragem Avançada de Processos**

### **História de Usuário**

**Como** advogado  
 **Quero** aplicar filtros na lista de processos  
 **Para que** eu possa encontrar rapidamente um caso específico.

### **Cenários de Validação (BDD)**

**Cenário 1 — Filtrar por cliente**

Dado que existem processos de diferentes clientes  
 Quando o advogado aplicar um filtro por cliente  
 Então o sistema deve exibir apenas os processos daquele cliente.

**Cenário 2 — Filtrar por status**

Dado que existem processos com diferentes status  
 Quando o advogado aplicar um filtro por status  
 Então o sistema deve mostrar apenas os processos com o status selecionado.

**Cenário 3 — Nenhum resultado encontrado**

Dado que o advogado aplicou filtros sem correspondência  
 Quando o sistema processar a busca  
 Então deve exibir uma mensagem informando que nenhum processo foi encontrado.

