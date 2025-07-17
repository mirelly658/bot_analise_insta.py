'# bot_teste_analise.py'
#==========================
#========================== 


# Importando as bibliotecas necessárias


import instagrapi # Biblioteca para interagir com o Instagram
import time # Biblioteca para manipulação de tempo
import random # Biblioteca para gerar números aleatórios
from instagrapi.exceptions import LoginRequired, ClientError, TwoFactorRequired, ChallengeRequired # Exceções específicas do instagrapi
from instagrapi import Client # Cliente principal do instagrapi 
from getpass import getpass # Para entrada de senha sem exibição no console ( util né,baby?)
import logging # Biblioteca para logging (registro de eventos)  

#_______________________________________________________________________________________________________________________________________________________

               # CONFIGURAÇÃO DO LOGGING PARA REGISTRO DE INFORMAÇÕES E ERROS
#-------------------------------------------------------------------------------------------------


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') # Configura o nível de logging e o formato das mensagens

# Função para registrar mensagens normais
def log_info(message):
    logging.info(message)

# Função para registrar erros
def log_error(message):
    logging.error(message)

# Função para lidar com autenticação de dois fatores
def two_factor_handler(username, password, cl):
    log_info("Autenticação de dois fatores necessária.")
    two_factor_code = input("Digite o código de autenticação de dois fatores (enviado por SMS ou aplicativo): ")
    try:
        # Tenta fazer login novamente com o código de dois fatores
        cl.login(username=username, password=password, verification_code=two_factor_code)
        log_info("Login com autenticação de dois fatores bem-sucedido!")
        return cl
    except Exception as e:
        log_error(f"Erro na autenticação de dois fatores: {e}")
        return None

# Função para lidar com desafios de autenticação
def challenge_code_handler(username, choice):
    log_info(f"Desafio de autenticação necessário. Escolha: {choice}")
    challenge_code = input("Digite o código de autenticação (enviado por e-mail ou SMS): ")
    return challenge_code

# Função para fazer login no Instagram
def login_instagram(username: str, password: str) -> instagrapi.Client:
    cl = instagrapi.Client()  # Cria um objeto para interagir com o Instagram
    cl.delay_range = [1, 5]   # Define pausas de 1 a 5 segundos entre ações
    cl.challenge_code_handler = challenge_code_handler  # Define a função para desafios
    
    for attempt in range(3):  # Tenta fazer login até 3 vezes, com pausas aleatórias
        log_info(f"Tentativa de login {attempt + 1} de 3...")
        try:
            log_info("Iniciando o login...")
            cl.login(username=username, password=password)  # Faz login com usuário e senha
            log_info("Login realizado com sucesso!")
            time.sleep(random.randint(1, 5))  # Pausa aleatória
            return cl
        except LoginRequired:
            log_error("Erro de login. Verifique suas credenciais, que ninguém é adivinha.")
            return None
        except TwoFactorRequired: # Exceção para autenticação de dois fatores
            log_info("Autentificação de dois fatores é necessária, Darling")
            cl = two_factor_handler(username, password, cl) 
            if cl:
                return cl
            return None
        except ChallengeRequired:
            log_info("Desafio de autenticação será tratado pela função challenge_code_handler,meu parceiro.")
            # O handler já foi definido, então o login tentará novamente automaticamente, pela gloria de Deus.
            continue
        except ClientError as e:
            log_error(f"Erro ao fazer login....instagram ta de TPM: {e}")
            return None
        except Exception as e:
            log_error(f"Erro inesperado ao fazer login, e o problema periste..: {e}")
            return None
    log_error("Falha ao fazer login após 3 tentativas,... essa merda.")
    return None

# Função para obter seguidores
def get_followers(cl: instagrapi.Client, username: str):
    try:
        log_info(f"Obtendo seguidores da nossa querida vitima... {username}...brincadeira.")
        user_id = cl.user_id_from_username(username)  # Converte o nome de usuário em ID
        followers = cl.user_followers(user_id)  # Obtém a lista de seguidores
        time.sleep(random.randint(1, 10))  # Pausa aleatória
        log_info(f"{len(followers)} seguidores obtidos com sucesso, baby.")
        return followers
    except ClientError as e:
        log_error(f"Erro ao obter seguidores....tente novamente mai tarde , darling: {e}")
        return None
    except Exception as e:
        log_error(f"Erro inesperado ao obter seguidores: {e}")
        return None
    


    #---------------------------------------------------------------------------------------------------------


# Função principal para executar o bot
if __name__ == "__main__":
    # Pedir nome de usuário e senha
    username = input("Digite seu nome de usuário do Instagram, que eu não sou adivinha: ")
    password = getpass("Digite sua senha do banco...brincadeiera ..é do instagram :) ")
    
    # Fazer login
    cl = login_instagram(username, password)
    
    # Se o login for bem-sucedido, obter seguidores
    if cl:
        followers = get_followers(cl, username)
        if followers:
            log_info("Lista de seguidores....darling:")
            for user_id, user in followers.items():
                log_info(f"Usuário: {user.username} (Nome: {user.full_name})")
        else:
            log_error("Não foi possível obter os seguidores, essa merda.")
    else:
        log_error("Não foi possível fazer login, o universo te odeia..")
    
    log_info("Programa encerrado, agora para de me usar que eu não sou um objeto...(drama queen).")
    time.sleep(random.randint(1, 5))  
    print(f" agora eu vou dormir, porque eu mereço, e você também, baby.")
    time.sleep(random.randint(1, 5))  # Pausa final antes de encerrar o programa
    exit(0)  # Encerra o programa com sucesso
    #_______________________________________________________________________________________________________________________________________________________
    #    bot sob analise, feito por @senhorita.raposinha... personalizavel de acordo com preferencias de usuario, e com tratamento de erros....
    