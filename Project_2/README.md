Z důvodu zachování citlivých přihlašovacích údajů mimo kód bylo potřeba i zajistit, aby se .env soubor neukládal na git. 
-> Proto byl .env vložen do souboru .gitignore, díky čemuž se .env nepushuje na git.

Údaje jsou v .env uloženy v tomto formátu:

# credentials pro připojení/vytvoření databáte Task_manager a tabulky Tasks
DB_TM_HOST=localhost
DB_TM_USER=root
DB_TM_PASSWORD=mypassword      # heslo "mypassword" zde slouží jen jako ukázka


# credentials pro testovací DB
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=mypasswors         # heslo "mypassword" zde slouží jen jako ukázka