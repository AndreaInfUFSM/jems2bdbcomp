# jems2bdbcomp
Cadastra artigos na BDBCOMP a partir de dados exportados do JEMS

## Instruções de uso


### Dependências

- python3
- python-requests
- python-lxml

Obs.: Testado apenas em Linux.

### Preparação

1. Clonar este repositório
2. Entrar na conferência no JEMS com permissão de chair
3. Descompactar na pasta `data/meta` o arquivo zip obtido em JEMS -> Conference -> Publication chair options -> Download metadata -> Camera ready
4. Descompactar na pasta `data/all` o arquivo zip obtido em JEMS -> Conference -> Chair -> Configurations -> Export all data
5. Cadastrar o evento manualmente na BDBCOMP, informando:
   - Nome do evento/conferência
   - Ano
   - Edição (usar números romanos, de preferência)
   - Quantidade de artigos
   - Idioma
6. Ajustar configurações em `src/csv2bdbcomp.py` (ver comentários no início do código)

### Execução

Abrir um terminal de comandos, localizar a pasta jems2bdbcomp e executar:

```
cd src
./jems2csv.py > output.csv
./csv2bdbcomp.py
```
 
### Observações

- Os scripts fazem parsing dos arquivos XML gerados pelo JEMS e das requisições à BDBCOMP. Por isso, se algo mudar no JEMS ou na BDBCOMP, os scripts provavelmente não vão mais funcionar.

- `jems2csv.py`: gera um CSV na saída padrão, combinando dados de 2 XML gerados pelo JEMS (título, autores, abstract e artigo.pdf). Opcionalmente, este CSV pode ser complementado manualmente com mais 2 colunas contendo a página inicial e final de cada artigo. Essas informações sobre as páginas não são obrigatórias na BDBCOMP, mas são úteis aos usuários. Assim, caso os artigos não tenham páginas numeradas, pode-se usar uma numeração de 1 até o total de páginas de cada artigo.

- `csv2bdbcomp.py`: lê dados de artigos em CSV e os insere na BDBCOMP. Antes de usá-lo, é necessário ajustar configurações dentro do script: dados do evento, entrada para o script (URL ou arquivo) e do intervalo do CSV que se quer processar. Pode-se passar o intervalo do CSV na linha de comando. Por default, o script processa apenas a primeira linha após o cabeçalho do CSV.

- Os scripts não fazem tratamento de exceções. Se algo der errado no parsing ou na comunicação com o servidor da BDBCOMP, a primeira coisa a fazer é observar os erros reportados pelo interpretador.

- Known bug: durante testes do script csv2bdbcomp.py, algumas vezes o servidor da BDBCOMP retornou uma página informando que o artigo foi cadastrado com sucesso, mas o artigo não aparece na área de curadoria da biblioteca. Não foram feitos testes exaustivos, mas pôde-se notar que a página de resposta nesses casos é idêntica à página de resposta de artigos que aparecem na área de curadoria. Se isso acontecer, basta executar o script novamente até que o artigo seja realmente inserido. Artigos duplicados dão erro e artigos inseridos erroneamente podem ser removidos via interface Web da área de curadoria.


