- [x] Descrição dos requisitos funcionais do sistemas (opções e funcionalidades);

- python3    #utilizado python na versao mais recente disponivel
- virtualenv #utilizado para instalação de bibliotecas python em ambiente isolado

# bibliotecas do python :

- flask            #framework reponsavel pela base do servidor
- flask-sqlalchemy #gerenciador de orm
- flask-login      #gerenciador de login
- flask-wtf        #protecao contra csfr

- [x] Modelo do banco de dados que será utilizado (tabelas, campos e relacionamentos);
sera utilizado como banco de dados o sqlite por ser leve e indicado para projetos de pequeno porte
as tabelas serao as seguintes:

| Tabela | Campos da Tabela                        | Descrição                              |
|--------|-----------------------------------------|----------------------------------------|
| user   | id, username, password                  | Tabela com cadastro de admins           |
| credor | id, nome                                | Tabela com cadastro de credores         |
| title  | id, credor_id, description, amount,year,month, status | Tabela com cadastro das dívidas         |

[x] Descrição dos requisitos não-funcionais incluindo as tecnologias que serão utilizadas com uma breve descrição de cada tecnologia. 

# as tecnologias não funcionais  utilizadas foram as seguintes:
- bootstrap 5      #framework css para facil criacao de paginas em pouco tempo
-  boxicons         #fonte personalizada para utilizacao em campo de icones no html
-  jquery           #framework javascript de facil uso



### O sistema Web deverá ter no mínimo os seguintes cadastros:
- [x] Credores;
- [x] Contas a Pagar;

### O sistema Web deverá prover no mínimo as seguintes consultas/relatórios:

- [x] Relação de contas a pagar em um determinado período;
- [x] Relação das contas pagas em um determinado período;
- [x] Contas de um determinado credor em um determinado status (pagas, em atraso e a pagar);
- [x] Relação de credores

    
    
 - [x]  Deverá ser implementada um serviço (API) que receba uma identificação de um credor o status de uma conta (paga, em atraso, a pagar) e retorne como resposta todos os títulos daquele credor naquela situação (similar a consulta 3 das observações anteriores).


- [x] criada a api com sucesso , usando a sequinte base http://127.0.0.1:5000/api/credores/ID-DO-CREDOR/STATUS/
por exemplo para consultar os status de um credor com id 3 usa as seguintes:
- http://127.0.0.1:5000/api/credores/3/devendo/  #para listar as dividas com status devendo 
- http://127.0.0.1:5000/api/credores/3/paga/     #para listar todas dividas pagas
- http://127.0.0.1:5000/api/credores/3/atrazo/   # para listar todas dividas com situacao de atrazo
