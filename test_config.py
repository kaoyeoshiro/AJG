import config

key = config.OPENROUTER_API_KEY
if key and key != "SUA_CHAVE_AQUI":
    print(f"OK - Chave configurada: {key[:20]}...")
else:
    print("ATENCAO - Chave precisa ser configurada")
    print("Para compilar o executavel, use: python build_with_key.py")