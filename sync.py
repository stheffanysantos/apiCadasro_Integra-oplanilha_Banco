import requests
import mysql.connector


def validate_value(value, value_type, default_value=None):

    if value is None or value == '':
        return default_value  
    
    if value_type == 'int':
        try:
            return int(value)
        except ValueError:
            return default_value  
    
    if value_type == 'float':
        try:
            return float(value)
        except ValueError:
            return default_value 
    
    
    return value


def sync_with_sheetdb():
    print("Sincronização iniciada...")

    
    SHEETDB_URL = 'https://sheetdb.io/api/v1/wnwwe3qjqo19h'

    
    try:
        response = requests.get(SHEETDB_URL)
        response.raise_for_status()
        data = response.json()
        print(f"Dados obtidos da API: {data}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API do SheetDB: {e}")
        return

    # Configurações do banco de dados MySQL
    DB_CONFIG = {
        'user': 'root',
        'password': 'tatu9012',  
        'host': 'localhost',  
        'database': 'controle_estoque',
        'auth_plugin': 'mysql_native_password', 
    }

    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("Conexão com o banco de dados estabelecida.")
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return

   
    try:
        for row in data:
            print(f"Processando linha: {row}")

            # Validando os valores
            id_pedido = validate_value(row.get('ID'), 'int', 0)  
            data_pedido = validate_value(row.get('Data'), 'str', '')  
            produto = validate_value(row.get('Produto'), 'str', '')  
            quantidade = validate_value(row.get('Quantidade'), 'int', 0)  
            preco = validate_value(row.get('Preco'), 'float', 0.0)  
            unidade = validate_value(row.get('Unidade'), 'str', '')  
            empresa = validate_value(row.get('Empresa'), 'str', '')  
            previsao = validate_value(row.get('Previsao'), 'str', '')  
            status = validate_value(row.get('Status'), 'str', 'pendente')  
            observacao = validate_value(row.get('Observacao'), 'str', '')  

            try:
                cursor.execute("""
                    INSERT INTO pedidos (id, data, produto, quantidade, preco, unidade, empresa, previsao, status, observacao)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    data = VALUES(data),
                    produto = VALUES(produto),
                    quantidade = VALUES(quantidade),
                    preco = VALUES(preco),
                    unidade = VALUES(unidade),
                    empresa = VALUES(empresa),
                    previsao = VALUES(previsao),
                    status = VALUES(status),
                    observacao = VALUES(observacao)
                """, (
                    id_pedido,
                    data_pedido,  
                    produto,
                    quantidade,
                    preco,
                    unidade,
                    empresa,
                    previsao,
                    status,
                    observacao
                ))
            except mysql.connector.Error as err:
                print(f"Erro ao processar linha {row}: {err}")

        conn.commit()
        print("Sincronização concluída com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao inserir/atualizar os dados: {err}")
    finally:
        cursor.close()
        conn.close()


sync_with_sheetdb()
